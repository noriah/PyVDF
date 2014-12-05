#!/usr/bin/python

with open("test.vdf") as filec:
  data = filec.read()


from PyVDF import PyVDF

if __debug__:
  import cProfile
  pr = cProfile.Profile()
  pr.enable()

PyVDF.parse(data)

if __debug__:
  pr.disable()
  pr.print_stats('cumulative')
