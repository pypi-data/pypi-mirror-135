![GitHub](https://img.shields.io/github/license/geozeke/parser201)
![PyPI](https://img.shields.io/pypi/v/parser201)
![PyPI - Status](https://img.shields.io/pypi/status/parser201)
![GitHub last commit](https://img.shields.io/github/last-commit/geozeke/parser201)
![GitHub issues](https://img.shields.io/github/issues/geozeke/parser201)
![PyPI - Downloads](https://img.shields.io/pypi/dm/parser201)
![GitHub repo size](https://img.shields.io/github/repo-size/geozeke/parser201)
![Lines of code](https://img.shields.io/tokei/lines/github/geozeke/parser201)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/parser201)

<br>

<img src="https://drive.google.com/uc?export=view&id=1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc" width="120"/>

## Features

The centerpiece of the parser201 module is the LogParser class. The class initializer takes a single line from an Apache access log file and extracts the individual fields into attributes within an object.

## Installation

```
pip3 install parser201
```

## Usage

The most common use-case for parser201 is importing individual lines from an Apache access log file and creating LogParser objects, like this:

```python
from parser201 import LogParser, FMT, TZ

with open('access.log', 'r') as f:
    for line in f:
        lp = LogParser(line)
        # Use lp as desired: add to List, Dictionary, etc.
```

## Documentation

See: [parser201 Documentation](https://geozeke.github.io/parser201).

## Version History

* 1.1.5 (2022-01-17)
	* Code linting and cleanup.<br><br>
* 1.1.4 (2021-12-23)
	* Documentation cleanup.<br><br>
* 1.1.3 (2021-12-19)
	* Make file tuning.
	* Documentation cleanup.
	* Added site logo to README.md.<br><br>
* 1.1.0 (2021-11-13)
	* Implemented selectable timestamp conversion options {*original*, *local*, [*UTC*](https://en.wikipedia.org/wiki/Coordinated_Universal_Time)}.
	* Implemented selectable formatting options for timestamp attribute {*string*, *dateobj*}.
	* Migrated API reference to GitHub pages.
	* Code cleanup.<br><br>
* 1.0.2 (2021-11-05)
	* Documentation cleanup.<br><br>
* 1.0.0 (2021-11-04)
	* Stable production release.
	* Migrated to a new development framework.
	* Implemented more robust and compartmentalized test cases.
	* Code tuning.<br><br>
* 0.2.0 (2021-10-31)
	* Changed behavior to gracefully fail for any malformed input line. If an input line cannot be successfully parsed, all attributes of the returned object are set to `None` and no messages are printed.
	* Added additional pytest cases to verify failure behavior.<br><br>
* 0.1.9 (2021-09-15)
	* Code cleanup for pep8 compliance.
	* Cleaned up Makefiles and scripts to remove references to python (meaning python2) and replace it with python3.<br><br>
* 0.1.7 (2021-06-05)
	* Re-tooled testing scripts to use parameterized test data, and conduct more robust testing.<br><br>
* 0.1.6 (2020-12-19)
	* Addressed exception handling for initializer input not being a valid string data type.
	* Documentation cleanup.<br><br>
* 0.1.5 (2020-10-26)
	* Enabled automatic deployment of tagged releases to pypi from travis using encrypted token.
	* Converted references to the master branch in the git repository to main across the documentation set.
	* Documentation cleanup.<br><br>
* 0.1.4 (2020-10-24)
	* Initial pypi release.
	* Fixed test file filtering issue in .gitignore.
	* Dependency fix for travis tests.<br><br>
* 0.1.1 (2020-10-22)
	* Follow-on testing on test.pypi.org.<br><br>
* 0.1.0 (2020-10-18)
	* Initial testing on test.pypi.org.