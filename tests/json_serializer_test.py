""" Module for test class - Node """
import unittest
from modules.json_serializer import JSONSerializer
from classes.class_for_tests import Example

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
        # recursion
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

    def tearDown(self):
        """ End """