# computor

## Overview
This project is based on the Ecole 42 computor (v1) and (v2) projects. The goal of computor_v1 is to enter, reduce/simplify, and then solve quadratic and linear equations. Conversely, computer_v2 is a general calculator that can hold the values of variables, functions, and matrices. Functions can be solved as in computor_v1, and matrix operations are possible. Matrices are not included in functions; however, polynomials can appear in the terms of matrices.

### Contributor
- M. Evonuk (https://github.com/mevonuk)

## Tools
- Coding language: Python

## Main Features

### V1
- Equations are simplified, terms are combined, and solutions are found for equations with dregree up to 2.
- Imaginary solutions are supported.
- Users have flexibility in how they enter terms:
	- "Explicit": a * x^0 + b * x^1 + c * x^2 ...
	- Free form: a + b x + c x^2 + ...
	- "Implicit": a + bx + cx2 + ...
	- Mixed order (of exponent degree): ax^3 - b + x = 4x^x - 3
- However:
	- x*x != x^2
	- exponents must be positive integers
	- multiplication and division (in equation entry) are not supported

### V2
- Functions, variables, matrices, and vectors are entered at the command prompt.
- Imaginary numbers are supported.
- Variables/functions/matrices can be redefined, type does not need to be conserved.
	- > f = 2
	-   2
	- > g = f
	-   2
	- > f(x) = 3 + x
	-   3 + x
- The following operators are supported for variables and in functions: *, /, +, -, %
- Matrices/vectors should be entered in the following format: matA = [[1,2];[4,7]] with semicolons seperating the rows of the matrix and commas seperating the columns.
	- Allowed operations include:
		- '+' and '-' (two matrices of same size)
		- '*' and '/' by a constant
		- '**' matrix multiplication
			- make sure matrix shapes are compatible!
			- e.g., a = [3,4]; b = [[1];[2]]; c = a ** b and d = b ** a are permitted.
	- The modulo (%) operator is not supported for matrices and vectors
- To define a function (of a single variable): f(x) = x^2 + ...
	- To solve an order < 3 equation: "f(x) = something ?" where "something" can be a constant or variable
	- "f(1) = ?" will return the value of the function f(x) with x = 1.
- Constants can be type Rational or Complex: A = 2 + 3 * i, C = 4.2
- To access a previously defined variable, function, or matrix, use the "?"
	- "C = ?" will return its value if defined, otherwise itself
	- C is equivalent to c
- Polynomials and variables will be simplified using the history of declared variables and values if possible
- Program is exited using "exit" or cntl-C

## Installation and Setup
1. Clone the repository
2. Change to computor_v1 directory

### V1
3. python computor.py "equation"
	- e.g.: python computor.py "2x + 3 x^2 = 5x^3 -x"

### V2
3. python computorv2.py