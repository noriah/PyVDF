__all__ = ['VDFParser', 'VDFWriter']
#####################################
# PyVDF.py                          #
# Author: noriah            #
#                                   #
# For Reading and Writing           #
#    VDF Files                      #
#   (Valve Data Format)             #
#                                   #
# Copyright (c) 2013 noriah #
#####################################

import re
from collections import OrderedDict

class VDFParser:
	def __init__(self, filename):
		
		self.data = OrderedDict()
		
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

		self.fdata = list(re.sub('!//.*!', '', fdata))
		self.fdata.append(None)
		self.__parse__()

	def __parse__(self):

		if self.error:
			return None

		data = OrderedDict() 
		array = wrap(data)
		path_sep = '\\\\+++\\\\/+++\\//+++//'
		key = ''
		string = ''
		path = ''
		grabKey = True
		quoted = False
		reading = False
		lastchar = ''
		lastlastchar = ''
		curchar = ''
		whitespace = ("\t", " ", "\n", "\r")
		quote = "\""
		escape = "\\"
		openbrace = "{"
		closebrace = "}"

		def formatPath(string):
			string = string.split(path_sep)
			for i, s in enumerate(string):
				if re.search("\.", s) != None:
					string[i] = "[" + s + "]"
			return ".".join(string)

		def update():
			if grabKey:
				#key, string, grabKey
				return [string, '', False]
			else:
				if array().has_key(key):
					raise VDFParserError("[5]Key Already Exists: " + formatPath(path + path_sep + key))
				array()[key] = string
				return ['', '', True]

		def newLevel():
			if grabKey:
				raise VDFParserError("[2]Something went wrong near here: " + formatPath(path))

			if array().has_key(key):
				raise VDFParserError("[5]Key Already Exists: " + formatPath(path + path_sep + key))
			array()[key] = OrderedDict()
			a = wrap(array()[key])
			p = path
			if p == '':
				p += key
			else:
				p += path_sep + key

			return [a, '', p, True]

		def oldLevel():
			if not grabKey:
				raise VDFParserError("[2]Something went wrong near here: " + formatPath(path))
			a = wrap(data)
			full_path = path.split(path_sep)
			new_path = ''
			if full_path:
				for x in full_path[:-1]:
					if new_path == '':
						new_path += x
					else:
						new_path += path_sep + x
					a = wrap(a()[x])

			return [a, new_path, True]
		
		
		for curchar in self.fdata:
			if not reading and curchar in whitespace:
				continue
			
			if curchar is None:
				if reading:
					if not quoted:
						if not (lastchar == quote and lastlastchar != escape):
							if string:
								if grabKey:
									raise VDFParserError("[4]Invalid Data at End of File: " + string)
								else:
									update()
				else:
					if key != '':
						raise VDFParserError("[4]Invalid Data at End of File: " + string)
				break

			if curchar == quote and lastchar != escape:
				if reading:
					reading = False
					quoted = False
					key, string, grabKey = update()
				else:
					reading = True
					quoted = True

			elif curchar in whitespace:
				if reading:
					if not quoted:
						reading = False
						key, string, grabKey = update()
					else:
						string += curchar
			
			elif curchar == openbrace:
				if reading:
					if not quoted:
						reading = False
						key, string, grabKey = update()
						array, key, path, grabKey = newLevel()
					else:
						string += curchar
				else:
					array, key, path, grabKey = newLevel()
					

			elif curchar == closebrace:
				if reading:
					if not quoted:
						reading = False
						key, string, grabKey = update()
						array, path, grabKey = oldLevel()
					else:
						string += curchar
				else:
					array, path, grabKey = oldLevel()
			else:
				string += curchar
				reading = True
			
			lastlastchar = lastchar
			lastchar = curchar
		self.data = data
	
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
					string += '\t\t"' + v + '"\n'
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


class VDFWriterError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class VDFParserError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


def wrap(obj):
	def __w__():
		return obj
	return __w__
