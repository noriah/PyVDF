import re
from collections import OrderedDict, deque

#############
# PyVDF #
#############
class PyVDF:
  """Parse VDFs and Valve KeyValue Files"""

  __version__ = "2.0.0"
  __release__ = "2.0.0"

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
    """
    Use the faster built-in dict class, or the slower, OrderedDict class

    :param var: Use fast dict or not.
    :type var: :py:obj:`bool`
    """

    PyVDF.__UseDict = dict if var else OrderedDict

  @staticmethod
  def setIndentation(var = "\t"):
    """
    Set the indentation of the output

    :param var: The indentation to use
    :type var: :py:obj:`str`
    """
    PyVDF.__OutputIndentation = var

  @staticmethod
  def setSpacing(var = "\t\t"):
    """
    Set the output spacing

    :param var: The characters to use for spacing
    :type var: :py:obj:`str`
    """
    PyVDF.__OutputSpacing = var

  @staticmethod
  def setCondensed(var = False):
    """
    Set condensed output

    :param var: Use condensed output or not
    :type var: :py:obj:`bool`
    """
    PyVDF.__CondensedOutput = var

  @staticmethod
  def setMaxTokenLength(var = 1024):
    """
    Set the maxmimum token length that can be read.

    :param var: Number of characters allowed in a token
    :type var: :py:obj:`int`
    """
    PyVDF.__MaxTokenLength = var

  @staticmethod
  def read(f):
    """
    Parse a String and return the data

    :param f: The file to read
    :type f: file/str
    :returns: A dictionary object containing the parsed data from f
    :raises: SyntaxError - An error occured reading the data.
    """
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
    """
    Parse a String and return the data

    :param s: The string to read
    :type s: :py:obj:`str`
    :returns: A dict object containing the data from s
    :raises: SyntaxError - An error occured reading the data.
    """
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
    """
    Format a dictionary object to look like a VDF file

    :param data: Data
    :type data: :py:obj:`dict`

    :returns: A vdf string representation of data
    """
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
    """
    Write a dictionary object to a file

    :param f: The file to write to
    :type f: file/string
    :param data: The data to write to the file
    :type data: dict
    """
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
    """
    Parse a file and return a dictionary object

    :param f: The file to read
    :type f: file/string
    :returns: A dict object containing the data from s
    :raises: SyntaxError - An error occured reading the data
    """
    self.__data = PyVDF.read(f)

  def loads(self, data):
    """
    Parse a string and return a dictionary object

    :param data: The data to read
    :type data: :py:obj:`str`
    :returns: A dict object containing the data from s
    :raises: SyntaxError - An error occured reading the data.
    """
    self.__data = PyVDF.reads(data)

  def getData(self):
    """
    Get the instance data
    """
    try:
      return self.__data
    except AttributeError:
      return PyVDF.__UseDict()

  def setData(self, data):
    """
    Set the data of the instance

    :param data: The data
    :type data: :py:obj:`dict`
    """
    self.__data = data

  def find(self, path):
    """
    Find a value

    :param path: The Key path to search for
    :type path: :py:obj:`str`
    :returns: The found value or an empty string if not found.
    """
    p = [re.sub('[\[\]]', '', w) for w in PyVDF.__RE_Path_Seperator.findall(path)]
    array = self.getData()
    for c in p:
      try:
        array = array[c]
      except KeyError:
        return ''
    return array

  def edit(self, path, value):
    """
    Edit a key value

    :param path: The path key for the value
    :type path: :py:obj:`str`
    :param value: The value to be set
    :type value: :py:obj:`str`
    """
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
    """
    Find multiple values

    :param paths: A list of path strings
    :type paths: :py:obj:`str`
    :returns: The found value or an empty string if not found.
    """
    return map(self.find, paths)

  def editMany(self, paths):
    """
    Edit multiple key values

    :param path: A list or tupple of lists or tupples.
    :type path: tuple
    """
    [self.edit(v[0], v[1]) for v in paths]


  def write_file(self, f):
    """
    write the instance data to a file

    :param f: The file to write to
    :type f: :py:obj:`str`
    """
    PyVDF.writeData(f, self.__data)

  def toString(self):
    """
    return the instance data as a vdf string

    :returns: A string of the instance data, in a vdf format
    :rtype: :py:obj:`str`
    """
    return PyVDF.formatData(self.__data)

# TODO - Json

  # def toJson(self):


  # def fromJson(self):

