# contains parse_num, parse_expression

from rational import Rational
from complex import Complex
from variable import Variable
from node import Node


def parse_num(token):
    if isinstance(token, (Node, Complex, Rational, Variable)):
        return token
    if token == 'i':
        return Complex(0, 1)
    if token.isalpha():
        return Variable(token, None)
    if '.' in token:
        return Rational(float(token))
    else:
        return Rational(int(token))


def parse_expression(tokens, index=0, min_precedence=1):
    precedence = {
        '**': 4,
        '^': 4,
        '*': 3,
        '/': 3,
        '%': 3,
        '+': 2,
        '-': 2,
        '=': 1
    }

    right_associative = {'^', '**'}

    def parse_primary(index):
        token = tokens[index]

        # Parentheses
        if token == '(':
            tree, new_index = parse_expression(tokens, index + 1)
            if tokens[new_index] != ')':
                raise SyntaxError("Unmatched parenthesis")
            return tree, new_index + 1

        # Function call tuple: ('FUNC', 'f', [['a']])
        elif isinstance(token, tuple) and token[0] == 'FUNC':
            func_name = token[1]
            args_token_lists = token[2]

            if len(args_token_lists) != 1:
                raise NotImplementedError("Only one-arg functions supported")

            arg_expr, _ = parse_expression(args_token_lists[0])
            # return Node(func_name, arg_expr, 'FUNC'), index + 1
            func = f"{func_name}({arg_expr})"
            # need to save here a function class?
            print("lexer:parse_expression:parse_primary: func", func, func_name, arg_expr)
            return Node(func_name, arg_expr, 'FUNC'), index + 1
            # return Node(func, None, 'FUNC'), index + 1

        return Node(parse_num(token), None, 'VAR'), index + 1

    lhs, index = parse_primary(index)

    while index < len(tokens):
        op = tokens[index]
        if op not in precedence:
            break
        prec = precedence[op]
        if prec < min_precedence:
            break
        next_min_prec = prec + (0 if op in right_associative else 1)

        rhs, index = parse_expression(tokens, index + 1, next_min_prec)

        lhs = Node(parse_num(lhs), parse_num(rhs), op)

    return lhs, index
