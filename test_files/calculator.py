class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        """Add two numbers."""
        self.result = x + y
        return self.result
    
    def subtract(self, x, y):
        """Subtract y from x."""
        self.result = x - y
        return self.result
    
    def multiply(self, x, y):
        """Multiply two numbers."""
        self.result = x * y
        return self.result
    
    def divide(self, x, y):
        """Divide x by y."""
        if y == 0:
            raise ValueError("Cannot divide by zero")
        self.result = x / y
        return self.result

# Test the calculator
if __name__ == "__main__":
    calc = Calculator()
    print("Addition: ", calc.add(5, 3))
    print("Subtraction: ", calc.subtract(10, 4))
    print("Multiplication: ", calc.multiply(6, 7))
    print("Division: ", calc.divide(20, 5)) 