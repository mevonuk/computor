from rational import Rational
from complex import Complex
from matrix import Matrix, Vector
from variable import Variable

def get_value(value, history):
    if value in history:
        result = history[value]
        if isinstance(result, str):
            result = get_value(result, history)
        return result
    print("Variable " + value + " is not defined")
    return None

class Node:

    def __init__(self, left, right, type):
        # left and right can be anything, op defines how they relate to each other
        self.left = left
        self.right = right
        self.type = type

    def __str__(self):
        l = str(self.left)
        r = str(self.right)
        if isinstance(self.left, Complex) and self.left.imag != 0:
            l = f"({l})"
        if isinstance(self.right, Complex) and self.right.imag != 0:
            r = f"({r})"
        if isinstance(self.left, Node):
            l = f"({l})"
        if isinstance(self.right, Node):
            r = f"({r})"
        if self.type in set('+-*/%^') or self.type == '**':
            o = f" {self.type} "
        return l + o + r
    
    def sub_var_node(self, variable):
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


    def solve_node(self, history):
        left_value = self.left
        right_value = self.right
        if isinstance(self.left, Node):
            left_value = self.left.solve_node(history)
        if isinstance(self.right, Node):
            right_value = self.right.solve_node(history)
        if isinstance(self.left, str):
            left_value = get_value(self.left, history)
        if isinstance(self.right, str):
            right_value = get_value(self.right, history)

        if left_value == None or right_value == None:
            print("Equation cannot be resolved")
            return None

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
            return None
        

# r = Rational(2)
# var = Variable('a', r)
# var.print_value()

# n1 = Node('b',r,'+')
# print(n1)

# n1.sub_var_node(var)


# c = Complex(3,5)
# r = Rational(2)
# m = Matrix([[3,4],[4,3]])

# v = Vector([[3,4]])
# print(v)

# n1 = Node(0,0,'+')
# print(n1)

# history = {}
# history['a'] = c
# history['c'] = 'a'

# n2 = Node(v.T(),m,'**')

# print("Solving... " + str(n2) + " =")

# print(n2.solve_node(history))