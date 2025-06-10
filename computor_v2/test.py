from complex import Complex
from parse import parse_cmd
from variable import Variable


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


# s = '-x-(-4-2*x)'
# s = 'y = 3'
# s = "f(Y) = (y^2 + 3*y +2 / 4)/(y+1) + 1"
s = "f(x) = x "
# s = "f(x) = 3 *  2x + x^2+1/(x+1)"

# s = "g(x) = (x+1)"

history = {}

r = Variable('a', 33)
history[r.name] = r

print('>', s)
key, value = parse_cmd(s, history)
if key is not None and value is not None:
	history[key] = value

s = "f(1) = ?"
print('>', s)
key, value = parse_cmd(s, history)
if key is not None and value is not None:
	history[key] = value

s = "b = a+ 2*f(1) "
print('>', s)
key, value = parse_cmd(s, history)
if key is not None and value is not None:
	history[key] = value

s = "1 + b = ?"
print('>', s)
key, value = parse_cmd(s, history)
if key is not None and value is not None:
	history[key] = value

# for key in history:
# 	print('history', key, history[key], type(history[key]))

s = "g(x) = a + b + f(1) * x"#+ f(1)"
print('>', s)
key, value = parse_cmd(s, history)
if key is not None and value is not None:
	history[key] = value




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