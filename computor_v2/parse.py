from rational import Rational
from variable import Variable
from polynomial import Polynomial, RationalExpression, plug_in_var, sub_exprs
from function import Function
from lex_base import tokenize, parse_tokens, extract_matrix_literal, parse_matrix_literal
from lexer import parse_expression, parse_num
from tree import Tree
from tools import get_value, get_value2
from my_math_tools import quadratic
from check_input import check_user_input


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

    # print('var in define_function_terms', var, type(var))

    terms, _ = parse_expression(term)

    # if not isinstance(terms, Tree):
        # terms = Tree(terms, 0, 'FUNC')

    # print('in define_function_terms', name, var, terms, type(terms))

    value = Function(name, var, terms)

    # print('in define_function_terms', value, type(value), value.terms)

    poly = value.convert_function()

    # print('in define_function_terms', poly, type(poly))

    value = poly
    # print('in define_function_terms',value, type(value))
    if isinstance(poly, RationalExpression):
        simplify = poly.simplify()
        print(simplify.solve(history))
        value = simplify
    return value


def define_function(func, history):
    var, _ = parse_expression(func[0][2])

    key = func[0][1]

    # print("in define_function", var, type(var), key, type(key))

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

    func_def = 0
    if func and func[0] and func[0][0] == 'FUNC':
        func_def = 1

    # check for solving, not FUNC
    if tokens[len(tokens) - 1] == '?' and func_def == 0:
        print("parse: parse_cmd: Solving in case func_def == 0")
        # remove ?
        end = len(tokens)-1
        tokens = tokens[:end]

        # case 1: ending with =
        if tokens[len(tokens)-1] == '=':
            # remove =
            end = len(tokens)-1
            tokens = tokens[:end]
            tokens = parse_tokens(tokens)

            tree, _ = parse_expression(tokens)
            print("parse_cmd: tree", tree, type(tree))
            if isinstance(tree, str):
                sol = get_value2(tree, history)
                if isinstance(sol, Tree):
                    sol = sol.solve_node(history)
            elif isinstance(tree, Variable):
                sol = get_value2(tree.name, history)
                if isinstance(sol, Tree):
                    sol = sol.solve_node(history)
            else:
                sol = tree.solve_node(history)
            if sol != None:
                print(sol)
        
        else:
            print("Please define function before trying to solve")

        return key, value

    # check for solving, FUNC
    if tokens[len(tokens) - 1] == '?' and func_def == 1:
        # remove ?
        end = len(tokens)-1
        tokens = tokens[:end]

        # case 1: ending with =
        if tokens[len(tokens)-1] == '=':
            # simple solve
            function = get_value(func[0][1], history)

            if function is None:
                print("Error: function is not defined")
                return key, value

            # check for variable
            variable = parse_num(func[0][2][0])

            # print('in parse cmd', function, type(function), variable, type(variable))

            if isinstance(variable, str):
                # print('instance 1')
                sol = function.terms.solve_node(history)
                print(sol)
            elif isinstance(function, (Polynomial, RationalExpression)):
                # print('instance 2')
                # print("to plug vars", function)
                function = function.plug_vars(variable, history)
                # print("to plug in var", function, variable)
                sol = plug_in_var(function, variable, history)
                print(sol)
            else:
                print("function not poly/rational or otherwise")

        # case 2: ending with something
        else:
            # quadratic solve
            # print("case 2: solve quadratic equation")
            left, right = split_at_equals(tokens)

            left = parse_tokens(left)
            right = parse_tokens(right)

            function_left = get_value(left[0][1], history)

            if function_left is None:
                print("Error: function is not defined")
                return key, value

            var = parse_num(func[0][2][0])

            # print("var in parse_cmd", var)
            function_right = define_function_terms('dummy_function', var, right, history)

            print(function_left, '=', function_right)


            if isinstance(function_left, (Polynomial, RationalExpression)):
                function_left = function_left.plug_vars(var, history)

            if isinstance(function_right, (Polynomial, RationalExpression)):
                function_right = function_right.plug_vars(var, history)

            function = sub_exprs(function_left, function_right)

            degree = function.get_degree()
            
            if degree < 3 and degree >= 0:
                print("solving equation:", function, '= 0')
                # need to plug in non-function variables !!!
                # print("var in parse_cmd", var)
                function2 = function.plug_vars(var, history)
                # print('in parse_cmd', function2)
                a, b, c = function2.get_coefficients(2)
                # print(a,b,c,type(a), type(b), type(c))
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
            print("Found matrix, parsing...")
            key = tokens[0]
            matrix_input = parse_matrix_literal(mat[0], mat_type)
            value = matrix_input
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

            # need to check for case where variable is set to itself plus something
            if tokens[0] in tokens[2:]:
                print("attempt to make variable recursive forbidden")
                return None, None

            # here parse RHS
            key = tokens[0]
            tokens = parse_tokens(tokens[2:])
            tree, _ = parse_expression(tokens)
            value = tree.solve_node(history) 
            var = Variable(key, value)
            # print('in parse_cmd', key, type(key), var, type(var), var.name, var.value, type(var.value))
            return key, var

    # next check for functions
    if func_def:
        # print("defining function")
        if func[len(func) - 1] != '=':
            if func[0][1] == 'i':
                print("ERROR: Assignment to i is forbidden")
                return None, None
            key, value = define_function(func, history)
            print(value)
            return key, value

    return key, value