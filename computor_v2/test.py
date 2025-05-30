from complex import Complex
from parse import parse_cmd

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
s = "f(x) = a^2 * x"#x^2 + 2x + 6 "
# s = "f(x) = 3 *  2x + x^2+1/(x+1)"

# s = "g(x) = (x+1)"

history = {}


print('>', s)
key, value = parse_cmd(s, history)
history[key] = value

# for key in history:
# 	print('history', key, history[key])

s = "f(x) = ?"
print('>', s)
key, value = parse_cmd(s, history)

s = "a = 3"
print('>', s)
key, value = parse_cmd(s, history)
history[key] = value

# for key in history:
# 	print('history', key, history[key])

s = "a = ?"
print('>', s)
key, value = parse_cmd(s, history)
history[key] = value

s = "f(x) = ?"
print('>', s)
key, value = parse_cmd(s, history)

exit()

s = "f(x) = 2 ?"
print('>', s)
key, value = parse_cmd(s, history)






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