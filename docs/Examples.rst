Examples
========

----

Using PyVDF
-----------

.. code-block:: python

   import PyVDF
   vdf = PyVDF()

Read a File
-----------

.. code-block:: python

   # Class Methods
   vdf = PyVDF(infile='/path/to/file')
   value = vdf['Path.to.Key']

   # Static Methods
   vdf = PyVDF.read('/path/to/file')
   value = vdf['Path']['to']['Key']

Read a String
-------------

.. code-block:: python

   food = '''
   "Apple"
   {
       "Pie"    "Good"
       "Cobbler"    "Great"
   }'''

   # Class Methods
   vdf = PyVDF(data=food)
   value = vdf['Apple.Pie']

   # Static Methods
   vdf = PyVDF.reads('/path/to/file')
   value = vdf['Apple']['Pie']


Find Multiple Values
--------------------

.. code-block:: python

   vdf.findMany(['Apple.Pie', 'Apple.Cobbler'])
   "['Good','Great']"

Edit Multiple Values
--------------------

.. code-block:: python

   vdf.editMany([('Apple.Pie','Pumpkin'),
                 ('Apple.Cobbler', 'Pie')])