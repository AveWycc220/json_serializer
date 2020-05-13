class Example():
    Null = None
    Int = 15
    Float = 15.6
    List = list()
    Set = set()
    Tuple = tuple()
    Frozenset = frozenset()
    BooleanT = True
    BooleanF = False
    @property
    def get_int(self):
        return self.Int * 2
    def some_method(self):
        pass