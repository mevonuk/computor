# functions to manipulate tree
# contains solve_node, sub_var_node, simplify_node

from variable import Variable
from tools import get_value2
from matrix import Matrix
from node import Node
from rational import Rational
from complex import Complex


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


def is_atomic(val):
    return isinstance(val, (int, float, Rational, Complex))


def organize_node_constants_left(node):
    if not isinstance(node, Node):
        return node

    # Recursively process children
    left = organize_node_constants_left(node.left)
    right = organize_node_constants_left(node.right)

    # Build the new node
    new_node = Node(left, right, node.type)

    if node.type in ('+', '-'):
        # If right is constant and left is symbolic, swap them
        if not is_atomic(left) and is_atomic(right):
            new_node = Node(right, left, node.type)

        # If left is a node and its right is constant (e.g., (a + 3)), bubble the 3 up
        if isinstance(left, Node):
            l1, l2 = left.left, left.right
            if not is_atomic(l1) and is_atomic(l2):
                # e.g., (x + 3) → (3 + x)
                reordered_left = Node(l2, l1, left.type)
                new_node = Node(reordered_left, right, node.type)

        # Same for right subtree
        if isinstance(right, Node):
            r1, r2 = right.left, right.right
            if not is_atomic(r1) and is_atomic(r2):
                reordered_right = Node(r2, r1, right.type)
                new_node = Node(left, reordered_right, node.type)

    return new_node


def organize_node_constants_right(node):
    if not isinstance(node, Node):
        return node

    # Recursively process children
    left = organize_node_constants_right(node.left)
    right = organize_node_constants_right(node.right)

    # Rebuild the node
    new_node = Node(left, right, node.type)

    # Now normalize based on type
    if node.type in ('+', '-'):
        # If left is constant and right is symbolic, swap them
        if is_atomic(left) and not is_atomic(right):
            new_node = Node(right, left, node.type)

        # If left is a node and its left is constant, bubble it right
        if isinstance(left, Node):
            l1, l2 = left.left, left.right
            if is_atomic(l1) and not is_atomic(l2):
                # e.g., (3 + x) → (x + 3)
                reordered_left = Node(l2, l1, left.type)
                new_node = Node(reordered_left, right, node.type)

        # Similarly for right side
        if isinstance(right, Node):
            r1, r2 = right.left, right.right
            if is_atomic(r1) and not is_atomic(r2):
                reordered_right = Node(r2, r1, right.type)
                new_node = Node(left, reordered_right, node.type)

    return new_node

def flatten_addition_chain(node):
    """Recursively flatten a node into a list of (term, sign) pairs where sign is +1 or -1"""
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


def simplify_node(node, history):
    """Recursively simplifies a node, combining constants where possible."""

    def resolve(value):
        """Resolves a value recursively: simplifies Nodes, fetches Variables/strings"""
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
        return resolve(val)
    
    left = resolve(node.left)
    right = resolve(node.right)

    # Case: both sides are fully numeric → evaluate
    if not isinstance(left, (str, Node, Variable)) and not isinstance(right, (str, Node, Variable)):
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
            print("Error simplifying:", e)
            return Node(left, right, node.type)

    if node.type in ('+', '-'):
        flat_terms = flatten_addition_chain(node)
        return rebuild_addition_chain(flat_terms)

    # Case: simplify partial expressions
    if node.type == '+':
        # Collapse constants if one side is numeric
        if isinstance(left, (int, float, Rational, Complex)) and isinstance(right, Node):
            right = simplify_node(right, history)
            if isinstance(right.left, (int, float, Rational, Complex)) and right.type == '+':
                # e.g., 3 + (4 + a) → 7 + a
                new_left = left + right.left
                return Node(new_left, right.right, '+')
        if isinstance(right, (int, float, Rational, Complex)) and isinstance(left, Node):
            left = simplify_node(left, history)
            if isinstance(left.left, (int, float, Rational, Complex)) and left.type == '+':
                # e.g., (4 + a) + 3 → 7 + a
                new_left = left.left + right
                return Node(new_left, left.right, '+')

    if node.type == '-':
        if isinstance(left, (int, float, Rational, Complex)) and isinstance(right, Node):
            right = simplify_node(right, history)
            if isinstance(right.left, (int, float, Rational, Complex)) and right.type == '+':
                new_left = left - right.left
                return Node(new_left, right.right, '-')
        if isinstance(right, (int, float, Rational, Complex)) and isinstance(left, Node):
            left = simplify_node(left, history)
            if isinstance(left.left, (int, float, Rational, Complex)) and left.type == '+':
                new_left = left.left - right
                return Node(new_left, left.right, '+')  # Still addition


    # FUNC node simplification
    if node.type == 'FUNC':
        return resolve(node.left)

    return Node(left, right, node.type)

def simplify_node_still_no(node, history):
    """Recursively simplifies a node, resolving variables and evaluating expressions."""

    def resolve(value):
        """Resolves a value recursively: simplifies Nodes, fetches Variables/strings"""
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
        return resolve(val)

    # Step 1: Recursively simplify children first
    left_value = resolve(node.left)
    right_value = resolve(node.right)

    # Step 2: Try to fully simplify if both sides are atomic
    if not isinstance(left_value, (str, Node, Variable)) and not isinstance(right_value, (str, Node, Variable)):
        try:
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
        except Exception as e:
            print(f"Error during simplification: {e}")
            return Node(left_value, right_value, node.type)

    # Step 3: Combine constants within a Node structure, e.g. (-1 + (a * a)) → ((a * a) - 1)
    if node.type == '+' and isinstance(left_value, (int, float)) and isinstance(right_value, Node):
        if isinstance(right_value.left, (int, float)):
            # Constant folding: left + (c + rest) → (left + c) + rest
            folded = left_value + right_value.left
            return simplify_node(Node(folded, right_value.right, right_value.type), history)
    if node.type == '+' and isinstance(right_value, (int, float)) and isinstance(left_value, Node):
        if isinstance(left_value.left, (int, float)):
            folded = right_value + left_value.left
            return simplify_node(Node(folded, left_value.right, left_value.type), history)

    if node.type == '-' and isinstance(left_value, Node) and isinstance(right_value, (int, float)):
        # (left - const) where left is a Node like -1 + (a * a)
        simplified_left = simplify_node(left_value, history)
        if isinstance(simplified_left.left, (int, float)):
            if simplified_left.type == '+':
                # Convert (-1 + (a * a)) - 4 → (a * a) - 5
                folded = simplified_left.left - right_value
                return simplify_node(Node(folded, simplified_left.right, '+'), history)

    # Otherwise return partially simplified node
    return Node(left_value, right_value, node.type)

def simplify_node_no(node, history):
    """Recursively simplifies a node, resolving variables and evaluating expressions."""

    def resolve(value):
        """Resolves a value recursively: simplifies Nodes, fetches Variables/strings"""
        if isinstance(value, Node):
            return simplify_node(value, history)
        if isinstance(value, Variable):
            val = get_value2(value.name, history)
        elif isinstance(value, str):
            val = get_value2(value, history)
        else:
            return value  # Already atomic

        # Recurse until it becomes atomic or cannot be resolved
        if val is None or val == value:
            return value
        return resolve(val)

    # Resolve left and right
    left_value = resolve(node.left)
    right_value = resolve(node.right)

    # Try to evaluate if both are atomic
    if not isinstance(left_value, (str, Node, Variable)) and not isinstance(right_value, (str, Node, Variable)):
        try:
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
        except Exception as e:
            print(f"Error during simplification: {e}")
            return Node(left_value, right_value, node.type)

    # If one side is fully simplified but the other isn't, simplify what we can
    # For operations like: (-1 + (a * a)) - 4, this handles -1 - 4
    if node.type in {'+', '-'}:
        if isinstance(left_value, (int, float)) and isinstance(right_value, Node):
            simplified_right = simplify_node(right_value, history)
            return Node(left_value, simplified_right, node.type)
        if isinstance(right_value, (int, float)) and isinstance(left_value, Node):
            simplified_left = simplify_node(left_value, history)
            return Node(simplified_left, right_value, node.type)

    # Return simplified node
    return Node(left_value, right_value, node.type)

def simplify_node2(node, history):
    """Recursively simplifies a node, resolving variables and evaluating expressions"""

    def resolve(value):
        """Resolves a value recursively: simplifies Nodes, fetches Variables/strings"""
        # Recursively simplify nested Nodes
        if isinstance(value, Node):
            return simplify_node(value, history)
        
        # Resolve Variable or string to its value
        if isinstance(value, Variable):
            val = get_value2(value.name, history)
        elif isinstance(value, str):
            val = get_value2(value, history)
        else:
            return value  # Already a number, matrix, etc.

        if val is None or val == value:
            return value

        # Catch the case where get_value2 returns a Node or Variable again
        return resolve(val)  # Recurse until atomic (int, float, Matrix, etc.)

    # Recursively resolve both sides
    # print("in simplify node:", node, type(node))
    left_value = resolve(node.left)
    right_value = resolve(node.right)

    # If both sides are now atomic (no longer Node or str or Variable), try simplifying
    if not isinstance(left_value, (str, Node, Variable)) and not isinstance(right_value, (str, Node, Variable)):
        try:
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
        except Exception as e:
            print(f"Error during simplification: {e}")
            return Node(left_value, right_value, node.type)

    # Handle special function or variable node types
    if node.type == 'FUNC':
        func = resolve(node.left)
        return func

    # Return simplified node if we couldn't fully evaluate
    return Node(left_value, right_value, node.type)

