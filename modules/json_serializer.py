""" Module for json-serializer """
import re
import os
import random

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
class JSONSerializer():
    """ Class of json-serializer """
    @staticmethod
    def __get_objects(class_object):
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
                            objects[key][i] = (JSONSerializer.__get_objects(j[i]))
                    else:
                        objects[key] = (JSONSerializer.__get_objects(j))
            return objects
        else:
            print("Classes must be in folder : 'classes', else wrong input")

    @staticmethod
    def __change_type(objects):
        """ Method for change wrong type of .json """
        for key in objects.keys():
            if isinstance(objects[key], (tuple, set, frozenset)):
                objects[key] = list(objects[key])
            if isinstance(objects[key], list):
                for i, _ in enumerate(objects[key]):
                    JSONSerializer.__change_type(objects[key][i])
        return objects

    @staticmethod
    def serialize(class_object, file_name=None):
        """ Method for output objects in .json """
        objects = JSONSerializer.__get_objects(class_object)
        objects = JSONSerializer.__change_type(objects)
        objects = JSONSerializer.__to_str(objects)
        JSONSerializer.__output(class_object, objects, file_name)
        return objects

    @staticmethod
    def __output(class_object, objects, file_name):
        """  Output in .json file """
        fix = random.randint(0, 10000000)
        if file_name:
            if str(file_name) + '.json'\
            in os.listdir(path=rf'f:\Projects\json_serializer\output'):
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{file_name}{fix}.json')
            else:
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{file_name}.json')
        else:
            if str(class_object.__class__.__name__) + str(id(class_object)) + '.json'\
            in os.listdir(path=rf'f:\Projects\json_serializer\output'):
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{class_object.__class__.__name__}{id(class_object)}{fix}.json')
            else:
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{class_object.__class__.__name__}{id(class_object)}.json')
        file = open(r'{}'.format(my_file), 'w')
        file.write(objects)
        if file_name:
            print(F'File {file_name}{fix}.json created.')
        else:
            print(F'File {class_object.__class__.__name__}{id(class_object)}{fix}.json created.')
        file = file.close

    @staticmethod
    def __to_str(objects):
        """ Method for conversion to string """
        objects_str = str(objects)
        objects_str = objects_str.replace("'", '"')
        objects_str = objects_str.replace('None', 'null')
        objects_str = objects_str.replace(', ', ',')
        objects_str = JSONSerializer.__dict_str(objects_str)
        return objects_str

    @staticmethod
    def __dict_str(objects_str):
        """ Help __to_str to convert dictionary using recursion" """
        count = 0
        count_object = 0
        count_array = 0
        temp_count = 0
        for i, _ in enumerate(objects_str):
            if _ == '{':
                objects_str = objects_str[0:i+count] + count_array * '  ' + '{\n\t'  + count_object*'\t'\
                + objects_str[i+1+count: len(objects_str)]
                count += 2 + (count_object * 1) + (count_array * 2)
                count_object += 1
            if _ == '}':
                count_object -= 1
                objects_str = objects_str[0:i+count] +  '\n' + count_object*'\t' + count_array * '  ' + '}'\
                + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1) +  (count_array * 2)
            if _ == ',':
                objects_str = objects_str[0:i+count] + ',\n' + count_object*'\t' + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1)
            if _ == '{' and objects_str[i+1] == '[':
                objects_str = objects_str[0:i+count] + count_object*'\t' + '\n{' + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1)
            if _ == '[' and objects_str[i+count+1] != ']':
                objects_str = objects_str[0:i+count] + '[\n' + count_object*'\t' + objects_str[i+1+count: len(objects_str)]
                if count_array != 1:
                    count_array += 1
                else:
                    temp_count += 1
                count += 1 + (count_object * 1)
            if _ == ']' and objects_str[i+count-1] != '[':
                if count_array == 1 and temp_count == 0:
                    count_array -= 1
                else:
                    temp_count -= 1
                objects_str = objects_str[0:i+count] + '\n' + count_object*'\t' +']' + count_array*'  '\
                + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1) + (count_array * 2)
        return objects_str