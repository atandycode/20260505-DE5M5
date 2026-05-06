class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_sum(self):
        return self.a + self.b
    
    def get_subtract(self):
        return self.a - self.b
    
    def get_divide(self):
        return self.a / self.b
    
    def get_prod(self):
        return self.a * self.b
    

myCalc1 = Calculator(3, 8)
