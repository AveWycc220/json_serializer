class Example():
    none_t = None
    int_t = 15
    float_t = 15.6
    list_t = list()
    set_t = None
    tuple_t = (16, 18, 19, 20)
    frozenset_t = frozenset()
    booleanT = True
    booleanF = False
    def __init__(self, value):
        self.int_t = value
        c = C(100)
        self.set_t = {c}
    @property
    def get_int(self):
        return self.int_t * 2
    def some_method(self):
        pass

class C():
    def __init__(self, value):
        self.value = value