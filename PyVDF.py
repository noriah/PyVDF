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

# QUOTE = '"'
# ESCAPE = '\\'
# NULL = '\0'
# WHITESPACE = ('\t', ' ')
# NEWLINE = ('\r', '\n')
# CONTROL_OPEN_BRACE = '{'
# CONTROL_CLOSE_BRACE = '}'
# CONTROL_OPEN_BRACKET = '['
# CONTROL_CLOSE_BRACKET = ']'
# CONTROL_END = ('\t', ' ', '\n', '\r', '{', '}', '[', ']', '"')

#############
# VDFParser #
#############
class VDFParser:

  _UseDict = dict
  _AllowNewlines = False

  def __init__(self, filename):

    try:
      with open(filename) as filec:
        fdata = filec.read()
        filec.close()
    except IOError as e:
      print("Could not open '" + filename + "' for reading.")
      print("This is Okay if we are making a new file (say, with VDFWriter).")
      self.data = self._UseDict()
      return
    self.data = self.parse(fdata)

  def __getitem__(self, key):
    return self.find(key)

  @staticmethod
  def useFastDict(var = True):
    VDFParser._UseDict = dict if var else OrderedDict

  @staticmethod
  def allowTokenNewlines(var = False):
    VDFParser._AllowNewlines = var

  @staticmethod
  def parse(s):
    s += '\0'
    charIndex, line, offset, grabKey = 0, 1, 0, True
    UsageDict = VDFParser._UseDict
    tokenNewLines = ValueError if VDFParser._AllowNewlines else Exception
    data, keys = UsageDict(), list()
    keyApp, keyPop = keys.append, keys.pop
    tree = data

    while s[charIndex] != '\0':
      char = s[charIndex]

      while char in ('\t', ' '):
        offset += 1
        charIndex += 1
        char = s[charIndex]

      if char == '\n':
        if s[charIndex + 1] == '\r':
          charIndex += 1
        line += 1
        offset = -1

      elif char == '\r':
        if s[charIndex + 1] == '\n':
          charIndex += 1
        line += 1
        offset = -1

      elif char == '/' and s[charIndex + 1] == '/':
        line += 1
        offset = -1
        charIndex += 1
        while 1:
          charIndex += 1
          if s[charIndex] in ('\n', '\r'):
            break

      elif char == '"':
        string = ''
        while 1:
          charIndex += 1
          offset += 1
          char = s[charIndex]
          if char == '\0':
            raise Exception("Hit EOF while reading token")

          if char == '"':
            break

          if char in ('\r', '\n'):
            try:
              raise tokenNewLines("Newline in Token at line {}\n Use allowTokenNewlines(True) to ignore this.".format(line))
            except ValueError:
              line += 1
              offset = 0
              charIndex += 1
              continue
          if char == '\\':
            charIndex += 1
            offset += 1
            char = s[charIndex]
            if char == '\0':
              raise Exception("Hit EOF while reading token")

          string += char

        if grabKey:
          k = string
        else:
          tree[k] = string
        grabKey = not grabKey
      
      elif char == '{':
        if grabKey:
          raise Exception("Value block without a Key at line {}, column {}".format(line, offset))
        else:
          keyApp(k)
          tree[k] = UsageDict()
          tree = tree[k]
          grabKey = True
      
      elif char == '}':
        if grabKey:
          keyPop()
          tree = data
          for key in keys:
            tree = tree[key]
        else:
          Exception("Expected to get a Value, got '}' instead.\n At line {}, column {}, key {}".format(line, offset, k))
      
      elif char == '[':
        while 1:
          charIndex += 1
          offset += 1
          if s[charIndex] == ']':
            break
      
      else:
        string = ''
        while 1:
          if char in ('\t', ' ', '\n', '\r', '{', '}', '[', ']', '"'):
            break

          if char in ('\r', '\n'):
            raise Exception("Newline in Un-quoted Token at line {}\n Use allowTokenNewlines(True) to ignore this.".format(line))
          if char == '\\':
            charIndex += 1
            offset += 1
            char = s[charIndex]
            if char == '\0': raise Exception("Hit EOF while reading token")

          string += char

          charIndex += 1
          offset += 1
          char = s[charIndex]
          if char == '\0':
            raise Exception("Hit EOF while reading token")
        
        if grabKey:
          k = string
        else:
          tree[k] = string
        grabKey = not grabKey
        continue

      charIndex += 1
      offset += 1
    
    if len(keys) == 0:
      return data
      
    raise Exception("Missing braces")
  
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
    return map(self.find, paths)


#############
# VDFWriter #
#############
class VDFWriter:

  _UseDict = dict
  _UseIndention = "\t"
  _UseSpacing = "\t\t"
  _UseCondensed = False

  def __init__(self, filename, data = None):
    self.file = filename
    if data is None:
      self.data = VDFWriter._UseDict()
    else:
      self.data = data

  @staticmethod
  def useFastDict(var = True):
    VDFWriter._UseDict = dict if var else OrderedDict

  @staticmethod
  def setIndention(var = "\t"):
    VDFWriter._UseIndention = var

  @staticmethod
  def setSpacing(var = "\t\t"):
    VDFWriter._UseSpacing = var

  @staticmethod
  def setCondensed(var = False):
    VDFWriter._UseCondensed = var

  @staticmethod
  def __format_data__(data):
    def loop(array, tab=''):
      string = ''
      for k, v in array.iteritems():
        string += tab + '"' + k + '"'
        if isinstance(v, dict):
          string += ('' if VDFWriter._UseCondensed else '\n' + tab)  + '{\n'
          string += loop(v, tab + VDFWriter._UseIndention)
          string += tab + '}\n'
        else:
          string += VDFWriter._UseSpacing + '"' + v.replace("\"", "\\\"") + '"\n'
      return string
    return loop(data)

  @staticmethod
  def writeData(filename, data):
    if not isinstance(data, dict):
      if isinstance(data, list):
        try:
          raise VDFWriterError(3)
        except VDFWriterError, e:
          print("Cannot write out List Data: " + str(data))
      else:
        try:
          raise VDFWriterError(2)
        except VDFWriterError, e:
          print("Data to write is not a Dictionary: " + str(data))
    try:
      filec = open(filename, 'w')
    except IOError as e:
      print("Could not open '" + filename + "' for writing.")
      print(e)
    data = VDFWriter.__format_data__(data)
    filec.write(data)
    filec.close()

  def setFile(self, filename):
    self.file = filename

  def setData(self, data):
    self.data = data

  def getData(self):
    return self.data

  def edit(self, path):
    if not isinstance(path, str):
      raise TypeError("Type of param 'path' not type 'string'")
    array = self.data
    if not isinstance(array, dict):
      array = VDFWriter._UseDict()
    path, value = path.split("=", 1)
    p = [w.replace('[', '').replace(']', '') for w in re.findall(r'[^\.\[\]]+|\[[^\[\]]*\]', path)]
    a = wrap(array)
    for c in p[:-1]:
      if not a().has_key(c):
        a()[c] = ""
      if not isinstance(a()[c], dict):
        a()[c] = VDFWriter._UseDict()
      a = wrap(a()[c])
    if value == ";;DELETE;;":
      a().pop(p[-1], None)
    else:
      a()[p[-1]] = value
    self.data = array

  def editMany(self, paths):
    if not isinstance(paths, list):
      raise TypeError("Type of param 'paths' not type 'list'")
    map(self.edit, paths)

  def write(self):
    VDFWriter.writeData(self.file, self.data)


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
