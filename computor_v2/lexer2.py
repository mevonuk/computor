# contains parse_num, parse_expression

from rational import Rational
from complex import Complex
from variable import Variable
from node import Node
from tools import get_value
from function_tools import get_function_value


def parse_num2(token, var, history):
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

            if len(args_token_lists) != 1:
                raise NotImplementedError("Only one-arg functions supported")

            arg_expr, _ = parse_expression2(args_token_lists[0], var, history)
            # return Node(func_name, arg_expr, 'FUNC'), index + 1
            func = f"{func_name}({arg_expr})"

            # need to check here in history !!!
            value = get_value(func_name, history)
            value2 = parse_num2(arg_expr, var, history)
            result = None
            if value is not None and value2 != var:
                result = get_function_value(func_name, value2, history)
                if isinstance(result, Variable):
                    return Node(result, None, 'VAR'), index + 1
                return result, index + 1
            # need to save here a function class?
            # print("lexer:parse_expression:parse_primary: func", func, func_name, arg_expr)
            return Node(func_name, arg_expr, 'FUNC'), index + 1
            # return Node(func, None, 'FUNC'), index + 1

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
