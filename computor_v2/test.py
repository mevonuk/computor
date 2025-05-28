from complex import Complex
from parse import parse_cmd
from lexer import tokenize, parse_expression, parse_tokens
from my_math_tools import quadratic
from tree import Node

def print_instructions():
    print("Welcome to computor_v2 by mevonuk")
    print("This calculator supports rational and complex numbers,")
    print("matrices, vectors, and simple functions.")
    print("\nAcceptible input:")
    print("\tvariable_name = expression (to assign a value to a variable)")
    print("\tExpression = ? (to solve expression)\n")
    print("To exit the program, enter 'exit'\n")


# print_instructions()

# tests:
# assigning matrix
# solving matrix containing functions and variables
# assigning functions
# solving functions, with variables and plugging in value of 'x' in ()
# assigining variables, setting equal to other variables
# solving with variables, functions
# solving quadratic equations

# need to be able to determine how many undefined variables there are
# then if 1, check the power, then if 2 or smaller, solve for the variable

# solving has two cases: f = ? and f(x) = 4 ? to solve for x

# print following input should show simplified form: f = 2 + 4 -> f = 6

# need to have a function to solve for a given value of x in f(x) while preserving the original
# function for use with a different value of x

# need to change the case when taking input so A = a

## simplifying expressions: (x^2 + 3x + 2)/(x + 1) = x + 2 -> use symplify from sympy

# s = '-x-(-4-2*x)'
# s = 'y = 3'
s = "f(y) = (y^2 + 4*y +2)/(y+1)"
# s = "f(x) = 3 *  2x + x^2+1/(x+1)"

# s = "f(x) = (x+1)"

history = {}

# history['f(a)'] = 5
history['x'] = 2
history['y'] = 2


print(s)
key, value = parse_cmd(s, history)

# if key and value:
#     history[key] = value
# print(history)

# s = 'y = ?'
# print(s)
# key, value = parse_cmd(s, history)

# print(s)
# tokens = tokenize(s)
# tokens = parse_tokens(tokens)
# print(tokens)

# tree, _ = parse_expression(tokens)
# print('tree', tree)
# sol = tree.solve_node(history)
# if sol != None:
#     print('sol', sol)


#mat, mat_type = extract_matrix_literal(s)
#print(mat, mat_type)

# num = parse_term(s)
# print("parsed:", num)

exit()

cmd = ""
history = {}

history['i'] = Complex(0, 1)

while(1):
    cmd = input("> ")
    if cmd == 'exit':
        exit()

    if cmd:
        print(cmd)
        key, value = parse_cmd(cmd, history)
        if key and value:
            history[key] = value

    print(history)