class Variable:
    def __init__(self, name, value):
        if not isinstance(name, str):
            print("Error: variable name should be a string")
            exit()
        self.value = value
        self.name = name

    def __str__(self):
        return self.name
    
    def print_value(self):
        print(f"Variable {self.name} = {self.value}")