PyVDF
==
Parse VDFs and Valve KeyValue Files

https://developer.valvesoftware.com/wiki/KeyValues

## API
All functionality is provided through the PyVDF module.
import it and call it to create an instance, or just call the static methods off the import.

### Basic Usage
```python
import PyVDF
Foo = PyVDF()
Foo = PyVDF(data=StringOData)
Foo = PyVDF(infile="/path/to/file.ext")
Foo = PyVDF(infile=fileInstance)
```

#### PyVDF(data=None, infile=None)

Constructor that can take either a string of vdf data, or a filename or file instance
```python
Foo = PyVDF(data='"Apples"{"NoApplesHere" "Nope"}')

Foo = PyVDF(infile='tests/test.vdf')

Foo = PyVDF(infile=open('tests/test.vdf', 'r'))
```


##### load(file/str f)
A method to load the contents of f
```python
Foo = PyVDF()
Foo.load('tests/test.vdf')
Foo.load(open('tests/test.vdf', 'r'))
```

##### loads(str data)
String version of .load

A method to load the contents of a string
```python
Foo = PyVDF()
Foo.loads('"Apples"{"AreApplesHere" "No Apples Here"}')
```

##### getData()
Return a dict or OrderedDict containing the objects data
```python
Foo = PyVDF(infile='tests/test.vdf')
FooBar = Foo.getData()
```

##### setData(dict data)
Set the objects data to the given dict or OrderedDict
```python
Foo = PyVDF()
Foo.setData({'Apples': {'AreApplesHere': 'No Apples Here'}})
```

##### find(str path)
Find a value from a path.
ex. Apples.AreApplesHere

If a path contains a key that has periods in the name, Surround that part of the path in brackets.

ex. ```UserLocalConfigStore.depots.17522.CDN.[content8.steampowered.com]```

The content8.steampowered.com part contains periods, and therefor must be surrounded in brackets.

If the path contains spaces, do not put it in quotes. That will look like literal quotes to python.

A non existant path will return an empty string

```python
Foo.find('Apples.AreApplesHere')
# No Apples Here
```
You can also use array notation get values
```python
Bar = Foo['Apples.AreApplesHere']
```

##### edit(str path, str value)
Like find, but the second argument is the value to set for that key-path

```python
Foo.edit('Apples.AreApplesHere', 'YES!!!')
```
You can also create new paths.
```python
Foo.edit('Non.Existant.Path', 'FooBar')
```

You can also use array notation to set values
```python
Foo['Path.To.Key'] = 'Value'
```

##### findMany(iterable paths)
like find, but will return a list of found or not found values.

Paths must be a list or a tuple of path strings.
```python
Foo.findMany(['Apples.AreApplesHere', 'Non.Existant.Path'])
# ['YES!!!', 'FooBar']
```

##### editMany(iteral paths)
like edit and findMany, however the paths must be a list or tuple of lists or tuples.
```python
Foo.editMany([('Apples.AreApplesHere', 'No'), ['Path', 'Yes']])
```

##### write_file(str filename)
Write the objects data to a file
```python
Foo.write_file('out.vdf')
```

##### toString()
Retrun the objects data as a VDF string
```python
Bar = Foo.toString()
```

### Static Calls

```python
import PyVDF
FooBar = PyVDF.read("/path/to/file.ext")
FooBar = PyVDF.read(fileInstance)
FooBar = PyVDF.reads(StringOData)
```

##### useFastDict(bool var)

##### setIndentation(str var)

##### setSpacing(str var)

##### setCondensed(bool var)

##### setMaxTokenLength(int var)

##### read(file/filename f)

##### reads(str data)

##### formatData(dict data)

##### writeData(file/filename f, dict data)

