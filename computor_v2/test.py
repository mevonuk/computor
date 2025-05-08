from rational import Rational
from complex import Complex
from matrix import Matrix, Vector
from function import Term, Polynomial
from parse import parse_cmd
from lexer import parse_number, parse_term, extract_matrix_literal
from parse import tokenize, parse_tokens

def print_instructions():
    print("Welcome to computor_v2 by mevonuk")
    print("This calculator supports rational and complex numbers,")
    print("matrices, vectors, and simple functions.")
    print("\nAcceptible input:")
    print("\tvariable_name = expression (to assign a value to a variable)")
    print("\tExpression = ? (to solve expression)\n")
    print("To exit the program, enter 'exit'\n")


# print_instructions()

s = 'f(x) = x^2 + 1(4+2*x)x*(x^3+5)'

s = '4.2x + 45'

print(s)
tokens = tokenize(s)
#print(tokens)
func = parse_tokens(tokens)
for item in func:
    print(item)

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
        key, value = parse_cmd(cmd)
        if key and value:
            history[key] = value

    print(history)