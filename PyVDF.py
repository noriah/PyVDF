__all__ = ['VDFParser', 'VDFWriter']
#####################################
# PyVDF.py                          #
# Author: noriah            #
# For Reading and Writing           #
#    VDF Files                      #
#   (Valve Data Format)             #
# Copyright (c) 2014 noriah #
#####################################

import re
from collections import OrderedDict

#############
# VDFParser #
#############
class VDFParser:
    def __init__(self, filename):
        
        try:
            with open(filename) as filec:
                fdata = ''
                for line in filec:
                    if not line.strip().startswith("//"):
                        fdata += line
                filec.close()
                self.error = False
        except IOError as e:
            print("Could not open '" + filename + "' for reading.")
            print("This is Okay if we are making a new file (say, with VDFWriter).")
            self.error = True
            return

        fdata = list(re.sub('!//.*!', '', fdata))
        fdata.append(None)
        self.fdata = iter(fdata)
        self.layers = 0
        self.data = self.readArray(True)

    def readArray(self, firstRun = False):

        QUOTE = "\""
        ESCAPE = "\\"
        WHITESPACE = ("\t", " ", "\n", "\r")
        CONTROL_OPEN_BRACE = "{"
        CONTROL_CLOSE_BRACE = "}"
        CONTROL_OPEN_BRACKET = "["
        CONTROL_CLOSE_BRACKET = "]"

        MAX_RECURSION = 20

        curchar = ''

        lastkey = '';

        data = OrderedDict()
        grabKey = True
        self.layers += 1

        def readEncapsedToken(char):
            string = ''
            lastchar = ''

            while 1:
                curchar = self.fdata.next()
                if curchar == char and lastchar != ESCAPE:
                    return string.decode("string-escape")
                elif curchar == ESCAPE and lastchar == ESCAPE:
                    lastchar = ''
                else:
                    string += curchar
                lastchar = curchar

        def readToken(char):
            string = char
            lastchar = ''

            while 1:
                curchar = self.fdata.next()
                if curchar in WHITESPACE:
                    return string.decode("string-escape")
                elif curchar == QUOTE and lastchar != ESCAPE:
                    raise VDFParserError("Unquoted Token hit an Unescaped Quote")
                elif curchar == ESCAPE and lastchar == ESCAPE:
                    lastchar = ''
                else:
                    string += curchar
                lastchar = curchar

        if(self.layers > MAX_RECURSION):
            raise VDFParserError("Hit Maximum Layer Limit: " + str(MAX_RECURSION))

        while 1:
            curchar = self.fdata.next()
            
            if curchar is None:
                if firstRun:
                    break;
                else:
                    raise VDFParserError("Hit EOF while reading array")

            elif curchar in WHITESPACE:
                pass

            elif curchar == QUOTE:
                if grabKey:
                    k = readEncapsedToken(QUOTE)
                    grabKey = False
                else:
                    data[k] = readEncapsedToken(QUOTE)
                    grabKey = True

            elif curchar == CONTROL_OPEN_BRACE:
                if grabKey:
                    raise VDFParserError("New array without a key!!!")
                else:
                    data[k] = self.readArray()
                    lastkey = k
                    grabKey = True

            elif curchar == CONTROL_CLOSE_BRACE:
                break

            elif curchar == CONTROL_OPEN_BRACKET:
                c = readEncapsedToken(CONTROL_CLOSE_BRACKET)
                v = data.remove(k)
                data[k + "[" + c + "]"] = v


            else:
                print(curchar)
                if grabKey:
                    k = readToken(curchar)
                    grabKey = False
                else:
                    data[k] = readToken(curchar)
                    grabKey = True

        self.layers -= 1
        return data

    
    def setFile(self, filename):
        self.__init__(filename)

    def getData(self):
        return self.data

    def find(self, path):
        if not isinstance(path, str):
            raise TypeError("Type of param 'path' not 'string'")
        path = re.sub('\[', '"', re.sub('\]', '"', re.sub('.\[', '"', re.sub('\].', '"', path)))).split('"')
        q = 0
        p = list()
        for x in path:
            q += 1
            if q % 2 != 0:
                p += x.split(".")
            else:
                p.append(x)
        array = self.data
        for c in p:
            if array.has_key(c):
                array = array[c]
            else:
                return ''
        return array

    def findMany(self, paths):
        if not isinstance(paths, list):
            raise TypeError("Type of param 'paths' not type 'list'")
        return [self.find(p) for p in paths]


#############
# VDFWriter #
#############
class VDFWriter:
    def __init__(self, filename, data = None):
        self.file = filename
        if data is None:
            self.data = OrderedDict()
        else:
            self.data = data
        self.olddata = self.data

    def setFile(self, filename):
        self.file = filename

    def setData(self, data):
        self.data = data
        self.olddata = data

    def getData(self):
        return self.data

    def edit(self, path):
        if not isinstance(path, str):
            raise TypeError("Type of param 'path' not type 'string'")
        array = self.data
        if not isinstance(array, OrderedDict):
            array = OrderedDict()
        path = path.split("=", 1)
        value = path[1]
        path = path[0]
        path = re.sub('\[', '', re.sub('\]', '', re.sub('.\[', '"', re.sub('\].', '"', path)))).split('"')
        q = 0
        p = list()
        for x in path:
            q += 1
            if q % 2 != 0:
                p += x.split(".")
            else:
                p.append(x)
        a = wrap(array)
        for c in p[:-1]:
            if not a().has_key(c):
                a()[c] = ""
            if not isinstance(a()[c], OrderedDict):
                a()[c] = OrderedDict()
            a = wrap(a()[c])
        if value == ";;DELETE;;":
            a().pop(p[-1], None)
        else:
            a()[p[-1]] = value
        self.data = array

    def editMany(self, paths):
        if not isinstance(paths, list):
            raise TypeError("Type of param 'paths' not type 'list'")
        [self.edit(p) for p in paths]

    def formatData(self, data = None):
        data = self.data if data is None else data
        def loop(array, tab=''):
            string = ''
            for k, v in array.iteritems():
                string += tab + '"' + k + '"'
                if isinstance(v, OrderedDict):
                    string += '\n' + tab + '{\n'
                    string += loop(v, tab + '\t')
                    string += tab + '}\n'
                else:
                    string += '\t\t"' + v.replace("\"", "\\\"") + '"\n'
            return string
        return loop(self.data)

    def write(self):
        array = self.data
        if not isinstance(array, OrderedDict):
            if isinstance(array, list):
                try:
                    raise VDFWriterError(3)
                except VDFWriterError, e:
                    print("Cannot write out List Data: " + str(array))
            else:
                try:
                    raise VDFWriterError(2)
                except VDFWriterError, e:
                    print("Data to write is not a Dictionary: " + stry(array))


        try:
            filec = open(self.file, 'w')
        except IOError as e:
            print("Could not open '" + self.file + "' for writing.")
            print(e)
        data = self.formatData()
        filec.write(data)
        filec.close()
        self.olddata = self.data

    def undo(self):
        self.data = self.olddata


##################
# VDFParserError #
##################
class VDFParserError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


##################
# VDFWriterError #
##################
class VDFWriterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def wrap(obj):
    def __w__():
        return obj
    return __w__
