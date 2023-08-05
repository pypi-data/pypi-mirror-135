# Author: Peter Nardi
# Date: 01/12/22
# License: MIT (terms at the end of this file)

# Title: parser201 - Apache Access Log Parser

# Imports

import datetime as dt
import re
import time
from enum import Enum


class TZ(Enum):
    """Enum to determine adjustment of the timestamp property of a
    `LogParser` object.
    """
    original = 1
    local = 2
    utc = 3


class FMT(Enum):
    """
    Enum to determine the format for the timestamp attribute of a
    `LogParser` object.
    """
    string = 1
    dateobj = 2


class LogParser:
    """The class initializer takes a single line (as a string) from an
    Apache log file and extracts the individual fields into attributes
    within an object.

    Arguments
    ---------
    line : str
        A single line from an Apache access log.
    timezone : {TZ.original, TZ.utc, TZ.local}, optional
        During parsing, adjust the timestamp of the `LogParser` object
        to match a particular timezone. Default is *TZ.original* (no
        adjustment). *TZ.local* adjusts the timestamp to the timezone
        currently selected on the machine running the code. *TZ.utc*
        adjusts the timestamp to [UTC](https:\
        //en.wikipedia.org/wiki/Coordinated_Universal_Time).
    format : {FMT.string, FMT.dateobj}, optional
        Set the format of the timestamp attribute of the `LogParser`
        object. Default is *FMT.string*. Using *FMT.dateobj* will store
        the timestamp attribute as a Python [datetime object](https:\
        //docs.python.org/3/library/datetime.html).

    Attributes
    ----------
    datasize : int
        The size of the response to the client (in bytes).
    ipaddress : str
        The remote host (the client IP).
    referrer : str
        The referrer header of the HTTP request containing the URL of
        the page from which this request was initiated. If none is
        present, this attribute is set to `-`.
    requestline : str
        The request line from the client. (e.g. `"GET / HTTP/1.0"`).
    statuscode : int
        The status code sent from the server to the client (`200`,
        `404`, etc.).
    timestamp : str or datetime object
        The date and time of the request in the following format:

        `dd/MMM/YYYY:HH:MM:SS –hhmm`

        NOTE: `-hhmm` is the time offset from Greenwich Mean Time (GMT).
        Usually (but not always) `mm == 00`. Negative offsets (`-hhmm`)
        are west of Greenwich; positive offsets (`+hhmm`) are east of
        Greenwich.
    useragent : str
        The browser identification string if any is present, and `-`
        otherwise.
    userid : str
        The identity of the user determined by `identd` (not usually
        used since not reliable). If `identd` is not present, this
        attribute is set to `-`.
    username : str
        The user name determined by HTTP authentication. If no username
        is present, this attribute is set to `-`.

    Examples
    --------
    Creating a `LogParser` object with default options. The timestamp
    attribute will not be adjusted and will be stored as a string.
    >>> from parser201 import LogParser, TZ, FMT
    >>> line = # a line from an Apache access log
    >>> lp = LogParser(line)

    Creating a `LogParser` object with custom options. The timestamp
    attribute will adjusted to the timezone on the local machine and
    will be stored as a Python [datetime object](https:\
    //docs.python.org/3/library/datetime.html).
    >>> from parser201 import LogParser, TZ, FMT
    >>> line = # a line from an Apache access log
    >>> lp = LogParser(line, timezone=TZ.local, format=FMT.dateobj)
    """
    # ---------------------------------------------------------------------

    def __init__(self, line, timezone=TZ.original, format=FMT.string):

        # Initialize attributes
        self.ipaddress = ''
        self.userid = ''
        self.username = ''
        self.timestamp = ''
        self.requestline = ''
        self.referrer = ''
        self.useragent = ''
        self.statuscode = 0
        self.datasize = 0

        # Initial check. If the line passed to the initializer is not a string
        # (type == str), then return an empty LogParser object.

        if type(line) != str:
            self.__noneFields()
            return

        # If a valid string is entered, then perform pre-processing. For some
        # lines, an empty field is represented as two quotes back-to-back, like
        # this: "". The regex to pull out agent strings between quotes will
        # incorrectly ignore that field, rather than returning an empty string.
        # Replace "" with "-" to prevent that.

        clean = line.replace('\"\"', '\"-\"')

        # agentStrings: This part of the regex:(?<!\\)\" is a negative
        # lookbehind assertion. It says, "end with a quote mark, unless that
        # quote mark is preceded by an escape character '\'"

        agentStrings = re.findall(r'\"(.+?)(?<!\\)\"', clean)

        # The next one's tricky. We're looking to extract the statuscode and
        # datasize fields. For some entires, the datasize field is '-', but for
        # all entries the returncode field is a reliable integer. If we split
        # the log line on space, then the first purely isnumeric() item in the
        # resulting list should be the returncode. If we capture the index of
        # that code, and take that code and the one next to it from the list,
        # we should have both fields. If the fields are valid integers, then
        # cast to them int; else set them to 0. If any of this fails, then
        # consider that we have a malformed log line and set all the properties
        # to None.

        try:
            L = clean.split(' ')
            i = [j for j in range(len(L)) if L[j].isnumeric()][0]
            codeAndSize = [int(n) if n.isnumeric() else 0 for n in L[i:i+2]]
            # Splitting on '[' returns a list where item [0] contains the first
            # three fields (ipaddress; userid; username), each separated by
            # space.
            first3 = clean.split('[')[0].split()
        except Exception:
            self.__noneFields()
            return

        # Set properties. If any of these fail, then consider that we have a
        # malformed log line and set all the properties to None.

        try:
            self.ipaddress = first3[0]
            self.userid = first3[1]
            self.username = first3[2]
            self.timestamp = re.search(
                r'\[(.+?)\]', clean).group().strip('[]')
            self.requestline = agentStrings[0]
            self.referrer = agentStrings[1]
            self.useragent = agentStrings[2]
            self.statuscode = codeAndSize[0]
            self.datasize = codeAndSize[1]
        except Exception:
            self.__noneFields()
            return

        # Process date/time stamp and adjust timezone/format as indicated

        if timezone == TZ.original and format == FMT.string:
            return

        try:
            dateobj = dt.datetime.strptime(self.timestamp,
                                           '%d/%b/%Y:%H:%M:%S %z')
        except ValueError:
            self.__noneFields()
            return

        sign, hh, mm = self.__decomposeTZ(self.timestamp)

        if timezone == TZ.original:
            pass

        elif timezone == TZ.local:
            zoneString = time.strftime('%z')
            # First convert to GMT
            dateobj = dateobj + (-1*sign*dt.timedelta(hours=hh, minutes=mm))
            # Now convert to local time and replace tzinfo
            sign, hh, mm = self.__decomposeTZ(zoneString)
            zoneObject = dt.timezone(dt.timedelta(hours=hh*sign, minutes=mm))
            dateobj = dateobj + (sign*dt.timedelta(hours=hh, minutes=mm))
            dateobj = dateobj.replace(tzinfo=zoneObject)

        elif timezone == TZ.utc:
            dateobj = dateobj + (-1*sign*dt.timedelta(hours=hh, minutes=mm))
            sign, hh, mm = self.__decomposeTZ('+0000')
            zoneObject = dt.timezone(dt.timedelta(hours=0, minutes=0))
            dateobj = dateobj.replace(tzinfo=zoneObject)

        else:  # pragma no cover
            pass

        # ---------------------------------------

        if format == FMT.string:
            self.timestamp = dateobj.strftime('%d/%b/%Y:%H:%M:%S %z')

        elif format == FMT.dateobj:
            self.timestamp = dateobj

        else:  # pragma no cover
            return

        return

    # ---------------------------------------------------------------------

    # Method to set every field to None, in the event of a corrupted log line.

    def __noneFields(self):
        for property in [p for p in dir(self) if not p.startswith('_')]:
            setattr(self, property, None)
        return

    # ---------------------------------------------------------------------

    # Method for string rendering of a LogParser object

    def __str__(self):
        """The class provides a `__str__` method which renders a
        `LogParser` object as string suitable for display.

        Examples
        --------
        Create a `LogParser` object like this:

        >>> from parser201 import LogParser, TZ, FMT
        >>> line = # a line from an Apache access log
        >>> lp = LogParser(line)

        When you print it, the following is displayed:

        >>> print(lp)
          ipaddress: 81.48.51.130
             userid: -
           username: -
          timestamp: 24/Mar/2009:18:07:16 +0100
        requestline: GET /images/puce.gif HTTP/1.1
         statuscode: 304
           datasize: 2454
            referer: -
          useragent: Mozilla/4.0 compatible; MSIE 7.0; Windows NT 5.1;
        """
        labels = ['ipaddress', 'userid', 'username', 'timestamp',
                  'requestline', 'statuscode', 'datasize', 'referrer',
                  'useragent']
        padding = len(max(labels, key=len))
        L = []

        # Build the string in the same order as the labels.
        for label in labels:
            L.append(f'{label:>{padding}}: {getattr(self, label)}')

        return '\n'.join(L)

    # ---------------------------------------------------------------------

    def __decomposeTZ(self, zone):
        leader, hrs, mins = zone[-5], zone[-4:-2], zone[-2:]
        sign = -1 if leader == '-' else 1
        return sign, int(hrs), int(mins)


# ---------------------------------------------------------------------


if __name__ == '__main__':  # pragma no cover
    pass

# ---------------------------------------------------------------------

# MIT License
#
# Copyright (c) 2020-2022 Peter Nardi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
