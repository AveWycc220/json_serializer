""" Module for json-serializer """
import re
import os
import random

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
class JSONSerializer():
    """ Class of json-serializer """

    @staticmethod
    def serialize(class_object, file_name=None):
        """ Method for output objects in .json """
        objects = JSONSerializer.__get_objects(class_object)
        objects = JSONSerializer.__change_type(objects)
        objects = JSONSerializer.__to_str(objects)
        JSONSerializer.__output(class_object, objects, file_name)
        return objects

    @staticmethod
    def __get_objects(class_object, id_last_objects=None):
        """
        Method for getting objects in class
        Classes must be in folder : 'classes'
        """
        class_type = str(type(class_object))
        if re.search(r'classes.', class_type):
            objects = dict()
            objects.update(class_object.__dict__)
            for i in range(len(class_object.__dir__())):
                if not class_object.__dir__()[i].startswith('__'):
                    default_objects = class_object.__dir__()[i]
                    if default_objects not in class_object.__dict__.keys() and\
                    not str(class_object.__getattribute__(F'{default_objects}')).startswith('<bound method'):
                        objects[F'{default_objects}'] = class_object.__getattribute__(F'{default_objects}')
            for j, key in zip(objects.values(), objects.keys()):
                if bool(re.search(r'classes.', str(j))) or bool(re.search(r'classes.', str(type(j)))):
                    if isinstance(objects[key], (list, tuple, set, frozenset)):
                        objects[key] = list(objects[key])
                        j = list(j)
                        for i in range(len(objects[key])):
                            if id(j) != id_last_objects:
                                objects[key][i] = (JSONSerializer.__get_objects(j[i]))
                            else:
                                last_object_dict = list(j[i].__dict__)
                                objects[key][i] = F'Object with {last_object_dict[0]} : {j.__dict__[last_object_dict[0]]}'
                    else:
                        if id(j) != id_last_objects:
                            objects[key] = (JSONSerializer.__get_objects(j, id(class_object)))
                        else:
                            last_object_dict = list(j.__dict__)
                            objects[key] = F'Object with {last_object_dict[0]} : {j.__dict__[last_object_dict[0]]}'
            return objects
        else:
            print("Classes must be in folder : 'classes', else wrong input")

    @staticmethod
    def __change_type(objects):
        """ Method for change wrong type of .json """
        for key in objects.keys():
            if isinstance(objects[key], (tuple, set, frozenset)):
                objects[key] = list(objects[key])
            if isinstance(objects[key], list) and bool(re.search(r'classes.', str(objects[key]))):
                for i, _ in enumerate(objects[key]):
                    JSONSerializer.__change_type(objects[key][i])
        return objects

    @staticmethod
    def __output(class_object, objects, file_name):
        """  Output in .json file """
        fix = random.randint(0, 10000000)
        if file_name:
            file_exists = str(file_name) + '.json' in os.listdir(path=rf'{THIS_FOLDER}\..\output')
        else:
            file_exists = str(class_object.__class__.__name__) + str(id(class_object)) + '.json'\
            in os.listdir(path=rf'{THIS_FOLDER}\..\output')
        if file_name:
            if file_exists:
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{file_name}{fix}.json')
            else:
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{file_name}.json')
        else:
            if file_exists:
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{class_object.__class__.__name__}{id(class_object)}{fix}.json')
            else:
                my_file = os.path.join(THIS_FOLDER,\
                rf'..\output\{class_object.__class__.__name__}{id(class_object)}.json')
        file = open(r'{}'.format(my_file), 'w')
        if file_name:
            if file_exists:
                print(F'File {file_name}{fix}.json created.')
            else:
                if str(file_name) + '.json' in os.listdir(path=rf'{THIS_FOLDER}\..\output'):
                    print(F'File {file_name}.json created.')
                else: 
                    print(F'File {file_name}.json NOT created.')
        else:
            if file_exists:
                print(F'File {class_object.__class__.__name__}{id(class_object)}{fix}.json created.')
            else:
                if str(class_object.__class__.__name__) + str(id(class_object)) + '.json'\
                in os.listdir(path=rf'{THIS_FOLDER}\..\output'):
                    print(F'File {class_object.__class__.__name__}{id(class_object)}.json created.')
                else:
                    print(F'File {class_object.__class__.__name__}{id(class_object)}.json NOT created.')
        file.write(objects)
        file = file.close()

    @staticmethod
    def __to_str(objects):
        """ Method for conversion to string """
        objects_str = str(objects)
        objects_str = objects_str.replace("'", '"')
        objects_str = objects_str.replace('None', 'null')
        objects_str = objects_str.replace(', ', ',')
        objects_str = objects_str.replace('True', 'true')
        objects_str = objects_str.replace('False', 'false')
        objects_str = JSONSerializer.__dict_str(objects_str)
        return objects_str

    @staticmethod
    def __dict_str(objects_str):
        """ Help __to_str to convert dictionary """
        count = 0
        count_object = 0
        count_array = 0
        temp_count = 0
        for i, item in enumerate(objects_str):
            if item == '{':
                objects_str = objects_str[0:i+count] + count_array * '  ' + '{\n\t'  + count_object*'\t'\
                + objects_str[i+1+count: len(objects_str)]
                count += 2 + (count_object * 1) + (count_array * 2)
                count_object += 1
            if item == '}':
                count_object -= 1
                objects_str = objects_str[0:i+count] +  '\n' + count_object*'\t' + count_array * '  ' + '}'\
                + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1) +  (count_array * 2)
            if item == ',':
                objects_str = objects_str[0:i+count] + ',\n' + count_object*'\t' + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1)
            if item == '{' and objects_str[i+1] == '[':
                objects_str = objects_str[0:i+count] + count_object*'\t' + '\n{' + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1)
            if item == '[' and objects_str[i+count+1] != ']':
                objects_str = objects_str[0:i+count] + '[\n' + count_object*'\t' + objects_str[i+1+count: len(objects_str)]
                if count_array != 1:
                    count_array += 1
                else:
                    temp_count += 1
                count += 1 + (count_object * 1)
            if item == ']' and objects_str[i+count-1] != '[':
                if count_array == 1 and temp_count == 0:
                    count_array -= 1
                else:
                    temp_count -= 1
                objects_str = objects_str[0:i+count] + '\n' + count_object*'\t' +']' + count_array*'  '\
                + objects_str[i+1+count: len(objects_str)]
                count += 1 + (count_object * 1) + (count_array * 2)
        return objects_str