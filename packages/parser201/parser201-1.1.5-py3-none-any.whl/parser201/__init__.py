"""
.. include:: ../../docs/intro.md
"""

__version__ = '1.1.5'

from .classes import FMT  # noqa
from .classes import TZ  # noqa
from .classes import LogParser  # noqa

# pdoc will look here to determine which members to leave out of the
# documentation.
__pdoc__ = {}
__pdoc__['classes.FMT'] = False
__pdoc__['classes.TZ'] = False
__pdoc__['classes.LogParser.__str__'] = True
