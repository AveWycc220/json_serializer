""" Module for using json_serializer """
import json
from modules.json_serializer import JSONSerializer
from classes.example import Person
from classes.set import Set

#Example
first = Person(1, "Jack")
second = Person(2, "Jill")
third = Person(3, "Aleks")
first.id_person = second
first.children.append(second)
first.children.append(third)
print(first.__class__)
JSONSerializer.serialize(first, 'Jack')
# Check : Example
with open(r'output\Aleks.json') as f:
    templates = json.load(f)
print(templates)
f = f.close()
print(type(templates))
#Set
set_on_avl_tree = Set('int')
set_on_avl_tree.add('15')
set_on_avl_tree.add('167')
set_on_avl_tree.add('4')
set_on_avl_tree.add('200')
JSONSerializer.serialize(set_on_avl_tree, 'Set')