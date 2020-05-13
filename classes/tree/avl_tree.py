""" Module for elements in tree """
from modules.tree.node import Node

class AVLTree():
    """ Class of avl_tree. """
    def __init__(self):
        """ Initialization """
        self.__root = None
        self.__node_count = 0

    @property
    def node_count(self):
        """ Getter for _node_count """
        return self.__node_count

    def _set_root(self, val):
        """ Set the root value """
        self.__root = Node(val)

    def insert(self, val):
        """ Insert a val into AVLTree """
        if self.__root is None:
            self._set_root(val)
            self.__node_count += 1
        else:
            try:
                self._insert_node(self.__root, val)
                self.__node_count += 1
            except TypeError:
                print("TypeError. Use the same type of input that you chose before.")

    def _insert_node(self, current_node, val):
        """ Help 'def insert()' to insert a value into tree. """
        node_to_rebalance = None
        if current_node.value > val:
            if current_node.left:
                self._insert_node(current_node.left, val)
            else:
                new_node = Node(val)
                current_node.left = new_node
                new_node.parent = current_node
                if current_node.height == 0:
                    current_node.recompute_heights()
                    node = current_node
                    while node:
                        if node.balance_factor() in [-2, 2]:
                            node_to_rebalance = node
                            break
                        node = node.parent
        else:
            if current_node.right:
                self._insert_node(current_node.right, val)
            else:
                new_node = Node(val)
                current_node.right = new_node
                new_node.parent = current_node
                if current_node.height == 0:
                    current_node.recompute_heights()
                    node = current_node
                    while node:
                        if node.balance_factor() in [-2, 2]:
                            node_to_rebalance = node
                            break
                        node = node.parent
        if node_to_rebalance:
            self._rebalance(node_to_rebalance)
            
    def _rebalance(self, node_to_rebalance):
        """ Method for balance tree """
        if node_to_rebalance.balance_factor() == -2:
            if node_to_rebalance.right.balance_factor() <= 0:
                self._rrc(node_to_rebalance)
            else:
                self._rlc(node_to_rebalance)
        if node_to_rebalance.balance_factor() == +2:
            if node_to_rebalance.left.balance_factor() >= 0:
                self._llc(node_to_rebalance)
            else:
                self._lrc(node_to_rebalance)

    def _rrc(self, A):
        """ Right-right-case (single left rotation). """
        F = A.parent
        B = A.right
        A.right = B.left
        if A.right:
            A.right.parent = A
        B.left = A
        A.parent = B
        if F is None:
            self.__root = B
            self.__root.parent = None
        else:
            if F.right == A:
                F.right = B
            else:
                F.left = B
            B.parent = F
        A.recompute_heights()
        B.recompute_heights()

    def _rlc(self, A):
        """ Right-left-case (double left rotation). """
        F = A.parent
        B = A.right
        C = B.left
        B.left = C.right
        if B.left:
            B.left.parent = B
        A.right = C.left
        if A.right:
            A.right.parent = A
        C.right = B
        B.parent = C
        C.left = A
        A.parent = C
        if F is None:
            self.__root = C
            self.__root.parent = None
        else:
            if F.right == A:
                F.right = C
            else:
                F.left = C
            C.parent = F
        A.recompute_heights()
        B.recompute_heights()

    def _llc(self, A):
        """ Left-left-case (single right rotation). """
        F = A.parent
        B = A.left
        A.left = B.right
        if A.left:
            A.left.parent = A
        B.right = A
        A.parent = B
        if F is None:
            self.__root = B
            self.__root.parent = None
        else:
            if F.right == A:
                F.right = B
            else:
                F.left = B
            B.parent = F
        A.recompute_heights()
        B.recompute_heights()

    def _lrc(self, A):
        """ Left-right-case (double right rotation). """
        F = A.parent
        B = A.left
        C = B.right
        A.left = C.right
        if A.left:
            A.left.parent = A
        B.right = C.left
        if B.right:
            B.right.parent = B
        C.left = B
        B.parent = C
        C.right = A
        A.parent = C
        if F is None:
            self.__root = C
            self.__root.parent = None
        else:
            if F.right == A:
                F.right = C
            else:
                F.left = C
            C.parent = F
        A.recompute_heights()
        B.recompute_heights()

    def _search_for_delete(self, key):
        """ Search key for delete in the tree. """
        return self._search_node(self.__root, key, True)

    def search(self, key, return_node=False):
        """ Search key for delete in the tree. """
        return str(self._search_node(self.__root, key, True)) if return_node else self._search_node(self.__root, key)

    def _search_node(self, current_node, key, return_node=False):
        """ Help 'search' to find node """
        try:
            if current_node is None:
                return None if return_node else False
            elif current_node.value == key:
                return current_node if return_node else True
            elif current_node.value > key:
                return self._search_node(current_node.left, key, True) if return_node else self._search_node(current_node.left, key)
            else:
                return self._search_node(current_node.right, key, True) if return_node else self._search_node(current_node.right, key)
        except TypeError:
            return None if return_node else False

    def delete(self, key):
        """ Delete a node with a key """
        node = self._search_for_delete(key)
        if node is not None:
            self.__node_count -= 1
            if node.height == 0:
                self._remove_leaf(node)
            elif node.left and node.right:
                self._swap_and_remove(node)
            else:
                self._remove_branch(node)
        else:
            return False

    def _remove_leaf(self, node):
        """ If the node is a leaf.  Remove it and return. """
        parent = node.parent
        if parent:
            if parent.left == node:
                parent.left = None
            else:
                parent.right = None
            parent.recompute_heights()
        else:
            self.__root = None
        del node
        node = parent
        while node:
            if not node.balance_factor() in [-1, 0, 1]:
                self._rebalance(node)
            node = node.parent

    def _swap_and_remove(self, node):
        """
        If the node has two children. Swap items with the successor
        of the node (the smallest item in its right subtree) and
        delete the successor from the right subtree of the node.
        """
        successor = self._find_smallest(node.right)
        self._swap_nodes(node, successor)
        if node.height == 0:
            self._remove_leaf(node)
        else:
            self._remove_branch(node)

    def _find_smallest(self, start_node):
        """ Find the smallest item for _swap_and_remove """
        node = start_node
        while node.left:
            node = node.left
        return node

    def _swap_nodes(self, node1, node2):
        """ Swap nodes in _swap_and_remove """
        parent1 = node1.parent
        left_child1 = node1.left
        right_child1 = node1.right
        parent2 = node2.parent
        left_child2 = node2.left
        right_child2 = node2.right
        node1.height, node2.height = node2.height, node1.height
        if parent1:
            if parent1.left == node1:
                parent1.left = node2
            else:
                parent1.right = node2
            node2.parent = parent1
        else:
            self.__root = node2
            node2.parent = None
        node2.left = left_child1
        left_child1.parent = node2
        node1.left = left_child2
        if left_child2:
            left_child2.parent = node1
        node1.right = right_child2
        if right_child2:
            right_child2.parent = node1
        if not parent2 == node1:
            node2.right = right_child1
            right_child1.parent = node2
            parent2.left = node1
            node1.parent = parent2
        else:
            node2.right = node1
            node1.parent = node2

    def _remove_branch(self, node):
        """ Remove branch for _swap_and_remove() and delete() """
        parent = node.parent
        if parent:
            if parent.left == node:
                parent.left = (node.right if node.right else node.left)
            else:
                parent.right = (node.right if node.right else node.left)
            if node.left:
                node.left.parent = parent
            else:
                node.right.parent = parent
            parent.recompute_heights()
        else:
            if node.right:
                self.__root = node.right
                self.__root.parent = None
            if node.left:
                self.__root = node.left
                self.__root.parent = None
        self.__root.recompute_heights()
        del node
        node = parent
        while node:
            if not node.balance_factor() in [-1, 0, 1]:
                self._rebalance(node)
            node = node.parent

    def max(self, return_value=False):
        """ Output max value of tree, 'return_value = True' if you want get value : int"""
        try:
            node = self.__root
            while node.right:
                node = node.right
            return node.value if return_value else str(node.value)
        except AttributeError:
            return None if return_value else str("Tree is empty")

    def min(self, return_value=False):
        """ Output max value of tree, 'return_value = True' if you want get value : int"""
        try:
            node = self.__root
            while node.left:
                node = node.left
            return node.value if return_value else str(node.value)
        except AttributeError:
            return None if return_value else str("Tree is empty")
