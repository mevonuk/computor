# Contains Tree class based on Node class
# with functions to simplify node and sub a variable into a node

from matrix import Matrix
from variable import Variable
from tools import get_value2
from node import Node


class Tree(Node):
    """child of Node class"""

    def sub_var_node(self, variable):
        """Substitutes the value of a Variable into variable name"""
        if isinstance(self.left, Variable) and self.left == variable:
            self.left = variable.value
        elif isinstance(self.left, str) and self.left == variable.name:
            self.left = variable.value
        elif isinstance(self.left, Node):
            self.left.sub_var_node(variable)

        if isinstance(self.right, Variable) and self.right == variable:
            self.right = variable.value
        elif isinstance(self.right, str) and self.right == variable.name:
            self.right = variable.value
        elif isinstance(self.left, Node):
            self.right.sub_var_node(variable)

    def simplify_node(self, history):
        """Simplifies a node if possible"""
        left_value = self.left
        right_value = self.right
        print("simplify", left_value, right_value, self.type)
        if isinstance(self.left, Node):
            left_value = self.left.simplify_node(history)
        if isinstance(self.right, Node):
            right_value = self.right.simplify_node(history)
        if isinstance(self.left, str):
            left_value = get_value2(self.left, history)
        if isinstance(self.right, str):
            right_value = get_value2(self.right, history)
        if isinstance(self.left, Variable):
            left_value = get_value2(self.left.name, history)
        if isinstance(self.right, Variable):
            right_value = get_value2(self.right.name, history)

        print("in simplify node values:", left_value, right_value, self.type)

        if not (isinstance(self.right, Node) or isinstance(self.left, Node)) and not (isinstance(self.right, str) or isinstance(self.left, str)):
            if self.type == '+':
                return left_value + right_value
            if self.type == '-':
                return left_value - right_value
            if self.type == '*':
                return left_value * right_value
            if self.type == '/':
                return left_value / right_value
            if self.type == '%':
                return left_value % right_value
            if self.type == '^':
                return left_value ** right_value
            if self.type == '**':
                if isinstance(left_value, Matrix) and isinstance(right_value, Matrix):
                    return right_value * left_value
                print("** can only be used with matrix multiplication")
                return None
        if self.type == 'FUNC':
            func = f"{self.left}"
            func = self.left
            if isinstance(func, str):
                return get_value2(func, history)
            return func
        return Node(left_value, right_value, self.type)
