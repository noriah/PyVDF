from PyVDF import PyVDF
import pytest
import unittest

class RunTests(unittest.TestCase):

  def setUp(self):
    self.Apple = PyVDF.read("tests/test.vdf")

  def test_read_unformatted(self):
    m = PyVDF.read("tests/malformed.vdf")
    assert m == self.Apple

  def test_read_single_line(self):
    ol = PyVDF.read("tests/one_line.vdf")
    assert ol == self.Apple

  def test_read_braces_only(self):
    PyVDF.read("tests/nuthin_but_brace.vdf")

  def test_read_fake_file(self):
    null = PyVDF(infile='apples')

  def test_find(self):
    Food = PyVDF(infile='tests/food.vdf')
    Pie = Food['Food.Desert.Pie']
    NoPie = Food['Food.Desert.NoPie']
    assert Pie == "Apple"
    assert NoPie == ""

  def test_find_many(self):
    Food = PyVDF(infile='tests/food.vdf')
    Cake, Burger = Food.findMany(['Food.Desert.Cake', 'Food.Meal.Burger'])
    assert Cake == "Vanilla"
    assert Burger == "CheeseBurger"

  def test_error_token_length(self):
    PyVDF.setMaxTokenLength(3)
    with pytest.raises(Exception):
      null = PyVDF('"Apples"{"NoApplesHere" "Nope"}')
    PyVDF.setMaxTokenLength(1200)

  def test_edit(self):
    Food = PyVDF()
    Food['Food.Desert.Cake'] = "CheeseBurger"
    assert Food.getData()['Food']['Desert']['Cake'] == "CheeseBurger"

  def test_edit_many(self):
    Food = PyVDF()
    Food.editMany([('Food.Meal.Burger', "Apple"),
                   ('Food.Desert.Pie', "Vanilla")])
    assert Food.getData()['Food']['Meal']['Burger'] == "Apple"
    assert Food.getData()['Food']['Desert']['Pie'] == "Vanilla"

  def test_companion_brace(self):
    with pytest.raises(Exception):
      PyVDF(infile='tests/breakit.vdf')

  def test_missing_brace(self):
    with pytest.raises(Exception):
      PyVDF(infile='tests/breakit2.vdf')

  def test_block_no_key(self):
    with pytest.raises(Exception):
      PyVDF(infile='tests/breakit3.vdf')

  def test_data_not_dictionary(self):
    Error = PyVDF()
    Error['Nope.Nope'] = None
    with pytest.raises(Exception):
      Error.setData(list())
      Error.write_file('Apples.out')

  def test_write_directory_fail(self):
    Error = PyVDF()
    Error.setData({"apple": ['apples']})
    Error['apple.pie'] = None
    Error.write_file('./')

  def test_set_data_valid(self):
    Food = PyVDF()
    Food.load('tests/test.vdf')
    Food.loads('"Apples"{"NoApplesHere" "Nope"}')
    Food.toString()

  def test_write_file_static(self):
    PyVDF.useFastDict(False)

    Food = PyVDF()
    Food['Food.Meal.Burger'] = "Apple"

    PyVDF.setIndentation(" ")
    PyVDF.setCondensed(True)
    PyVDF.setSpacing(" ")
    Food.write_file('menu.cfg')
