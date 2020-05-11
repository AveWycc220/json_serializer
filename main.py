""" Module for using json_serializer """
from modules.json_serializer import JSONSerializer
from classes.example import Person

first = Person(1, "Jack")
second = Person(2, "Jill")
third = Person(3, "Aleks")
fourth = Person(4, "Gman")
first.children.append(second)
first.children.append(third)
third.children.append(fourth)
print(JSONSerializer.get_objects(first))