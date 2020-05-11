class Person():
    id_person = None
    name = None
    children = []
    last_work = ()
    job = None
    def __init__(self, id_person, name):
        self.id_person = id_person
        self.name = name
        self.children = []
        self.last_work = ()
