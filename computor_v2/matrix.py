# Note that scalar * matrix is NOT supported, format must be matrix * scalar
# Thus vector * matrix is also NOT supported, format must be vector * scalar
# This is because scalar includes Rational and Complex classes

# Also scalar / matrix is a no no because that doesn't exist: matrices have inverses

# Inverse Martix
# A^-1 = adj(A) / |A|
# A is a square matrix
# adj(A) is the adjoint matrix of A = the transpose of the cofactor element matrix of A
# |A| is the determinant of A, where |A| != 0
## this is easy for 2 x 2 matrices but then gets more complicated, skip?

class Matrix:

	def __init__(self, *args):
		"""Initializes via list of lists or size of matrix"""
		self.data = None
		self.shape = None
		largs = list(args)
		if len(largs) != 1:
			print("Usage: initialize Matrix with list of lists or tuple")
			exit()
		elif isinstance(largs[0], tuple):
			self.shape = largs[0]
			self.data = []
			for i in range(self.shape[0]):
				lst = []
				for j in range(self.shape[1]):
					lst.append(0)
				self.data.append(lst)
		elif all(isinstance(a, list) for a in largs[0]):
			x = len(largs[0])
			y = len(largs[0][0])
			for i in range(1, x):
				if len(largs[0][i]) != y:
					print("Error: All rows of a matrix should have the same length")
					return None
			self.data = largs[0]
			self.shape = (x, y)
		else:
			print("Usage: initialize Matrix with list of lists or tuple")
			exit()

	def __str__(self):
		"""Returns string of matix"""
		if self.data != None:
			output = "["
			for i in range(self.shape[0]):
				output += "[" + ", ".join( [ str(element) for element in self.data[i] ] ) + "]"
				if i < self.shape[0] - 1:
					output += ", "
			output += "]"
			return(output)
		else:
			return("Matrix is empty")

	def __repr__(self):
		"""Returns info of matix"""
		if self.data != None:
			output = "This is a Matrix object containing the following matrix: ["
			for i in range(self.shape[0]):
				output += "[" + ", ".join( [ str(element) for element in self.data[i] ] ) + "]"
				if i < self.shape[0] - 1:
					output += ", "
			output += "]"
			return(output)
		else:
			return("Matrix is empty")

	def __mod__(self, o):
		print("Error: mod not allowed with matrix/vector")
		return None
	
	def __rmod__(self, o):
		print("Error: mod not allowed with matrix/vector")
		return None
	
	def __pow__(self, o):
		print("Error: pow not allowed with matrix/vector")
		return None

	def __rpow__(self, o):
		print("Error: pow not allowed with matrix/vector")
		return None
		  
	def __add__(self, o):
		"""magic addition of matrices, only of the same size"""
		if not isinstance(o, Matrix):
			print("ERROR: attempt to add non-Matrix obj")
			return None
		if o.shape[0] != self.shape[0] or o.shape[1] != self.shape[1]:
			print("ERROR: addition failed: matrices are not of the same size")
			return None
		new_matrix = []
		for i in range(self.shape[0]):
			lst = []
			for j in range(self.shape[1]):
				lst.append(self.data[i][j] + o.data[i][j])
			new_matrix.append(lst)
		new_matrix = Matrix(new_matrix)
		return new_matrix

	def __radd__(self, o):
		"""reverse addition"""
		print("ERROR: not a valid demand")

	def __sub__(self, o):
		"""subtraction only for matrices of the same size"""
		if not isinstance(o, Matrix):
			print("ERROR: attempt to subtract non-Matrix obj")
			return None
		if o.shape[0] != self.shape[0] or o.shape[1] != self.shape[1]:
			print("ERROR: subtraction failed: matrices are not of the same size")
			return None
		new_matrix = []
		for i in range(self.shape[0]):
			lst = []
			for j in range(self.shape[1]):
				lst.append(self.data[i][j] - o.data[i][j])
			new_matrix.append(lst)
		new_matrix = Matrix(new_matrix)
		return new_matrix

	def __rsub__(self, o):
		"""reverse subtraction only for matrices of the same size"""
		"""not actually sure what this means so probably wrong"""
		print("ERROR: not a valid demand")
		return None

	def __truediv__(self, d): #change here
		"""Division by scalar"""
		if isinstance(d, Matrix) or isinstance(d, str):
			print("ERROR: can only divide by scalar")
			return None
		if d == 0:
			print("ERROR: Division by zero")
			return None
		new_matrix = []
		for i in range(self.shape[0]):
			lst = []
			for j in range(self.shape[1]):
				lst.append(self.data[i][j] / d)
			new_matrix.append(lst)
		new_matrix = Matrix(new_matrix)
		return new_matrix

	def __rtruediv__(self, d):
		"""reverse Division by scalar"""
		print("ERROR: not a valid demand")
		return None

	def __mul__(self, o):
		"""Multiplication by Matrix or Scalar or Vector"""
		#by matrix
		if isinstance(o, Matrix) and self.shape[1] == o.shape[0]:
			new_matrix = []
			for i in range(self.shape[0]):
				lst = []
				for j in range(o.shape[1]):
					value = 0
					for k in range(self.shape[1]):
						value += self.data[i][k] * o.data[k][j]
					lst.append(value)
				new_matrix.append(lst)
			if len(new_matrix) == 1 or len(new_matrix[0]) == 1:
				new_vector = Vector(new_matrix) #return vector
				return new_vector
			else:
				new_matrix = Matrix(new_matrix)# return matrix
				return new_matrix
		#by vector
		elif isinstance(o, Vector) and self.shape[1] == o.shape[0]:
			new_vector = []
			for i in range(self.shape[0]):
				lst = []
				value = 0
				for k in range(self.shape[1]):
					value += self.data[i][k] * o.data[1][k]
				lst.append(value)
			new_vector.append(lst)
			if len(new_vector) == 1 and len(new_vector[0]) == 1:
				new_scalar = new_vector[0][0] #return scalar
				return new_scalar
			else:
				new_vector = Vector(new_vector) #return vector
				return new_vector
		#by scalar
		elif not (isinstance(o, Matrix) or isinstance(o, str)):
			new_matrix = []
			for i in range(self.shape[0]):
				lst = []
				for j in range(self.shape[1]):
					lst.append(self.data[i][j] * o)
				new_matrix.append(lst)
			new_matrix = Matrix(new_matrix)
			return new_matrix
		else:
			print("ERROR: not a valid operation")
			return None

	def __rmul__(self, o):
		"""reverse Multiplication by Matrix or Scalar or Vector"""
		#by matrix
		if isinstance(o, Matrix) and self.shape[1] == o.shape[0]:
			new_matrix = []
			for i in range(self.shape[0]):
				lst = []
				for j in range(o.shape[1]):
					value = 0
					for k in range(self.shape[1]):
						value += self.data[i][k] * o.data[k][j]
					lst.append(value)
				new_matrix.append(lst)
			if len(new_matrix) == 1 or len(new_matrix[0]) == 1:
				new_vector = Vector(new_matrix) #return vector
				return new_vector
			else:
				new_matrix = Matrix(new_matrix)# return matrix
				return new_matrix
		#by vector
		elif isinstance(o, Vector) and self.shape[1] == o.shape[0]:
			new_vector = []
			for i in range(self.shape[0]):
				lst = []
				value = 0
				for k in range(self.shape[1]):
					value += self.data[i][k] * o.data[1][k]
				lst.append(value)
			new_vector.append(lst)
			if len(new_vector) == 1 and len(new_vector[0]) == 1:
				new_scalar = new_vector[0][0] #return scalar
				return new_scalar
			else:
				new_vector = Vector(new_vector) #return vector
				return new_vector
		#by scalar
		elif not (isinstance(o, Matrix) or isinstance(o, str)):
			new_matrix = []
			for i in range(self.shape[0]):
				lst = []
				for j in range(self.shape[1]):
					lst.append(self.data[i][j] * o)
				new_matrix.append(lst)
			new_matrix = Matrix(new_matrix)
			return new_matrix
		else:
			print("ERROR: not a valid operation")
			return None

	def T(self):
		"""Return transpose of Matrix"""
		new_matrix = []
		for j in range(self.shape[1]):
			lst = []
			for i in range(self.shape[0]):
				lst.append(self.data[i][j])
			new_matrix.append(lst)
		new_matrix = Matrix(new_matrix)
		return new_matrix

class Vector(Matrix):

	def __init__(self, *args):
		super().__init__(*args)
		if self.shape[1] != 1 and self.shape[0] != 1:
			print("ERROR: object is not a vector")
			return None

	def dot(self, o):
		"""dot product of two vectors"""
		if isinstance(o, Vector) and o.shape[0] == self.shape[1] and o.shape[1] == self.shape[0]:
			new_value = self * o
			if len(new_value.data) == 1 and len(new_value.data[0]) == 1:
				new_value = new_value.data[0][0] #return scalar
			return new_value
		else:
			print("ERROR: dimension problem")
			return None


