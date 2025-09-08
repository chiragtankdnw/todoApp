"""
Utility functions for the todo app.
Contains a basic calculator class and helper functions.
"""


class Calculator:
    """
    A basic calculator utility class for performing arithmetic operations.
    """
    
    @staticmethod
    def add(a, b):
        """Add two numbers."""
        return a + b
    
    @staticmethod
    def subtract(a, b):
        """Subtract b from a."""
        return a - b
    
    @staticmethod
    def multiply(a, b):
        """Multiply two numbers."""
        return a * b
    
    @staticmethod
    def divide(a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @staticmethod
    def power(a, b):
        """Raise a to the power of b."""
        return a ** b
    
    @staticmethod
    def modulo(a, b):
        """Return remainder of a divided by b."""
        if b == 0:
            raise ValueError("Cannot perform modulo with zero")
        return a % b
    
    @staticmethod
    def square_root(a):
        """Calculate square root of a number."""
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return a ** 0.5


def calculate_expression(expression):
    """
    Safely evaluate a mathematical expression string.
    Only allows basic arithmetic operations.
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        float: Result of the calculation
        
    Raises:
        ValueError: If expression is invalid or contains forbidden operations
    """
    # Remove whitespace
    expression = expression.replace(" ", "")
    
    # Check for valid characters only
    allowed_chars = set("0123456789+-*/.()^")
    if not all(char in allowed_chars for char in expression):
        raise ValueError("Invalid characters in expression")
    
    # Replace ^ with ** for power operation
    expression = expression.replace("^", "**")
    
    try:
        # Use eval but restrict to mathematical operations only
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


def format_calculation_result(result, decimal_places=2):
    """
    Format calculation result for display.
    
    Args:
        result (float): The calculation result
        decimal_places (int): Number of decimal places to show
        
    Returns:
        str: Formatted result string
    """
    if isinstance(result, int) or result.is_integer():
        return str(int(result))
    else:
        return f"{result:.{decimal_places}f}"
