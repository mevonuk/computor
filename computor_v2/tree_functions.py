# functions to manipulate tree
# contains solve_node, sub_var_node, simplify_node

from variable import Variable
from tools import get_value2
from matrix import Matrix
from node import Node


def solve_node(node: Node, history: dict):
    """Solves node using information saved in
    history dictionary as appropriate"""
    if not isinstance(node, Node):
        raise TypeError("only node can be solved in solve_node")

    left_value = node.left
    right_value = node.right
    if isinstance(node.left, Node):
        left_value = node.left.solve_node(history)
    if isinstance(node.right, Node):
        right_value = node.right.solve_node(history)
    if isinstance(node.left, str):
        left_value = get_value2(node.left, history)
    if isinstance(node.right, str):
        right_value = get_value2(node.right, history)
    if isinstance(node.left, Variable):
        left_value = get_value2(node.left.name, history)
    if isinstance(node.right, Variable):
        right_value = get_value2(node.right.name, history)

    if left_value is None or right_value is None:
        # print("node: solve_node, None value", left_value, right_value, senodelf.type)
        if node.type != 'FUNC' and node.type != 'VAR':
            print("Equation cannot be resolved")
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
        # func = node.left
        print("type is function", node.left, node.right)
        func = get_value2(node.left, history)
        print("function in history is", func)

        func_value = func.plug_vars(node.right, history)
        # func_value = plug_in_var(func_value, node.right, history)
        print("function value is", func_value)
        return None

    print("not caught in solve_node")
    return None


def sub_var_node(node, variable):
    """Substitutes the value of a Variable into variable name"""
    if isinstance(node.left, Variable) and node.left == variable:
        node.left = variable.value
    elif isinstance(node.left, str) and node.left == variable.name:
        node.left = variable.value
    elif isinstance(node.left, Node):
        sub_var_node(node.left, variable)

    if isinstance(node.right, Variable) and node.right == variable:
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
