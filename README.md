PyVDF
==
Parse VDFs and Valve KeyValue Files

[![Code Climate](https://codeclimate.com/github/noriah/PyVDF/badges/gpa.svg)](https://codeclimate.com/github/noriah/PyVDF)
[![Build Status](https://img.shields.io/travis/noriah/PyVDF.svg?branch=master)](https://travis-ci.org/noriah/PyVDF)
[![PyPI version](https://img.shields.io/pypi/v/pyvdf.svg)](https://pypi.python.org/pypi/PyVDF)
[![Coverage Status](https://img.shields.io/coveralls/noriah/PyVDF.svg)](https://coveralls.io/r/noriah/PyVDF)


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
from PyVDF import PyVDF
Foo = PyVDF()
Foo = PyVDF(data=StringOData)
Foo = PyVDF(infile="/path/to/file.ext")
Foo = PyVDF(infile=fileInstance)
```
