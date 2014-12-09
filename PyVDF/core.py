'''
Copyright (c) 2014 noriah vix@noriah.dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software isfurnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

__all__ = ['PyVDF']

import re
import sys
import types
from collections import OrderedDict, deque

#############
# PyVDF #
#############
class PyVDF:
  """Parse VDFs and Valve KeyValue Files

  https://developer.valvesoftware.com/wiki/KeyValues


    >>> food = '''
    ... "Apple"
    ... {
    ...     "Pie"   "Good"
    ...     "Cobbler"        "Great"
    ... }'''

    >>> import PyVDF
    >>> apple = PyVDF(food)
    >>> apple.find('Apple.Pie')
    'Good'
    
    >>> apple.findMany(['Apple.Pie','Apple.Cobbler'])
    ['Good','Great']


  Load a file

    >>> apple.load(file instance/filename)

  Load a string

    >>> apple.loads(data)

  As a Static Method

    >>> apple = PyVDF.read(food)
    >>> apple['Apple']['Pie']
    'Good'

  Use OrderedDict instead of dict

    >>> PyVDF.useFastDict(False)

  Output Data as a String

    * Using Class Method on PyVDF instance
    apple.toString()
    '"Apple"\n{\n\t"Cobbler"\t\t"Great"\n\t"Pie"\t\t"Good"\n}\n'

    * Using Static Method on Dictionary
    >>> PyVDF.formatData(apple)
    '"Apple"\n{\n\t"Cobbler"\t\t"Great"\n\t"Pie"\t\t"Good"\n}\n'

  Set Condensed Output (Curly Braces on same line as Key)
    
    >>> PyVDF.setCondensed(True)
    >>> PyVDF.formatData(apple)
    '"Apple"{\n\t"Cobbler"\t\t"Great"\n\t"Pie"\t\t"Good"\n}\n'

  Set Output Spacing and/or Indentation

    >>> PyVDF.setIndention('\t\t\t')
    >>> PyVDF.setSpacing('What a Terrible Spacer')

    >>> PyVDF.formatData(apple)
    '"Apple"\n{\n\t\t\t"Cobbler"What a Terrible Spacer"Great"\n\t\t\t"Pie"What a Terrible Spacer"Good"\n}\n'

  Set Maximum Token length (Outline from valve says Max of 1024,
  but they broke their own rule) Default is 1200

    >>> PyVDF.setMaxTokenLength(2000)

  Write a file

    * Static Method
    >>> PyVDF.writeData(file instance/filename, apple)

    * PyVDF Instance
    >>> apple.write_file(file instance/filename)

  Get Data from Instance

    >>> apple.getData()

  Set Instance data

    >>> apple.setData(apple_new)

  """

  __version__ = "1.0.4"

  __UseDict = dict
  __OutputIndentation = "\t"
  __OutputSpacing = "\t\t"
  __CondensedOutput = False
  __MaxTokenLength = 1200

  __ERR_BadToken = "Bad token on line {}.\n Possible Newline or Token greater than {} character in length"
  __ERR_BlockNoKey = "Value block without a Key at line {}.\n Last Token: {}"
  __ERR_CompanionBrace = "Expected to get a Value, got '}}' instead.\n At line {}. Last Token: {}"
  __ERR_EODToken = "Hit End of Data while reading token"
  __ERR_EODArray = "Missing braces"

  __ERR_NotDict = "Data is not of type dict\n {}"

  __RE_Token_Quoted = re.compile(r'(?:\\.|[^"])*"')
  __RE_Token_UnQuoted = re.compile(r'^(?:\\.|[^\\"\s\{\}\[\]])*')
  __RE_Path_Seperator = re.compile(r'[^\.\[\]]+|\[[^\[\]]*\]')

  def __init__(self, data=None, infile=None):
    if data != None:
      self.__data = PyVDF.reads(data)
    elif infile != None:
      self.__data = PyVDF.read(infile)
    return

  def __getitem__(self, key):
    return self.find(key)

  def __setitem__(self, key, value):
    self.edit(key, value)

  @staticmethod
  def useFastDict(var = True):
    PyVDF.__UseDict = dict if var else OrderedDict

  @staticmethod
  def setIndentation(var = "\t"):
    PyVDF.__OutputIndentation = var

  @staticmethod
  def setSpacing(var = "\t\t"):
    PyVDF.__OutputSpacing = var

  @staticmethod
  def setCondensed(var = False):
    PyVDF.__CondensedOutput = var

  @staticmethod
  def setMaxTokenLength(var = 1024):
    PyVDF.__MaxTokenLength = var

  @staticmethod
  def read(f):
    try:
      return PyVDF.reads(f.read())
    except AttributeError:
      pass
      
    try:
      with open(f, 'r') as filec:
        data = PyVDF.reads(filec.read())
        filec.close()
        return data
    except IOError as e:
      print("Could not open '" + f + "' for reading.")
      print("Ignore this if you are creating a new file.")

    return PyVDF.__UseDict()

  @staticmethod
  def reads(s):
    _dict = PyVDF.__UseDict
    _len = len
    _whitespace = frozenset('\t ')
    _newline = frozenset('\n\r')
    
    _quote_match = PyVDF.__RE_Token_Quoted.match
    _unquote_match = PyVDF.__RE_Token_UnQuoted.match
    _max_length = PyVDF.__MaxTokenLength
    
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

        # elif char == '\r':
        #   if s[ci + 1] == '\n':
        #     ci += 1
        #   line += 1
          
        elif char == '{':
          if grabKey:
            raise Exception(PyVDF.__ERR_BlockNoKey.format(line, k))
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
            raise Exception(PyVDF.__ERR_CompanionBrace.format(line, k))

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
      raise Exception(PyVDF.__ERR_EODArray)
    except AttributeError:
      raise Exception(PyVDF.__ERR_BadToken.format(line, _max_length))


  @staticmethod
  def formatData(data):
    condensed = PyVDF.__CondensedOutput
    indentation = PyVDF.__OutputIndentation
    spacing = PyVDF.__OutputSpacing
    def loop(array, tab=''):
      string = ''
      for k, v in array.items():
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
  def writeData(f, data):
    if not isinstance(data, dict):
      raise Exception(PyVDF.__ERR_NotDict.format(repr(data)))
    data = PyVDF.formatData(data)
    try:
      f.write(data)
    except AttributeError:
      pass
    
    try:
      filec = open(f, 'w')
      filec.write(data)
      filec.close()
    except IOError as e:
      print("Could not open '" + f + "' for writing.")
      print(e)
    
  def load(self, f):
    self.__data = PyVDF.read(f)

  def loads(self, data):
    self.__data = PyVDF.reads(data)

  def getData(self):
    try:
      return self.__data
    except AttributeError:
      return PyVDF.__UseDict()

  def setData(self, data):
    self.__data = data

  def find(self, path):
    p = [re.sub('[\[\]]', '', w) for w in PyVDF.__RE_Path_Seperator.findall(path)]
    array = self.getData()
    for c in p:
      try:
        array = array[c]
      except KeyError:
        return ''
    return array

  def edit(self, path, value):
    _dict = PyVDF.__UseDict
    p = [re.sub('[\[\]]', '', w) for w in PyVDF.__RE_Path_Seperator.findall(path)]
    array = self.getData()
    a = array
    for c in p[:-1]:
      try:
        if not isinstance(a[c], dict):
          a[c] = _dict()
      except KeyError:
        a[c] = _dict()
      a = a[c]
    if value == None:
      a.pop(p[-1], None)
    else:
      a[p[-1]] = value
    self.__data = array

  def findMany(self, paths):
    return map(self.find, paths)

  def editMany(self, paths):
    [self.edit(v[0], v[1]) for v in paths]
      

  def write_file(self, f):
    PyVDF.writeData(f, self.__data)

  def toString(self):
    return PyVDF.formatData(self.__data)

# TODO - Json

  # def toJson(self):


  # def fromJson(self):
