from django.test import TestCase
from .utils import Calculator, calculate_expression, format_calculation_result


class CalculatorTestCase(TestCase):
    """Test cases for the Calculator utility class."""
    
    def test_add_positive_numbers(self):
        """Test addition of positive numbers."""
        self.assertEqual(Calculator.add(5, 3), 8)
        self.assertEqual(Calculator.add(10, 15), 25)
        self.assertEqual(Calculator.add(1, 1), 2)
    
    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        self.assertEqual(Calculator.add(-5, -3), -8)
        self.assertEqual(Calculator.add(-5, 3), -2)
        self.assertEqual(Calculator.add(5, -3), 2)
    
    def test_add_zero(self):
        """Test addition with zero."""
        self.assertEqual(Calculator.add(0, 5), 5)
        self.assertEqual(Calculator.add(5, 0), 5)
        self.assertEqual(Calculator.add(0, 0), 0)
    
    def test_add_floats(self):
        """Test addition with floating point numbers."""
        self.assertAlmostEqual(Calculator.add(1.5, 2.3), 3.8, places=7)
        self.assertAlmostEqual(Calculator.add(0.1, 0.2), 0.3, places=7)
    
    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers."""
        self.assertEqual(Calculator.subtract(10, 3), 7)
        self.assertEqual(Calculator.subtract(5, 5), 0)
        self.assertEqual(Calculator.subtract(3, 10), -7)
    
    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        self.assertEqual(Calculator.subtract(-5, -3), -2)
        self.assertEqual(Calculator.subtract(-5, 3), -8)
        self.assertEqual(Calculator.subtract(5, -3), 8)
    
    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers."""
        self.assertEqual(Calculator.multiply(5, 3), 15)
        self.assertEqual(Calculator.multiply(4, 0), 0)
        self.assertEqual(Calculator.multiply(7, 1), 7)
    
    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        self.assertEqual(Calculator.multiply(-5, 3), -15)
        self.assertEqual(Calculator.multiply(-5, -3), 15)
        self.assertEqual(Calculator.multiply(5, -3), -15)
    
    def test_multiply_floats(self):
        """Test multiplication with floating point numbers."""
        self.assertAlmostEqual(Calculator.multiply(2.5, 4), 10.0, places=7)
        self.assertAlmostEqual(Calculator.multiply(1.5, 2.2), 3.3, places=7)
    
    def test_divide_positive_numbers(self):
        """Test division of positive numbers."""
        self.assertEqual(Calculator.divide(10, 2), 5)
        self.assertEqual(Calculator.divide(7, 2), 3.5)
        self.assertEqual(Calculator.divide(9, 3), 3)
    
    def test_divide_negative_numbers(self):
        """Test division with negative numbers."""
        self.assertEqual(Calculator.divide(-10, 2), -5)
        self.assertEqual(Calculator.divide(-10, -2), 5)
        self.assertEqual(Calculator.divide(10, -2), -5)
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Calculator.divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")
        
        with self.assertRaises(ValueError):
            Calculator.divide(-5, 0)
    
    def test_power_operations(self):
        """Test power operations."""
        self.assertEqual(Calculator.power(2, 3), 8)
        self.assertEqual(Calculator.power(5, 0), 1)
        self.assertEqual(Calculator.power(0, 5), 0)
        self.assertEqual(Calculator.power(-2, 3), -8)
        self.assertEqual(Calculator.power(-2, 2), 4)
        self.assertEqual(Calculator.power(3, 2), 9)
    
    def test_modulo_operations(self):
        """Test modulo operations."""
        self.assertEqual(Calculator.modulo(10, 3), 1)
        self.assertEqual(Calculator.modulo(15, 5), 0)
        self.assertEqual(Calculator.modulo(7, 2), 1)
        self.assertEqual(Calculator.modulo(8, 4), 0)
    
    def test_modulo_by_zero(self):
        """Test modulo by zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Calculator.modulo(10, 0)
        self.assertEqual(str(context.exception), "Cannot perform modulo with zero")
    
    def test_square_root_positive(self):
        """Test square root of positive numbers."""
        self.assertEqual(Calculator.square_root(9), 3)
        self.assertEqual(Calculator.square_root(16), 4)
        self.assertAlmostEqual(Calculator.square_root(2), 1.4142135623730951, places=7)
        self.assertEqual(Calculator.square_root(0), 0)
        self.assertEqual(Calculator.square_root(1), 1)
    
    def test_square_root_negative(self):
        """Test square root of negative numbers raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Calculator.square_root(-1)
        self.assertEqual(str(context.exception), "Cannot calculate square root of negative number")
        
        with self.assertRaises(ValueError):
            Calculator.square_root(-9)


class CalculateExpressionTestCase(TestCase):
    """Test cases for the calculate_expression function."""
    
    def test_simple_expressions(self):
        """Test simple mathematical expressions."""
        self.assertEqual(calculate_expression("2 + 3"), 5)
        self.assertEqual(calculate_expression("10 - 4"), 6)
        self.assertEqual(calculate_expression("5 * 3"), 15)
        self.assertEqual(calculate_expression("15 / 3"), 5)
    
    def test_complex_expressions(self):
        """Test complex mathematical expressions."""
        self.assertEqual(calculate_expression("2 + 3 * 4"), 14)
        self.assertEqual(calculate_expression("(2 + 3) * 4"), 20)
        self.assertEqual(calculate_expression("2^3"), 8)  # Power operation
        self.assertAlmostEqual(calculate_expression("10 / 3 * 3"), 10.0, places=7)
        self.assertEqual(calculate_expression("(10 + 5) / 3"), 5)
    
    def test_expressions_with_floats(self):
        """Test expressions with floating point numbers."""
        self.assertAlmostEqual(calculate_expression("1.5 + 2.5"), 4.0, places=7)
        self.assertAlmostEqual(calculate_expression("3.14 * 2"), 6.28, places=7)
        self.assertEqual(calculate_expression("5.0 / 2.0"), 2.5)
    
    def test_expressions_with_whitespace(self):
        """Test expressions with various whitespace."""
        self.assertEqual(calculate_expression(" 2 + 3 "), 5)
        self.assertEqual(calculate_expression("2+3"), 5)
        self.assertEqual(calculate_expression("  (2  +  3)  *  4  "), 20)
    
    def test_invalid_expressions(self):
        """Test invalid expressions raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_expression("2 + abc")  # Invalid characters
        
        with self.assertRaises(ValueError):
            calculate_expression("import os")  # Dangerous code
        
        with self.assertRaises(ValueError):
            calculate_expression("2 +")  # Incomplete expression
        
        with self.assertRaises(ValueError):
            calculate_expression("2 + $")  # Invalid character
    
    def test_division_by_zero_in_expression(self):
        """Test division by zero in expressions."""
        with self.assertRaises(ValueError) as context:
            calculate_expression("10 / 0")
        self.assertEqual(str(context.exception), "Division by zero")
        
        with self.assertRaises(ValueError):
            calculate_expression("5 / (3 - 3)")
    
    def test_empty_expression(self):
        """Test empty expression raises ValueError."""
        with self.assertRaises(ValueError):
            calculate_expression("")
        
        with self.assertRaises(ValueError):
            calculate_expression("   ")


class FormatCalculationResultTestCase(TestCase):
    """Test cases for the format_calculation_result function."""
    
    def test_format_integers(self):
        """Test formatting integer results."""
        self.assertEqual(format_calculation_result(5), "5")
        self.assertEqual(format_calculation_result(10.0), "10")
        self.assertEqual(format_calculation_result(-3), "-3")
    
    def test_format_floats_default_precision(self):
        """Test formatting float results with default precision."""
        self.assertEqual(format_calculation_result(5.123), "5.12")
        self.assertEqual(format_calculation_result(3.456789), "3.46")
        self.assertEqual(format_calculation_result(-2.789), "-2.79")
    
    def test_format_floats_custom_precision(self):
        """Test formatting float results with custom precision."""
        self.assertEqual(format_calculation_result(5.123456, 4), "5.1235")
        self.assertEqual(format_calculation_result(3.14159, 3), "3.142")
        self.assertEqual(format_calculation_result(2.0, 1), "2")
    
    def test_format_zero(self):
        """Test formatting zero values."""
        self.assertEqual(format_calculation_result(0), "0")
        self.assertEqual(format_calculation_result(0.0), "0")
        self.assertEqual(format_calculation_result(0.00), "0")
