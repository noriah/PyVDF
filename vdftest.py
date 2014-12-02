#!/usr/bin/python

import cProfile
# from guppy import hpy
# h = hpy()
# h.setrelheap()
from PyVDF import PyVDF

PyVDF.useFastDict(True)
PyVDF.allowTokenNewlines(True)
pr = cProfile.Profile()
pr.enable()
# with open("localconfig.vdf") as filec:
#     PyVDF.parse(filec.read())

pie = PyVDF()
pie.load_file("test.vdf")
# print(h.heap())
# print(h.heap().more)

pr.disable()
pr.print_stats('cumulative')
