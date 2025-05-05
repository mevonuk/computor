# computor

## Overview
This project is based on the Ecole 42 computor (v1) project.  The goal is to enter, reduce/simplify, and then solve, quadratic and linear equations.

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

## Installation and Setup (v1)
1. Clone the repository
2. Change to computor_v1 directory
3. python computor.py "equation"
	- python computor.py "2x + 3 x^2 = 5x^3 -x"