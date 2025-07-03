# contains parse_num2, parse_expression2

from rational import Rational
from complex import Complex
from variable import Variable
from node import Node

from tools import get_value
from function_tools import get_function_value

from matrix import Matrix, Vector

from lex_base import parse_num, tokenize
from lex_base import parse_tokens
from tree_tool import solve_node


def parse_num2(token, var, history):
    # print("in parse_num2", token, var)
    if not isinstance(token, str):
        return token
    if token == 'i':
        return Complex(0, 1)
    if token.isalpha():
        # need to check here in history !!!
        if token != var:
            value = get_value(token, history)
            if value is not None:
                # print("returning value", value, type(value))
                return value
        # print("returning variable")
        return Variable(token, None)
    # print("returning rational", token)
    if '.' in token:
        return Rational(float(token))
    else:
        return Rational(int(token))


def parse_expression2(tokens, var, history, index=0, min_precedence=1):
    precedence = {
        '**': 5,
        '^': 5,
        '*': 4,
        '/': 4,
        '%': 3,
        '+': 2,
        '-': 2,
        '=': 1
    }

    right_associative = {'^', '**'}

    def parse_primary2(index, var, history):
        token = tokens[index]

        # Parentheses
        if token == '(':
            tree, new_index = parse_expression2(tokens, var, history, index + 1)
            if tokens[new_index] != ')':
                raise SyntaxError("Unmatched parenthesis")
            return tree, new_index + 1

        # Function call tuple: ('FUNC', 'f', [['a']])
        elif isinstance(token, tuple) and token[0] == 'FUNC':
            func_name = token[1]
            args_token_lists = token[2]

            # print(func_name, args_token_lists[0])

            if len(args_token_lists) != 1:
                raise NotImplementedError("Only one-arg functions supported")

            arg_expr = args_token_lists[0]
            if isinstance(args_token_lists[0], list) and len(args_token_lists[0]) > 1:
                arg_expr, _ = parse_expression2(args_token_lists[0], var, history)

            # need to check here in history !!!
            value = get_value(func_name, history)

            value2 = parse_num2(arg_expr, value.var, history)

            result = None
            if value is not None and value2 != var:
                result = get_function_value(func_name, value2, history)
                if isinstance(result, Variable):
                    return Node(result, None, 'VAR'), index + 1
                return result, index + 1
            return Node(func_name, arg_expr, 'FUNC'), index + 1

        return parse_num2(token, var, history), index + 1

    lhs, index = parse_primary2(index, var, history)

    while index < len(tokens):
        op = tokens[index]
        if op not in precedence:
            break
        prec = precedence[op]
        if prec < min_precedence:
            break
        next_min_prec = prec + (0 if op in right_associative else 1)

        rhs, index = parse_expression2(tokens, var, history, index + 1, next_min_prec)

        lhs = Node(parse_num2(lhs, var, history), parse_num2(rhs, var, history), op)

    return lhs, index


def parse_matrix_literal(matrix_str, matrix_type, history):
    """Parse matrix tokens"""
    # Remove outer brackets
    rows = matrix_str.split(';')
    # remove brackets
    num_col = -1
    matrix_data = []
    for row in rows:
        row = row.replace('[', '')
        row = row.replace(']', '')
        new_row = []
        for term in row.split(','):
            # parse term here
            term = tokenize(term)
            tokens = parse_tokens(term)
            tree, _ = parse_expression2(tokens, None, history)
            value = tree
            if isinstance(tree, Node):
                value = solve_node(tree, history)
            new_row.append(value)
        num_col_old = num_col
        num_col = len(new_row)
        if num_col_old != -1 and num_col_old != num_col:
            print("Error: All cols of a matrix should have the same length")
            return None
        matrix_data.append(new_row)
    if matrix_type == 2:
        return Matrix(matrix_data)
    else:
        return Vector(matrix_data)
