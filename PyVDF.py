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
from collections import OrderedDict

#############
# PyVDF #
#############
class PyVDF:

  _UseDict = dict
  _AllowNewlines = False
  _UseIndention = "\t"
  _UseSpacing = "\t\t"
  _UseCondensed = False

  def __init__(self):
    self.data = PyVDF._UseDict()

  def __getitem__(self, key):
    return self.find(key)

  def __setitem__(self, key, value):
    self.edit(key, value)

  @staticmethod
  def useFastDict(var = True):
    PyVDF._UseDict = dict if var else OrderedDict

  @staticmethod
  def allowTokenNewlines(var = False):
    PyVDF._AllowNewlines = var

  @staticmethod
  def setIndention(var = "\t"):
    PyVDF._UseIndention = var

  @staticmethod
  def setSpacing(var = "\t\t"):
    PyVDF._UseSpacing = var

  @staticmethod
  def setCondensed(var = False):
    PyVDF._UseCondensed = var

  @staticmethod
  def parse(s):
    s += '\0'
    ci = 0
    line = 0
    grabKey = True
    UsageDict = PyVDF._UseDict
    tokenNewLines = ValueError if PyVDF._AllowNewlines else Exception
    data = UsageDict()
    keys = list()
    keyApp = keys.append
    keyPop = keys.pop
    tree = data

    if PyVDF._AllowNewlines:
      re_quoted_token = re.compile(r'^"((?:\\.|[^"])*)"', re.M)
    else:
      re_quoted_token = re.compile(r'^"((?:\\.|[^"])*)"')

    re_unquoted_token = re.compile(r'^((?:\\.|[^\\"\s\{\}\[\]])*)')

    while 1:
      char = s[ci]

      while char in ('\t', ' '):
        ci += 1
        char = s[ci]

      if char == '"':
        try:
          string = re_quoted_token.match(s[ci:ci + 1200]).group(1)
          ci += len(string) + 1
        except AttributeError:
          string = ''
          while 1:
            ci += 1
            char = s[ci]
            if char == '\0':
              raise Exception("Hit End of Data while reading token")

            if char == '"':
              break

            if char in ('\r', '\n'):
              try:
                raise tokenNewLines("Newline in Token at line {}\n Use allowTokenNewlines(True) to ignore this.".format(line))
              except ValueError:
                line += 1
                ci += 1
            if char == '\\':
              ci += 1
              char = s[ci]
              if char == '\0':
                raise Exception("Hit End of Data while reading token")

            string += char

        if grabKey:
          k = string
        else:
          tree[k] = string
        grabKey = not grabKey

      elif char == '{':
        if not grabKey:
          keyApp(k)
          tree[k] = UsageDict()
          tree = tree[k]
          grabKey = True
        else:
          raise Exception("Value block without a Key at line {}.\n Last Token: {}".format(line, k))

      elif char == '}':
        if grabKey:
          keyPop()
          tree = data
          for key in keys:
            tree = tree[key]
        else:
          Exception("Expected to get a Value, got '}}' instead.\n At line {}.\n Last Token: {}".format(line, k))

      elif char == '\n':
        if s[ci + 1] == '\r':
          ci += 1
        line += 1

      elif char == '\r':
        if s[ci + 1] == '\n':
          ci += 1
        line += 1

      elif char == '/' and s[ci + 1] == '/':
        line += 1
        ci += 1
        while 1:
          ci += 1
          if s[ci] in ('\n', '\r'):
            break

      elif char == '[':
        while 1:
          ci += 1
          if s[ci] == ']':
            break

      elif char == '\0':
        break

      else:
        try:
          string = re_unquoted_token.match(s, ci, ci + 1200).group(1)
          ci += len(string)
        except AttributeError:
          string = ''
          while 1:
            if char in ('\t', ' ', '\n', '\r', '{', '}', '[', ']', '"'):
              break

            if char == '\\':
              ci += 1
              char = s[ci]
              if char == '\0': raise Exception("Hit End of Data while reading token")

            string += char

            ci += 1
            char = s[ci]
            if char == '\0':
              raise Exception("Hit End of Data while reading token")

        if grabKey:
          k = string
        else:
          tree[k] = string
        grabKey = not grabKey
        continue

      ci += 1

    if len(keys) == 0:
      return data

    raise Exception("Missing braces")

  @staticmethod
  def formatData(data):
    condensed = PyVDF._UseCondensed
    indentation = PyVDF._UseIndention
    spacing = PyVDF._UseSpacing
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
            string += '{}"{}"\n'.format(spacing, v.replace("\"", "\\\"").replace("\\", "\\\\"))
      return string
    return loop(data)

  @staticmethod
  def writeData(filename, data):
    if not isinstance(data, dict):
      if isinstance(data, list):
        raise Exception("Cannot write out List Data\n {}".format(repr(data)))
      else:
        raise Exception("Data to write is not a Dictionary\n {}".format(repr(data)))
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
      print(e)

  def load_string(self, string):
    self.data = PyVDF.parse(string)

  def getData(self):
    return self.data

  def setData(self, data):
    self.data = data

  def find(self, path):
    p = [re.sub('[\[\]]', '', w) for w in re.findall(r'[^\.\[\]]+|\[[^\[\]]*\]', path)]
    array = self.data
    for c in p:
      try:
        array = array[c]
      except KeyError:
        return ''
    return array

  def edit(self, path, value):
    UsageDict = PyVDF._UseDict()
    p = [re.sub('[\[\]]', '', w) for w in re.findall(r'[^\.\[\]]+|\[[^\[\]]*\]', path)]
    array = self.data
    a = array
    for c in p[:-1]:
      try:
        if not isinstance(a[c], dict):
          a[c] = UsageDict()
      except KeyError:
        a[c] = ""
      a = a[c]
    if value == ";;DELETE;;":
      a.pop(p[-1], None)
    else:
      a[p[-1]] = value
    self.data = array

  def findMany(self, paths):
    return map(self.find, paths)

  def editMany(self, paths):
    map((lambda (p, v): self.edit(p, v)), paths)

  def write_file(self, filename):
    self.writeData(filename, self.data)

  def write_string(self):
    return PyVDF.formatData(self.data)