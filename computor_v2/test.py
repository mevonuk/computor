from complex import Complex
from parse import parse_cmd
from lexer import tokenize, parse_expression, parse_tokens

def print_instructions():
    print("Welcome to computor_v2 by mevonuk")
    print("This calculator supports rational and complex numbers,")
    print("matrices, vectors, and simple functions.")
    print("\nAcceptible input:")
    print("\tvariable_name = expression (to assign a value to a variable)")
    print("\tExpression = ? (to solve expression)\n")
    print("To exit the program, enter 'exit'\n")


# print_instructions()

s = '-x-(-4-2*x)'
#s = '5 + i +3x^2 - f(a)'

history = {}

history['f(a)'] = 5
history['x'] = 1

print(s)
tokens = tokenize(s)
tokens = parse_tokens(tokens)
print(tokens)

tree, _ = parse_expression(tokens)
print(tree)
sol = tree.solve_node(history)
if sol != None:
    print(sol)


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