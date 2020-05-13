""" Module of set """
import ast
from accessify import implements
from modules.set.interface_set import ISet
from modules.tree.avl_tree import AVLTree

TYPES = {
    'int' : int,
    'str' : str,
    'float' : float,
    'bool' : bool,
    'list' : list,
    'dict' : dict,
    'set' : set,
    'tuple' : tuple,
}

@implements(ISet)
class Set():
    """ Class of set on avl tree """
    __tree = None
    __set_type = None

    def __init__(self, tree_type):
        """ Initialization """
        if self._check_type(tree_type):
            self.__tree = AVLTree()
            self.__set_type = tree_type

    def add(self, val):
        """ Add value in set """
        val = self._conversion(val)
        if self.__tree.search(val):
            print("Element is already exist") 
        else:
            if isinstance(val, TYPES[self.__set_type]):
                self.__tree.insert(val)
            else:
                print("TypeError : Wrong Input")

    def clear(self):
        """ Delete all elements in set """
        del self.__tree
        self.__tree = AVLTree()
        print("Set is empty now")

    def remove(self, val):
        """ Remove element from set """
        val = self._conversion(val)
        if isinstance(val, TYPES[self.__set_type]):
            self.__tree.delete(val)
        else:
            print("TypeError : Wrong Input")

    def contains(self, val):
        """ Return true or node if contains, else False or None """
        val = self._conversion(val)
        if isinstance(val, TYPES[self.__set_type]):
            return self.__tree.search(val)
        else:
            return str("TypeError : Wrong Input")

    def count(self):
        """ Get count of elements in set """
        return self.__tree.node_count

    def is_empty(self):
        """ Return true is not empty, else False """
        if self.__set_type is None:
            return None
        else:
            return True if self.__tree.node_count == 0 else False

    def _conversion(self, val):
        """ Convert value in needed type """
        if (self.__set_type == "str"):
            return val
        else:
            try:
                return ast.literal_eval(val)
            except ValueError:
                return None

    def _check_type(self, tree_type):
        if tree_type in TYPES.keys():
            return True
        else:
            print('TypeError : Wrong Type')
            return False
          