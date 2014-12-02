#!/usr/bin/python

import cProfile
from PyVDF import PyVDF

PyVDF.useFastDict(True)
PyVDF.allowTokenNewlines(True)
pr = cProfile.Profile()
pr.enable()
with open("test.vdf") as filec:
    PyVDF.parse(filec.read())
# pie = VDFParser("test.vdf")
pr.disable()
pr.print_stats('cumulative')
