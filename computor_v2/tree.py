from complex import Complex
from matrix import Matrix
from variable import Variable

def get_value(value, history):
    if value in history:
        result = history[value]
        if isinstance(result, str):
            result = get_value(result, history)
        return result
    print(value + " is not defined")
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
        o = str(self.type)
        if isinstance(self.left, Complex) and self.left.imag != 0:
            l = f"({l})"
        if isinstance(self.right, Complex) and self.right.imag != 0:
            r = f"({r})"
        if isinstance(self.left, Node):
            l = f"({l})"
        if isinstance(self.right, Node):
            r = f"({r})"
        if self.type in set('+-') or self.type == '**':
            o = f" {self.type} "
        if self.type in set('*/%^'):
            o = f"{self.type}"
        if self.type == 'FUNC':
            return f"{l}"
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

        if (left_value == None or right_value == None) and self.type != 'FUNC' :
            #print("Equation cannot be resolved")
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
        if self.type == 'FUNC':
            func = f"{self.left}"
            func = self.left
            return get_value(func, history)
            







# class Tree:

#     def __init__(self, data):
#         self.left = None
#         self.right = None
#         self.data = data

#     def print_tree(self):
#         if self.left:
#             self.left.print_tree()
#         print(self.data)
#         if self.right:
#             self.right.print_tree()

#     def insert_left(self,data):
#         if self.data:
#             if self.left is None:
#                 self.left = Tree(data)
#             else:
#                 self.left.insert_left(data)
#         else:
#             self.data = data

#     def insert_right(self,data):
#         if self.data:
#             if self.right is None:
#                 self.right = Tree(data)
#             else:
#                 self.right.insert_right(data)
#         else:
#             self.data = data

# list = ['(','4.5', '+', '5',')']
# list = ['4.5', '+', '5']

# stack = []
# tree = Tree('')
# currenttree = tree
# stack.append(tree)

# for l in list:
#     print(l)
#     if l == '(':
#         currenttree.insert_left('')
#         stack.append(currenttree)
#         currenttree = currenttree.left
#     elif l in ('+_*/'):
#         currenttree.data = l
#         currenttree.insert_right('')
#         stack.append(currenttree)
#         currenttree = currenttree.right
#     elif l == ')':
#         currenttree = stack.pop()
#     elif l not in ('+-*/)'):
#         try:
#             currenttree.data = float(l)
#             parent = stack.pop()
#             currenttree = parent
#         except ValueError:
#             raise ValueError("token is not valid", l)
        
# tree.print_tree()

    


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