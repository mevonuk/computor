from rational import Rational
from complex import Complex
from matrix import Matrix, Vector
from function import Term, Polynomial
from parse import parse_cmd

print("Welcome to computor_v2 by mevonuk")
print("This calculator supports rational and complex numbers,")
print("matrices, vectors, and simple functions.")
print("\nAcceptible input:")
print("\tvariable_name = expression (to assign a value to a variable)")
print("\tExpression = ? (to solve expression)\n")
print("To exit the program, enter 'exit'\n")

cmd = ""
history = {}

while(1):
    cmd = input("> ")
    if cmd == 'exit':
        exit()

    if cmd:
        print(cmd)
        content = parse_cmd(cmd)