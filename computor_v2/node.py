# defines Node class and how to print Nodes

from complex import Complex


class Node:
    """class for node object for making trees"""

    def __init__(self, left, right, type):
        """Initialize with the left and right side of node
        with the operator that relates them"""
        # left and right can be anything
        self.left = left
        self.right = right
        self.type = type

    def __str__(self):
        """Defines how to convert node to string"""
        ln = str(self.left)
        r = str(self.right)
        o = str(self.type)
        if isinstance(self.left, Complex) and self.left.imag != 0:
            ln = f"({ln})"
        if isinstance(self.right, Complex) and self.right.imag != 0:
            r = f"({r})"
        if isinstance(self.left, Node):
            ln = f"({ln})"
        if isinstance(self.right, Node):
            r = f"({r})"
        if self.type in set('+-') or self.type == '**':
            o = f" {self.type} "
        if self.type in set('*/%^'):
            o = f" {self.type} "
        if self.type == 'FUNC':
            return f"{ln}"
        if self.type == 'VAR':
            return f"{ln}"
        return ln + o + r
