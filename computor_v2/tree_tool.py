# functions to manipulate tree
# contains solve_node, simplify_node

from variable import Variable
from matrix import Matrix
from node import Node

from tools import get_value2, power_node
from tree_functions import resolve


def resolve_matrix(input_matrix, history):
    """sub history values in matrix"""
    new_matrix = []
    for i in range(input_matrix.shape[0]):
        lst = []
        for k in range(input_matrix.shape[1]):
            value2 = resolve(input_matrix.data[i][k], history)
            lst.append(value2)
        new_matrix.append(lst)
    return Matrix(new_matrix)  # return matrix


def solve_node(node: Node, history: dict):
    """Solves node using information saved in
    history dictionary as appropriate"""
    if not isinstance(node, Node):
        raise TypeError("only node can be solved in solve_node")

    left_value = node.left
    right_value = node.right

    if isinstance(left_value, str):
        left_value = get_value2(left_value, history)
    if isinstance(right_value, str):
        right_value = get_value2(right_value, history)
    if isinstance(left_value, Variable):
        left_value = get_value2(left_value.name, history)
    if isinstance(right_value, Variable):
        right_value = get_value2(right_value.name, history)

    if isinstance(left_value, Node):
        left_value = solve_node(left_value, history)
    if isinstance(right_value, Node):
        right_value = solve_node(right_value, history)

    if left_value is not None and right_value is None:
        return left_value

    if node.type == 'VAR' and right_value is None:
        return left_value

    if isinstance(left_value, Matrix):
        left_value = resolve_matrix(left_value, history)
    if isinstance(right_value, Matrix):
        right_value = resolve_matrix(right_value, history)

    # if not isinstance(left_value, (str, Node))
    #     and not isinstance(right_value, (str, Node)):
    if all(
        not isinstance(v, (str, Node, Matrix))
        for v in (left_value, right_value)
    ):
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
            return power_node(left_value, right_value)

    elif isinstance(left_value, str) or isinstance(right_value, str):
        if node.type == '+':
            return Node(left_value, right_value, '+')
        if node.type == '-':
            return Node(left_value, right_value, '-')
        if node.type == '*':
            return left_value * right_value
        if node.type == '/':
            return left_value / right_value
        if node.type == '%':
            return Node(left_value, right_value, '%')
        if node.type == '^':
            return Node(left_value, right_value, '^')

    elif isinstance(left_value, Matrix) or isinstance(right_value, Matrix):
        if node.type == '+':
            return Node(left_value, right_value, '+')
        if node.type == '-':
            return Node(left_value, right_value, '-')
        if node.type == '*':
            return Node(left_value, right_value, '*')
        if node.type == '/':
            return Node(left_value, right_value, '/')
    else:
        if node.type == '+':
            return Node(left_value, right_value, '+')
        if node.type == '-':
            return Node(left_value, right_value, '-')
        if node.type == '*':
            return Node(left_value, right_value, '*')
        if node.type == '/':
            return Node(left_value, right_value, '/')
        if node.type == '%':
            return Node(left_value, right_value, '%')
        if node.type == '^':
            return Node(left_value, right_value, '^')

    if node.type == '**':
        if isinstance(left_value, Matrix):
            if isinstance(right_value, Matrix):
                return right_value * left_value
        print("** can only be used with matrix multiplication")
        return None

    return node
