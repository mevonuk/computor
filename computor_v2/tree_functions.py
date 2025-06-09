# functions to manipulate tree
# contains solve_node, sub_var_node, simplify_node

from variable import Variable
from tools import get_value2
from matrix import Matrix
from node import Node


def sub_var_node(node, variable):
    """Substitutes the value of a Variable into variable name"""
    if not isinstance(node, Node):
        return node
    
    # print("in sub_var_node", node, type(node), variable, type(variable))
    # print("in sub_var_node::", node.left, type(node.left))

    if isinstance(node.left, Variable) and node.left.name == variable.name:
        node.left = variable.value
    elif isinstance(node.left, str) and node.left == variable.name:
        node.left = variable.value
    elif isinstance(node.left, Node):
        sub_var_node(node.left, variable)

    if isinstance(node.right, Variable) and node.right.name == variable.name:
        node.right = variable.value
    elif isinstance(node.right, str) and node.right == variable.name:
        node.right = variable.value
    elif isinstance(node.left, Node):
        sub_var_node(node.right,variable)


def simplify_node(node, history):
    """Simplifies a node if possible"""
    left_value = node.left
    right_value = node.right
    print("simplify", left_value, right_value, node.type)
    if isinstance(node.left, Node):
        left_value = node.left.simplify_node(history)
    if isinstance(node.right, Node):
        right_value = node.right.simplify_node(history)
    if isinstance(node.left, str):
        left_value = get_value2(node.left, history)
    if isinstance(node.right, str):
        right_value = get_value2(node.right, history)
    if isinstance(node.left, Variable):
        left_value = get_value2(node.left.name, history)
    if isinstance(node.right, Variable):
        right_value = get_value2(node.right.name, history)

    print("in simplify node values:", left_value, right_value, node.type)

    if not (isinstance(node.right, Node) or isinstance(node.left, Node)) and not (isinstance(node.right, str) or isinstance(node.left, str)):
        if node.type == '+':
            return left_value + right_value
        if node.type == '-':
            return left_value - right_value
        if node.type == '*':
            return left_value * right_value
        if node.type == '/':
            return left_value / right_value
        if node.type == '%':
            return left_value % right_value
        if node.type == '^':
            return left_value ** right_value
        if node.type == '**':
            if isinstance(left_value, Matrix) and isinstance(right_value, Matrix):
                return right_value * left_value
            print("** can only be used with matrix multiplication")
            return None
    if node.type == 'FUNC':
        func = f"{node.left}"
        func = node.left
        if isinstance(func, str):
            return get_value2(func, history)
        return func
    return Node(left_value, right_value, node.type)
