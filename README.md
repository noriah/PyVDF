PyVDF
==
Parse VDFs and Valve KeyValue Files

[![Build Status](https://img.shields.io/travis/noriah/PyVDF.svg?branch=master&style=flat-square)](https://travis-ci.org/noriah/PyVDF)[![PyPI version](https://img.shields.io/pypi/v/pyvdf.svg?style=flat-square)](https://pypi.python.org/pypi/PyVDF)[![Coverage Status](https://img.shields.io/coveralls/noriah/PyVDF.svg?style=flat-square)](https://coveralls.io/r/noriah/PyVDF)[![Downloads](https://img.shields.io/pypi/dm/PyVDF.svg?style=flat-square)](https://pypi.python.org/pypi/PyVDF)


## Documentation
* PyVDF - https://noriah.github.io/PyVDF
* KeyValues - https://developer.valvesoftware.com/wiki/KeyValues

## Installation
`pip install PyVDF`

## API
All functionality is provided through the PyVDF module.
import it and call it to create an instance, or just call the static methods off the import.

## Basic Usage
```python
import PyVDF
Foo = PyVDF()
Foo = PyVDF(data=StringOData)
Foo = PyVDF(infile="/path/to/file.ext")
Foo = PyVDF(infile=fileInstance)
```