__all__ = ['VDFParser', 'VDFWriter']
#####################################
# PyVDF.py                          #
# Author: noriah            #
# For Reading and Writing           #
#    VDF Files                      #
#   (Valve Data File)               #
# Copyright (c) 2014 noriah #
#####################################

import re
from collections import OrderedDict

#############
# VDFParser #
#############
class VDFParser:

    UseDict = dict

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
            self.data = self.UseDict()
            return

        fdata = list(re.sub('!//.*!', '', fdata))
        fdata.append(None)
        self.fdata = iter(fdata)
        self.layers = 0
        self.data = self.readArray()

    def __getitem__(self, key):
        return self.find(key)

    @staticmethod
    def useFastDict(var = True):
        VDFParser.UseDict = dict if var else OrderedDict

    def readArray(self):

        QUOTE = "\""
        ESCAPE = "\\"
        WHITESPACE = ("\t", " ", "\n", "\r")
        CONTROL_OPEN_BRACE = "{"
        CONTROL_CLOSE_BRACE = "}"
        CONTROL_OPEN_BRACKET = "["
        CONTROL_CLOSE_BRACKET = "]"
        CONTROL_END = ("\t", " ", "\n", "\r", "{", "}", "[", "]", "\"")

        MAX_RECURSION = 20

        curchar = self.fdata.next()
        data = VDFParser.UseDict()
        grabKey = True
        self.layers += 1

        def readToken(curchar, endchar):
            string = ''
            if curchar == ESCAPE: curchar = self.fdata.next()
            if curchar in endchar: return curchar, string
    
            while curchar is not None:
                string += curchar
                curchar = self.fdata.next()
                if curchar in endchar: return curchar, string
                if curchar == ESCAPE: curchar = self.fdata.next()
    
            raise VDFParserError("Hit EOF while reading token")

        if(self.layers > MAX_RECURSION):
            raise VDFParserError("Hit Maximum Layer Limit: " + str(MAX_RECURSION))

        while curchar is not None:
            if curchar in WHITESPACE: pass
            elif curchar == QUOTE:
                if grabKey:
                    curchar, k = readToken(self.fdata.next(), QUOTE)
                    grabKey = False
                else:
                    curchar, data[k] = readToken(self.fdata.next(), QUOTE)
                    grabKey = True
            elif curchar == CONTROL_OPEN_BRACE:
                if grabKey: raise VDFParserError("New array without a key!!!")
                else:
                    data[k] = self.readArray()
                    grabKey = True
            elif curchar == CONTROL_CLOSE_BRACE:
                self.layers -= 1
                return data
            elif curchar == CONTROL_OPEN_BRACKET:
                c = readToken("", CONTROL_CLOSE_BRACKET)
                v = data.pop(k)
                data[k + "[" + c + "]"] = v
            else:
                if grabKey:
                    curchar, k = readToken(curchar, CONTROL_END)
                    grabKey = False
                    continue
                else:
                    curchar, data[k] = readToken(curchar, CONTROL_END)
                    grabKey = True
                    continue
            curchar = self.fdata.next()

        if self.layers == 1: return data        
        raise VDFParserError("Hit EOF while reading array")
    
    def setFile(self, filename):
        self.__init__(filename)

    def getData(self):
        return self.data

    def find(self, path):
        if not isinstance(path, str):
            raise TypeError("Type of param 'path' not 'string'")
        p = [w.replace('[', '').replace(']', '') for w in re.findall(r'[^\.\[\]]+|\[[^\[\]]*\]', path)]
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

    UseDict = dict
    UseIndention = "\t"
    UseSpacing = "\t\t"
    UseCondensed = False

    def __init__(self, filename, data = None):
        self.file = filename
        if data is None:
            self.data = VDFWriter.UseDict()
        else:
            self.data = data
        self.olddata = self.data

    @staticmethod
    def useFastDict(var = True):
        VDFWriter.UseDict = dict if var else OrderedDict

    @staticmethod
    def setIndention(var = "\t"):
        VDFWriter.UseIndention = var

    @staticmethod
    def setSpacing(var = "\t\t"):
        VDFWriter.UseSpacing = var

    @staticmethod
    def setCondensed(var = False):
        VDFWriter.UseCondensed = var

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
        if not isinstance(array, dict):
            array = VDFWriter.UseDict()
        path = path.split("=", 1)
        value = path[1]
        path = path[0]
        p = [w.replace('[', '').replace(']', '') for w in re.findall(r'[^\.\[\]]+|\[[^\[\]]*\]', path)]
        a = wrap(array)
        for c in p[:-1]:
            if not a().has_key(c):
                a()[c] = ""
            if not isinstance(a()[c], dict):
                a()[c] = VDFWriter.UseDict()
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
                if isinstance(v, dict):
                    string += ('' if VDFWriter.UseCondensed else '\n' + tab)  + '{\n'
                    string += loop(v, tab + VDFWriter.UseIndention)
                    string += tab + '}\n'
                else:
                    string += VDFWriter.UseSpacing + '"' + v.replace("\"", "\\\"") + '"\n'
            return string
        return loop(self.data)

    def write(self):
        array = self.data
        if not isinstance(array, dict):
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
