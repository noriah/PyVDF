#!/usr/bin/python

# Test file for PyVDF.py

# If no exceptions are given, It passed.

import PyVDF

# import cProfile
# pr = cProfile.Profile()
# pr.enable()

# Test the files using the faster built-in dict
# The built-in dict does not preserve insert order

print("Reading tests/test.vdf")
Apple = PyVDF.read("tests/test.vdf")
print("Success")

print("Reading tests/malformed.vdf")
if Apple != PyVDF.read("tests/malformed.vdf"):
  raise Exception("Failure: Malformed != Test")
else:
  print("Success: Malformed == Test")

print("Reading tests/one_line.vdf")
if Apple != PyVDF.read("tests/one_line.vdf"):
  raise Exception("Failure: One Line != Test")
else:
  print("Success: One Line == Test")

print("Reading tests/nuthin_but_brace.vdf")
PyVDF.read("tests/nuthin_but_brace.vdf")
print("Success")

# Test the files using the slower OrderedDict
# OrderedDict preserves the insert order


print("Setting useFastDict to False")
PyVDF.useFastDict(False)
print("Success")

print("Reading tests/test.vdf")
Apple = PyVDF.read("tests/test.vdf")
print("Success")

print("Reading tests/malformed.vdf")
if Apple != PyVDF.read("tests/malformed.vdf"):
  raise Exception("Failure: Malformed OD != Test OD")
else:
  print("Success: Malformed OD == Test OD")

print("Reading tests/one_line.vdf")
if Apple != PyVDF.read("tests/one_line.vdf"):
  raise Exception("Failure: One Line OD != Test OD")
else:
  print("Success: One Line OD == Test OD")

print("Reading tests/nuthin_but_brace.vdf")
PyVDF.read("tests/nuthin_but_brace.vdf")
print("Success")

# pr.disable()
# pr.print_stats("cumulative")
