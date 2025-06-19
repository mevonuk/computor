# functions to manipulate tree
# contains solve_node, simplify_node

from variable import Variable
from tools import get_value2
from matrix import Matrix
from node import Node
from function_tools import get_function_value


def solve_node(node: Node, history: dict):
    """Solves node using information saved in
    history dictionary as appropriate"""
    if not isinstance(node, Node):
        raise TypeError("only node can be solved in solve_node")
    
    # print("Entering solve_node")

    left_value = node.left
    right_value = node.right

    # print(left_value, type(left_value), right_value, type(right_value))

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

    # if isinstance(left_value, Variable):
    #     left_value = get_value2(left_value.name, history)
    # if isinstance(right_value, Variable):
    #     right_value = get_value2(right_value.name, history)

    # print(left_value, type(left_value), right_value, type(right_value))

    if left_value is not None and right_value is None:
        # if node.type != 'FUNC' and node.type != 'VAR':
        return left_value

    # if left_value is None or right_value is None:
    #     if node.type != 'FUNC' and node.type != 'VAR':
    #         # print("node: solve_node, None value", left_value, right_value, node.type)
    #         # print("Equation cannot be resolved")
    #         return None

    # if isinstance(left_value, str) or isinstance(right_value, str):
    #     # print("node: solve_node: string", left_value, right_value, node.type)
    #     return None

    if node.type == 'VAR' and right_value is None:
        return left_value

    if not isinstance(left_value, (str, Node)) and not isinstance(right_value, (str, Node)):
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
        if isinstance(left_value, Matrix):
            if isinstance(right_value, Matrix):
                return right_value * left_value
        print("** can only be used with matrix multiplication")
        return None
    if node.type == 'FUNC':
        function_name = node.left
        function_var = None
        if isinstance(node.right, Node):
            function_var = node.right.left
        else:
            function_var = node.right
        result = get_function_value(function_name, function_var, history)
        return result

    # print("Equation cannot be solved")
    return node


def solve_node_var(node: Node, var, history: dict):
    """Solves node using information saved in
    history dictionary as appropriate"""
    if not isinstance(node, Node):
        raise TypeError("only node can be solved in solve_node")

    # print("not solving var", var, var.left, var.right, type(var.left))

    left_value = node.left
    right_value = node.right
    if isinstance(node.left, Node):
        left_value = solve_node_var(node.left, var, history)
    if isinstance(node.right, Node):
        right_value = solve_node_var(node.right, var, history)
    if isinstance(node.left, str):
        if left_value == var:
            return None
        left_value = get_value2(node.left, history)
    if isinstance(node.right, str):
        if right_value == var:
            return None
        right_value = get_value2(node.right, history)
    if isinstance(node.left, Variable):
        if left_value.name == var:
            return None
        left_value = get_value2(node.left.name, history)
    if isinstance(node.right, Variable):
        if right_value.name == var:
            return None
        right_value = get_value2(node.right.name, history)

    if left_value is None or right_value is None:
        if node.type != 'FUNC' and node.type != 'VAR':
            # print(left_value, right_value, node.type)
            # print("Equation cannot be resolved")
            return None

    if isinstance(left_value, str) or isinstance(right_value, str):
        # print("node: solve_node: string", left_value, right_value, node.type)
        return None

    if node.type == 'VAR' and right_value is None:
        return left_value

    if node.type == '+':
        return left_value + right_value
    if node.type == '-':
        return left_value - right_value
    if node.type == '*':
        # print('here', left_value, right_value, type(left_value), type(right_value))
        return left_value * right_value
    if node.type == '/':
        return left_value / right_value
    if node.type == '%':
        return left_value % right_value
    if node.type == '^':
        return left_value ** right_value
    if node.type == '**':
        if isinstance(left_value, Matrix):
            if isinstance(right_value, Matrix):
                return right_value * left_value
        print("** can only be used with matrix multiplication")
        return None
    if node.type == 'FUNC':
        function_name = node.left
        function_var = node.right.left
        result = get_function_value(function_name, function_var, history)
        return result

    print("not caught in solve_node")
    return None
