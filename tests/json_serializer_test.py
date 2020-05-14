""" Module for test class - Node """
import unittest
import os
import json
from modules.json_serializer import JSONSerializer
from classes.class_for_tests import Example

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class TestJSONSerializer(unittest.TestCase):
    """ Class for test methods of JSONSerializer """

    # pylint: disable=W0212
    # W0212 - Access to a protected member

    def setUp(self):
        """ Start """

    def test_get_objects(self):
        """ Test for getting objects in class """
        A = Example(20)
        objects = JSONSerializer._JSONSerializer__get_objects(A)
        # int
        self.assertEqual(objects['int_t'], 20)
        # none
        self.assertEqual(objects['none_t'], None)
        # float
        self.assertEqual(objects['float_t'], 15.6)
        # list
        self.assertEqual(objects['list_t'], [])
        # set
        self.assertEqual(objects['set_t'], [{'value': 100}])
        # tuple
        self.assertEqual(objects['tuple_t'], (16, 18, 19, 20))
        # frozenset
        self.assertEqual(objects['frozenset_t'], frozenset({}))
        # bool
        self.assertEqual(objects['booleanT'], True)
        self.assertEqual(objects['booleanF'], False)
        # infinite recursion
        B = Example(30)
        A.none_t = B
        B.none_t = A
        objects = JSONSerializer._JSONSerializer__get_objects(A)
        self.assertEqual(objects, {'int_t': 20, 'set_t': [{'value': 100}],\
        'none_t': {'int_t': 30, 'set_t': [{'value': 100}], 'none_t': 'Object with int_t : 20',\
        'float_t': 15.6, 'list_t': [], 'tuple_t': (16, 18, 19, 20), 'frozenset_t': frozenset(),\
        'booleanT': True, 'booleanF': False, 'get_int': 60},
        'float_t': 15.6, 'list_t': [], 'tuple_t': (16, 18, 19, 20), 'frozenset_t': frozenset(),\
        'booleanT': True, 'booleanF': False, 'get_int': 40})
        self.assertEqual(objects['none_t']['none_t'], 'Object with int_t : 20')

    def test_change_type(self):
        """ Test for changing types """
        A = Example(20)
        objects = JSONSerializer._JSONSerializer__get_objects(A)
        objects = JSONSerializer._JSONSerializer__change_type(objects)
        # int
        self.assertEqual(objects['int_t'], 20)
        # none
        self.assertEqual(objects['none_t'], None)
        # float
        self.assertEqual(objects['float_t'], 15.6)
        # list
        self.assertEqual(objects['list_t'], [])
        # set
        self.assertEqual(objects['set_t'], [{'value': 100}])
        # tuple
        self.assertEqual(objects['tuple_t'], [16, 18, 19, 20])
        # frozenset
        self.assertEqual(objects['frozenset_t'], [])
        # bool
        self.assertEqual(objects['booleanT'], True)
        self.assertEqual(objects['booleanF'], False)

    def test_to_str(self):
        """ Test for conersion in type : str """
        A = Example(20)
        objects = JSONSerializer._JSONSerializer__get_objects(A)
        objects = JSONSerializer._JSONSerializer__change_type(objects)
        objects_str = JSONSerializer._JSONSerializer__to_str(objects)
        self.assertEqual(objects_str.count("'"), 0)
        self.assertEqual(objects_str.count("None"), 0)
        self.assertEqual(objects_str.count(", "), 0)
        self.assertEqual(objects_str.count("True"), 0)
        self.assertEqual(objects_str.count("False"), 0)
    
    def test_dict_to_str(self):
        """ Test for method that helps __to_str to convert dictionary """
        A = Example(20)
        objects = JSONSerializer._JSONSerializer__get_objects(A)
        objects = JSONSerializer._JSONSerializer__change_type(objects)
        objects_str = JSONSerializer._JSONSerializer__to_str(objects)
        with open(r'objects_to_str.txt') as f:
            templates = f.read()
        f = f.close
        self.maxDiff = None
        self.assertEqual(objects_str, templates)
    
    def test_output(self):
        """ Test for method of outputting objects in .json """
        # With file_name
        A = Example(20)
        file_name = 'Example'
        objects = JSONSerializer._JSONSerializer__get_objects(A)
        objects = JSONSerializer._JSONSerializer__change_type(objects)
        objects = JSONSerializer._JSONSerializer__to_str(objects)
        JSONSerializer._JSONSerializer__output(A, objects, file_name)
        file_exists = str(file_name) + '.json' in os.listdir(path=rf'f:\Projects\json_serializer\output')
        self.assertEqual(file_exists, True)
        os.remove(path=rf'f:\Projects\json_serializer\output\{file_name}.json')
        # Without file_name
        file_exists = False
        JSONSerializer._JSONSerializer__output(A, objects, None)
        file_exists = str(A.__class__.__name__) + str(id(A)) + '.json'\
        in os.listdir(path=rf'f:\Projects\json_serializer\output')
        self.assertEqual(file_exists, True)
        os.remove(path=rf'f:\Projects\json_serializer\output\{A.__class__.__name__}{id(A)}.json')
        # Wrong name for Windows
        file_exists = False
        JSONSerializer._JSONSerializer__output(A, objects, 'NUL')
        file_exists = str(file_name) + '.json' in os.listdir(path=rf'f:\Projects\json_serializer\output')
        self.assertEqual(file_exists, False)

    def test_serialize(self):
        """ Test for APi method : serialize """
        A = Example(20)
        JSONSerializer.serialize(A, 'A')
        objects = JSONSerializer._JSONSerializer__get_objects(A)
        objects = JSONSerializer._JSONSerializer__change_type(objects)
        with open(r'..\output\A.json') as f:
            templates = json.load(f)
        f = f.close()
        self.assertEqual(objects, templates)
        os.remove(path=rf'f:\Projects\json_serializer\output\A.json')

    def tearDown(self):
        """ End """