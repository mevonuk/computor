# functions to manipulate tree
# contains sub_var_node, flatten_addition_chain,
#          rebuild_addition_chain, resolve, simplify_node

from variable import Variable
from matrix import Matrix
from node import Node
from rational import Rational
from complex import Complex

from tools import get_value2


def sub_var_node(node, variable):
    """Recursively replaces instances of a variable with its value."""
    if isinstance(node, Node):
        # Recursively replace in both left and right
        left = sub_var_node(node.left, variable)
        right = sub_var_node(node.right, variable)
        return Node(left, right, node.type)

    elif isinstance(node, Variable) and node.name == variable.name:
        return variable.value

    elif isinstance(node, str) and node == variable.name:
        return variable.value

    # Base case: return unchanged
    return node


def flatten_addition_chain(node):
    """Recursively flatten a node into a list of
    (term, sign) pairs where sign is +1 or -1"""
    terms = []

    def collect(n, sign=1):
        if isinstance(n, Node):
            if n.type == '+':
                collect(n.left, sign)
                collect(n.right, sign)
            elif n.type == '-':
                collect(n.left, sign)
                collect(n.right, -sign)
            else:
                terms.append((n, sign))
        elif isinstance(n, (int, float, Rational, Complex)):
            terms.append((n, sign))
        else:
            terms.append((n, sign))

    collect(node)
    return terms


def rebuild_addition_chain(terms):
    """Given flattened (term, sign) list, rebuild simplified node"""
    constants = 0
    symbolic = []

    for term, sign in terms:
        if isinstance(term, (int, float, Rational, Complex)):
            constants += sign * term
        else:
            symbolic.append((term, sign))

    # Start with constant, if any
    result = constants if constants != 0 else None

    for term, sign in symbolic:
        if result is None:
            result = term if sign == 1 else Node(0, term, '-')
        else:
            op = '+' if sign == 1 else '-'
            result = Node(result, term, op)

    if result is None:
        return 0  # Everything canceled out
    return result


def resolve(value, history):
    """Resolves a value recursively:
    simplifies Nodes, fetches Variables/strings"""
    if isinstance(value, Node):
        return simplify_node(value, history)
    if isinstance(value, Variable):
        val = get_value2(value.name, history)
    elif isinstance(value, str):
        val = get_value2(value, history)
    else:
        return value  # Already atomic

    if val is None or val == value:
        return value
    return resolve(val, history)


def simplify_node(node, history):
    """Recursively simplifies a node, combining constants where possible."""
    left = resolve(node.left, history)
    right = resolve(node.right, history)

    one = Rational(1)
    if node.type == '*':
        if right == one:
            return left

    # Case: both sides are fully numeric → evaluate
    if all(not isinstance(v, (str, Node, Variable)) for v in (left, right)):
        try:
            if node.type == '+':
                return left + right
            elif node.type == '-':
                return left - right
            elif node.type == '*':
                return left * right
            elif node.type == '/':
                return left / right
            elif node.type == '%':
                return left % right
            elif node.type == '^':
                return left ** right
            elif node.type == '**':
                if isinstance(left, Matrix) and isinstance(right, Matrix):
                    return right * left
                print("** can only be used with matrix multiplication")
                return None
        except Exception as e:
            # print("Error simplifying:", e)
            return Node(left, right, node.type)

    if node.type in ('+', '-'):
        flat_terms = flatten_addition_chain(node)
        return rebuild_addition_chain(flat_terms)

    ALLOWED = (int, float, Rational, Complex)

    # Case: simplify partial expressions
    if node.type == '+':
        # Collapse constants if one side is numeric
        if isinstance(left, ALLOWED) and isinstance(right, Node):
            right = simplify_node(right, history)
            if isinstance(right.left, ALLOWED) and right.type == '+':
                # e.g., 3 + (4 + a) → 7 + a
                new_left = left + right.left
                return Node(new_left, right.right, '+')
        if isinstance(right, ALLOWED) and isinstance(left, Node):
            left = simplify_node(left, history)
            if isinstance(left.left, ALLOWED) and left.type == '+':
                # e.g., (4 + a) + 3 → 7 + a
                new_left = left.left + right
                return Node(new_left, left.right, '+')

    if node.type == '-':
        if isinstance(left, ALLOWED) and isinstance(right, Node):
            right = simplify_node(right, history)
            if isinstance(right.left, ALLOWED) and right.type == '+':
                new_left = left - right.left
                return Node(new_left, right.right, '-')
        if isinstance(right, ALLOWED) and isinstance(left, Node):
            left = simplify_node(left, history)
            if isinstance(left.left, ALLOWED) and left.type == '+':
                new_left = left.left - right
                return Node(new_left, left.right, '+')  # Still addition

    # FUNC node simplification
    if node.type == 'FUNC':
        return resolve(node.left, history)

    return Node(left, right, node.type)
