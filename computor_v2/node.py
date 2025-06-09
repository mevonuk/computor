from complex import Complex
from variable import Variable
from tools import get_value2
from matrix import Matrix


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
            o = f"{self.type}"
        if self.type == 'FUNC':
            return f"{ln}"
        if self.type == 'VAR':
            return f"{ln}"
        return ln + o + r

    # problem here !!! because solve node calls circularly for things
    # when self.type is 'FUNC'
    def solve_node(self, history):
        """Solves node using information saved in
        history dictionary as appropriate"""
        left_value = self.left
        right_value = self.right
        if isinstance(self.left, Node):
            left_value = self.left.solve_node(history)
        if isinstance(self.right, Node):
            right_value = self.right.solve_node(history)
        if isinstance(self.left, str):
            left_value = get_value2(self.left, history)
        if isinstance(self.right, str):
            right_value = get_value2(self.right, history)
        if isinstance(self.left, Variable):
            left_value = get_value2(self.left.name, history)
        if isinstance(self.right, Variable):
            right_value = get_value2(self.right.name, history)

        if left_value is None or right_value is None:
            # print("node: solve_node, None value", left_value, right_value, self.type)
            if self.type != 'FUNC' and self.type != 'VAR':
                print("Equation cannot be resolved")
                return None

        if isinstance(left_value, str) or isinstance(right_value, str):
            # print("node: solve_node: string", left_value, right_value, self.type)
            return None

        if self.type == 'VAR' and right_value is None:
            return left_value

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
            if isinstance(left_value, Matrix):
                if isinstance(right_value, Matrix):
                    return right_value * left_value
            print("** can only be used with matrix multiplication")
            return None
        if self.type == 'FUNC':
            # func = self.left
            print("type is function", self.left, self.right)
            func = get_value2(self.left, history)
            print("function in history is", func)

            func_value = func.plug_vars(self.right, history)
            # func_value = plug_in_var(func_value, self.right, history)
            print("function value is", func_value)
            return None

        print("not caught in solve_node")
        return None
