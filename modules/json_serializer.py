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
            for i in range(len(class_object.__dir__())):
                if not class_object.__dir__()[i].startswith('__') and not class_object.__dir__()[i].endswith('__'):
                    default_objects = class_object.__dir__()[i]
                    if default_objects not in class_object.__dict__.keys():
                        objects[F'{default_objects}'] = class_object.__getattribute__(F'{default_objects}')
            for j, key in zip(objects.values(), objects.keys()):
                if re.search(r'classes.', str(j)):
                    if isinstance(objects[key], (list, tuple, set, frozenset)):
                        objects[key] = list(objects[key])
                        for i in range(len(j)):
                            objects[key][i] = (JSONSerializer.get_objects(j[i]))
                    else:
                        objects[key] = (JSONSerializer.get_objects(j))
            return objects
        else:
            print("Classes must be in folder : 'classes', else wrong input")
            
    @staticmethod
    def change_type(objects):
        """ Method for change wrong type of .json """
        if isinstance(objects, str):
            return objects.replace('None', 'null')
        for key in objects.keys():
            if isinstance(objects[key], (tuple, set, frozenset)):
                objects[key] = list(objects[key])
            if isinstance(objects[key], list):
                for i, _ in enumerate(objects[key]):
                    JSONSerializer.change_type(objects[key][i])
        return objects
