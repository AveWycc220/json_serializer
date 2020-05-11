""" Module for json-serializer """
import re

class JSONSerializer():
    """ Class of json-serializer """
    @staticmethod
    def get_objects(class_object):
        """
        Method for getting objects in class
        Classes must be in folder : 'classes'
        """
        class_type = str(type(class_object))
        if re.search(r'classes.', class_type):
            objects = dict()
            objects.update(class_object.__dict__)
            for j, key in zip(objects.values(), objects.keys()):
                if re.search(r'classes.', str(j)):
                    for i in range(len(j)):
                        objects[key][i] = (JSONSerializer.get_objects(j[i]))
            return objects
        else:
            print("Classes must be in folder : 'classes', else wrong input")

    