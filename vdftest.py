#!/usr/bin/python

# Test file for PyVDF.py

# If no exceptions are given, It passed.

import PyVDF

# import cProfile
# pr = cProfile.Profile()
# pr.enable()

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

Food = PyVDF(infile='tests/food.vdf')
Empty = PyVDF()

Pie = Food['Food.Desert.Pie']
NoPie = Food['Food.Desert.NoPie']
Cake, Burger = Food.findMany(['Food.Desert.Cake', 'Food.Meal.Burger'])

PyVDF.useFastDict(False)

Empty['Food.Desert.Cake'] = Burger
Empty.editMany([
              ('Food.Meal.Burger', Pie),
              ('Food.Desert.Pie', Cake)])

PyVDF.setIndentation(" ")
PyVDF.setCondensed(True)
PyVDF.setSpacing(" ")

Empty.write_file('menu.cfg')



# PyVDF.set()

print("Reading tests/test.vdf")
Apple = PyVDF.read("tests/test.vdf")
print("Success")


# pr.disable()
# pr.print_stats("cumulative")
