class Person():
    id_person = None
    name = None
    children = []
    def __init__(self, id_person, name):
        self.__id_person = id_person
        self.name = name
        self.children = []