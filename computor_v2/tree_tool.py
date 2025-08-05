# functions to manipulate tree
# contains solve_node, simplify_node

from variable import Variable
from matrix import Matrix
from node import Node

from tools import get_value2, power_node


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

    # if not isinstance(left_value, (str, Node))
    #     and not isinstance(right_value, (str, Node)):
    if all(not isinstance(v, (str, Node)) for v in (left_value, right_value)):
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
    if node.type == '**':
        if isinstance(left_value, Matrix):
            if isinstance(right_value, Matrix):
                return right_value * left_value
        print("** can only be used with matrix multiplication")
        return None
    # if node.type == 'FUNC':
    #     function_name = node.left
    #     function_var = None
    #     if isinstance(node.right, Node):
    #         function_var = node.right.left
    #     else:
    #         function_var = node.right
    #     result = get_function_value(function_name, function_var, history)
    #     return result

    return node
