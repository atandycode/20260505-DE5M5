import argparse

class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_sum(self):
        return self.a + self.b
    
    def get_diff(self):
        return self.a - self.b
    
    def get_divide(self):
        return self.a / self.b
    
    def get_prod(self):
        return self.a * self.b
    
    def get_sqrt(self):
        return self.a ** 0.5
    
def main(args):
    calc = Calculator(args.input_a, args.input_b)

    method = getattr(calc, args.method)
    return method()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculator")

    parser.add_argument('--input_a', type=int, required=True, help="input first number")
    parser.add_argument('--input_b', type=int, required=True, help="input second number")

    parser.add_argument('--method',
                        type=str,
                        required=True,
                        choices=['get_sum', 'get_diff', 'get_divide', 'get_prod', 'get_sqrt'],
                        help="method to run")

    args = parser.parse_args()

    print(main(args))
