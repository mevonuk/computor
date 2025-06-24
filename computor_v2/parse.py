# contains: split_at_equals, define_function_terms, define_function, parse_cmd

from rational import Rational
from variable import Variable
from polynomial import Polynomial, RationalExpression
from function import Function
from node import Node

from polynomial import sub_exprs
from lex_base import tokenize, parse_tokens
from lex_base import extract_matrix_literal, parse_matrix_literal
from lexer import parse_expression, parse_num
from tools import get_value, get_value2
from my_math_tools import quadratic
from check_input import check_user_input
from tree_functions2 import solve_node
from tree_functions import simplify_node, resolve
from function_tools import get_function_value
from lexer2 import parse_expression2


def split_at_equals(tokens: str):
    """Splits string at the equal sign into left and right parts"""
    if '=' in tokens:
        idx = tokens.index('=')
        left = tokens[:idx]
        right = tokens[idx + 1:]
        return left, right
    else:
        raise ValueError("'=' not found in token list")


def define_function_terms(name, var, term, history):
    """Define function terms and return RHS of function
    in terms of a polynomial or rational function"""
    if isinstance(var, Node):
        safe_var = var.left.name
    elif isinstance(var, Variable):
        safe_var = var.name
    else:
        safe_var = var
    terms, _ = parse_expression2(term, safe_var, history)
    value = Function(name, var, terms)
    poly = value.convert_function()
    value = poly
    if isinstance(poly, RationalExpression):
        simplify = poly.simplify()
        value = simplify
    if isinstance(value, (Polynomial, RationalExpression)):
        value.combine_like_terms()
    return value


def define_function(func, history):
    """parses tokens of function definition and returns the
    fuction name as key, and the function expression as value"""
    var, _ = parse_expression(func[0][2])
    key = func[0][1]
    value = define_function_terms(func[0][1], var, func[2:], history)
    return key, value


def parse_cmd(cmd, history):
    """Main parsing control, checks input and funnels workflow"""
    if not isinstance(cmd, str):
        print("Error: Bad input to parcer, not a string")
        return None, None

    cmd = cmd.lower()
    if check_user_input(cmd) == 1:
        return None, None

    key = None
    value = None

    tokens = tokenize(cmd)
    func = parse_tokens(tokens)

    # is a function being defined?
    func_def = 0
    if func and func[0] and func[0][0] == 'FUNC' and func[1] == '=':
        func_def = 1

    # does the input end with a question mark?
    solve = 0
    if tokens[len(tokens) - 1] == '?':
        solve = 1
        # remove '?'
        end = len(tokens)-1
        tokens = tokens[:end]

    # solving, not FUNC
    if solve == 1 and func_def == 0:

        # case 1: ending with =
        if tokens[len(tokens)-1] == '=':
            # remove =
            end = len(tokens)-1
            tokens = tokens[:end]
            tokens = parse_tokens(tokens)

            tree, _ = parse_expression(tokens)
            # recursive search for value in history
            sol = resolve(tree, history)
            if sol is not None:
                print(sol)

        else:
            print("Please define function before trying to solve")

        return key, value

    # check for solving, FUNC
    if solve == 1 and func_def == 1:

        # case 1: ending with =
        if tokens[len(tokens)-1] == '=':
            # function name
            func_name = func[0][1]

            # function variable
            func_var = parse_num(func[0][2][0])

            result = get_function_value(func_name, func_var, history)

            if result is not None:
                print(result)

        # case 2: ending with something
        else:
            # quadratic solve
            left, right = split_at_equals(tokens)

            left = parse_tokens(left)
            right = parse_tokens(right)

            function_left = get_value(left[0][1], history)

            if function_left is None:
                print("Error: function is not defined")
                return key, value

            var = parse_num(func[0][2][0])

            function_right = define_function_terms(
                'dummy_function', var, right, history
            )

            print(function_left, '=', function_right)

            if isinstance(function_left, (Polynomial, RationalExpression)):
                function_left = function_left.plug_vars(history)

            if isinstance(function_right, (Polynomial, RationalExpression)):
                function_right = function_right.plug_vars(history)

            function = sub_exprs(function_left, function_right)

            degree = function.get_degree()

            if degree < 3 and degree >= 0:
                print("solving equation:", function, '= 0')
                # need to plug in non-function variables !!!
                function2 = function.plug_vars(history)
                a, b, c = function2.get_coefficients(2)
                if isinstance(a, Rational):
                    a = a.real
                if isinstance(b, Rational):
                    b = b.real
                if isinstance(c, Rational):
                    c = c.real
                quadratic(a, b, c)
            else:
                print("cannot solve equation", function, '= 0')

        return key, value

    # first check for matrices/vectors
    mat, mat_type = extract_matrix_literal(cmd)
    if mat and mat_type != 0:
        if not func_def:
            key = tokens[0]
            # this doesn't account for polynomials in matrix, variables are not substituted
            matrix_input = parse_matrix_literal(mat[0], mat_type)
            value = matrix_input
            print(value)
            return key, value
        else:
            print("ERROR: assigning matrix/vector to function")
            return None, None

    # next check for regular variables
    if not func_def and tokens[0].isalpha() and tokens[1] == '=':
        if tokens[len(tokens) - 1] != '=':
            if tokens[0] == 'i':
                print("ERROR: Assignment to i is forbidden")
                return None, None

            # case where variable is set to itself plus something
            if tokens[0] in tokens[2:]:
                print("attempt to make variable recursive forbidden")
                return None, None

            # here parse RHS
            key = tokens[0]
            tokens = parse_tokens(tokens[2:])
            tree, _ = parse_expression2(tokens, None, history)
            value = tree
            if isinstance(tree, Node):
                value = solve_node(tree, history)
            var = Variable(key, value)
            if value is not None:
                print(value)
                return key, var
            else:
                tree = simplify_node(tree, history)
                print(tree)
                return key, tree

    # next check for functions
    if func_def:
        if func[len(func) - 1] != '=':
            if func[0][1] == 'i':
                print("ERROR: Assignment to i is forbidden")
                return None, None
            key, value = define_function(func, history)
            if isinstance(value, (Polynomial, RationalExpression)):
                value.combine_like_terms()
            print(value)
            return key, value

    return key, value
