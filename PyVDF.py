__all__ = ['PyVDF']
#####################################
# PyVDF.py                          #
# Author: noriah            #
# For Reading and Writing           #
#    VDF Files                      #
#   (Valve Data File)               #
# Copyright (c) 2014 noriah #
#####################################

import re
from collections import OrderedDict, deque

#############
# PyVDF #
#############
class PyVDF:

  _UseDict = dict
  # _AllowNewlines = False
  _OutputIndentation = "\t"
  _OutputSpacing = "\t\t"
  _CondensedOutput = False
  _MaxTokenLength = 1200

  # _ERROR_READ_LongToken = "Holy Long Strings Batman!\n There's a token largers than {} characters on line {}"
  _ERROR_READ_BadToken = "Bad token on line {}.\n Possible Newline or Token greater than {} character in length"
  # _ERROR_READ_TokenNewline = "Newline in Token at line {}\n Use allowTokenNewlines(True) to ignore this."
  _ERROR_READ_BlockNoKey = "Value block without a Key at line {}.\n Last Token: {}"
  _ERROR_READ_CompanionBrace = "Expected to get a Value, got '}}' instead.\n At line {}. Last Token: {}"
  _ERROR_READ_EODToken = "Hit End of Data while reading token"
  _ERROR_READ_EODArray = "Missing braces"

  _ERROR_WRITE_NotDict = "Data is not of type dict\n {}"

  _RE_Token_Quoted = re.compile(r'(?:\\.|[^"])*"')
  _RE_Token_UnQuoted = re.compile(r'^(?:\\.|[^\\"\s\{\}\[\]])*')
  _RE_Path_Seperator = re.compile(r'[^\.\[\]]+|\[[^\[\]]*\]')

  def __init__(self):
    self.data = PyVDF._UseDict()

  def __getitem__(self, key):
    return self.find(key)

  def __setitem__(self, key, value):
    self.edit(key, value)

  @staticmethod
  def useFastDict(var = True):
    PyVDF._UseDict = dict if var else OrderedDict

  # @staticmethod
  # def allowTokenNewlines(var = False):
  #   PyVDF._AllowNewlines = var

  @staticmethod
  def setIndention(var = "\t"):
    PyVDF._OutputIndentation = var

  @staticmethod
  def setSpacing(var = "\t\t"):
    PyVDF._OutputSpacing = var

  @staticmethod
  def setCondensed(var = False):
    PyVDF._CondensedOutput = var

  @staticmethod
  def setMaxTokenLength(var = 1024):
    PyVDF._MaxTokenLength = var

  @staticmethod
  def parse(s):
    
    _dict = PyVDF._UseDict
    _len = len
    _whitespace = frozenset('\t ')
    _newline = frozenset('\n\r')
    # tokenNewLines = ValueError if PyVDF._AllowNewlines else Exception
    
    _quote_match = PyVDF._RE_Token_Quoted.match
    _unquote_match = PyVDF._RE_Token_UnQuoted.match
    _max_length = PyVDF._MaxTokenLength
    
    ci = 0
    line = 0
    grabKey = 1
    
    data = _dict()
    tree = data
    
    keys = deque()
    keyApp = keys.append
    keyPop = keys.pop
    
    try:
      while 1:
        
        while s[ci] in _whitespace:
          ci += 1
        
        char = s[ci]

        if char == '"':
          ci += 1
          string = _quote_match(s[ci:ci + _max_length]).group()[:-1]
          ci += _len(string)

          if grabKey:
            k = string
            grabKey = 0
          else:
            tree[k] = string
            grabKey = 1

        elif char == '\n':
          line += 1

        elif char == '\r':
          if s[ci + 1] == '\n':
            ci += 1
          line += 1
          
        elif char == '{':
          if grabKey:
            raise Exception(PyVDF._ERROR_READ_BlockNoKey.format(line, k))
          else:
            keyApp(k)
            tree[k] = _dict()
            tree = tree[k]
            grabKey = 1

        elif char == '}':
          if grabKey:
            keyPop()
            tree = data
            for key in keys:
              tree = tree[key]
          else:
            raise Exception(PyVDF._ERROR_READ_CompanionBrace.format(line, k))

        elif char == '/' and s[ci + 1] == '/':
          ci += 1
          line += 1
          while 1:
            ci += 1
            if s[ci] in _newline:
              break

        elif char == '[':
          while 1:
            ci += 1
            if s[ci] == ']':
              break

        else:
          string = _unquote_match(s[ci:ci + _max_length]).group()
          ci += _len(string)
            
          if grabKey:
            k = string
            grabKey = 0
          else:
            tree[k] = string
            grabKey = 1
          continue

        ci += 1

    except IndexError:
      if _len(keys) == 0:
        return data
      raise Exception(PyVDF._ERROR_READ_EODArray)
    except AttributeError:
      raise Exception(PyVDF._ERROR_READ_BadToken.format(line, _max_length))


  @staticmethod
  def formatData(data):
    condensed = PyVDF._CondensedOutput
    indentation = PyVDF._OutputIndentation
    spacing = PyVDF._OutputSpacing
    def loop(array, tab=''):
      string = ''
      for k, v in array.iteritems():
        string += '{}"{}"'.format(tab,k)
        if isinstance(v, dict):
          string += '{}{{\n{}{}}}\n'.format(
            '' if condensed else '\n' + tab,
            loop(v, tab + indentation),
            tab)
        else:
            string += '{}"{}"\n'.format(spacing, v)
      return string
    return loop(data)

  @staticmethod
  def writeData(filename, data):
    if not isinstance(data, dict):
      raise Exception(PyVDF._ERROR_WRITE_NotDict.format(repr(data)))
    try:
      filec = open(filename, 'w')
      data = PyVDF.formatData(data)
      filec.write(data)
      filec.close()
    except IOError as e:
      print("Could not open '" + filename + "' for writing.")
      print(e)
    
  def load_file(self, filename):
    try:
      with open(filename) as filec:
        self.data = PyVDF.parse(filec.read())
        filec.close()
    except IOError as e:
      print("Could not open '" + filename + "' for reading.")
      print("Ignore this if you are creating a new file.")

  def load_string(self, string):
    self.data = PyVDF.parse(string)

  def getData(self):
    return self.data

  def setData(self, data):
    self.data = data

  def find(self, path):
    p = [re.sub('[\[\]]', '', w) for w in PyVDF._RE_Path_Seperator.findall(path)]
    array = self.data
    for c in p:
      try:
        array = array[c]
      except KeyError:
        return ''
    return array

  def edit(self, path, value):
    _dict = PyVDF._UseDict
    p = [re.sub('[\[\]]', '', w) for w in PyVDF._RE_Path_Seperator.finall(path)]
    array = self.data
    a = array
    for c in p[:-1]:
      try:
        if not isinstance(a[c], dict):
          a[c] = _dict()
      except KeyError:
        a[c] = _dict()
      a = a[c]
    if value == ";;DELETE;;":
      a.pop(p[-1], None)
    else:
      a[p[-1]] = value
    self.data = array

  def findMany(self, paths):
    return map(self.find, paths)

  def editMany(self, paths):
    map((lambda p, v: self.edit(p, v)), paths)

  def write_file(self, filename):
    self.writeData(filename, self.data)

  def toString(self):
    return PyVDF.formatData(self.data)

  # def toJson(self):
  #   for k, v in

  # def fromJson(self):
