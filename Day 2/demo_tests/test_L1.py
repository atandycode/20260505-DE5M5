import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):
    def test_sum(self):
        calc = Calculator(6,3)
        self.assertEqual(calc.get_sum(), 9, "The answer was not 9.")

    def test_subtract(self):
        calc = Calculator(10, 5)
        self.assertEqual(calc.get_subtract(), 5, "The answer was not 5.")
    
    def test_product(self):
        calc = Calculator(10, 5)
        self.assertEqual(calc.get_prod(), 50, "The answer was not 50.")
    
    def test_divide(self):
        calc = Calculator(10, 5)
        self.assertEqual(calc.get_divide(), 2, "The answer was not 2.")

if __name__ == "__main__":
    unittest.main()