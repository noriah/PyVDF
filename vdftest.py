#!/usr/bin/python

import cProfile
from PyVDF import VDFParser

VDFParser.useFastDict(True)
VDFParser.allowTokenNewlines(True)
pr = cProfile.Profile()
pr.enable()
with open("test.vdf") as filec:
    VDFParser.parse(filec.read())
# pie = VDFParser("test.vdf")
pr.disable()
pr.print_stats('cumulative')
