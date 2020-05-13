""" Module for elements in tree """


class Node():
    """ Class for elements in tree """
    def __init__(self, value=None):
        """ Initialization """
        self.value = value
        self.parent = None
        self.right = None
        self.left = None
        self.height = 0

    def max_children_height(self):
        """ Return max height of subtrees """
        if self.left and self.right:
            return max(self.left.height, self.right.height)
        elif self.left and not self.right:
            return self.left.height
        elif not self.left and self.right:
            return self.right.height
        else:
            return -1

    def balance_factor(self):
        """ Balance Factor - calculate the height difference between the right and left subtrees """
        return (self.left.height if self.left else -1) - (self.right.height if self.right else -1)

    def recompute_heights(self):
        """ Change height of elements after operation """
        changed = True
        node = self
        while node and changed:
            old_height = node.height
            node.height = (node.max_children_height() + 1 if (node.right or node.left) else 0)
            changed = node.height != old_height
            node = node.parent

    def __str__(self):
        """ Output information """
        return F"Node(Value: {self.value}, Height: {self.height},\
 Right: {self.right.value if self.right else None},\
 Parent: {self.parent.value if self.parent else None},\
 Left: {self.left.value if self.left else None})"
