#!/usr/bin/python

import cProfile
from PyVDF import VDFParser

VDFParser.useFastDict(True)
pr = cProfile.Profile()
pr.enable()
pie = VDFParser("test.vdf")
pr.disable()
pr.print_stats('cumulative')
