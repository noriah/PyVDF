#!/usr/bin/python

# Test file for PyVDF.py

# If no exceptions are given, It passed.

import PyVDF

# import cProfile
# pr = cProfile.Profile()
# pr.enable()

# Test the files using the faster built-in dict
# The built-in dict does not preserve insert order

Apple = PyVDF.read('tests/test.vdf')
if Apple != PyVDF.read('tests/malformed.vdf'):
  raise Exception('Malformed != Test')

if Apple != PyVDF.read('tests/one_line.vdf'):
  raise Exception('One Line != Test')

PyVDF.read('tests/nuthin_but_brace.vdf')
print(Apple)

# Test the files using the slower OrderedDict
# OrderedDict preserves the insert order

PyVDF.useFastDict(False)

Apple = PyVDF.read('tests/test.vdf')
if Apple != PyVDF.read('tests/malformed.vdf'):
  raise Exception('Malformed OD != Test OD')

if Apple != PyVDF.read('tests/one_line.vdf'):
  raise Exception('One Line OD != Test OD')

PyVDF.read('tests/nuthin_but_brace.vdf')

# pr.disable()
# pr.print_stats('cumulative')
