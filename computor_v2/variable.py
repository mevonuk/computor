class Variable:
    """Variable class for assigning a value to a string"""

    def __init__(self, name, value):
        """Initialize variable object with name and value"""
        if not isinstance(name, str):
            raise TypeError("Error: variable name should be a string")
        self.value = value
        self.name = name

    def __str__(self):
        """Convert variable to string for printing"""
        return self.name

    def print_value(self):
        """Prints string with variable name and value"""
        print(f"Variable {self.name} = {self.value}")
