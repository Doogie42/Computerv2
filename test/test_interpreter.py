from computorv2.Token import tokenize
from computorv2.Parser import Parser
from computorv2.Interpreter import Interpreter
from computorv2.Token import Imaginary, Rational
import unittest
from computorv2.Exception import InterpretException

# result checked with https://www.wolframalpha.com/


class TestInterpreter(unittest.TestCase):
    def my_set_up(self, cmd: str):
        token_list = tokenize(cmd)
        parser = Parser(token_list)
        ast = parser.generate()
        return ast

    def test_addition(self):
        ast = self.my_set_up("5 + 2")
        interpreter = Interpreter(ast)
        self.assertEqual(Rational("7.0"), interpreter.interpret_ret_token())

    def test_subtraction(self):
        ast = self.my_set_up("44 - 2")
        interpreter = Interpreter(ast)
        self.assertEqual(Rational("42.0"), interpreter.interpret_ret_token())

    def test_multiplication(self):
        ast = self.my_set_up("21 * 2")
        interpreter = Interpreter(ast)
        self.assertEqual(Rational("42.0"), interpreter.interpret_ret_token())

    def test_division(self):
        ast = self.my_set_up("84 / 2")
        interpreter = Interpreter(ast)
        self.assertEqual(Rational("42.0"), interpreter.interpret_ret_token())

    def test_precedence(self):
        ast = self.my_set_up("5 + 2 * 21")
        interpreter = Interpreter(ast)
        self.assertEqual(Rational("47.0"), interpreter.interpret_ret_token())

    def test_parenthesis(self):
        ast = self.my_set_up("(5 + 16) * 2")
        interpreter = Interpreter(ast)
        self.assertEqual(Rational("42.0"), interpreter.interpret_ret_token())


class TestInterpreterImaginary(unittest.TestCase):
    def my_set_up(self, cmd: str):
        token_list = tokenize(cmd)
        parser = Parser(token_list)
        ast = parser.generate()
        return ast

    def test_addition(self):
        ast = self.my_set_up("5 + 2i")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=5, imaginary=2),
                         interpreter.interpret_ret_token())

    def test_subtraction(self):
        ast = self.my_set_up("44 - i")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=44, imaginary=-1),
                         interpreter.interpret_ret_token())

    def test_parentesis(self):
        ast = self.my_set_up("1 - (5 + i) + i + i")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=-4, imaginary=1),
                         interpreter.interpret_ret_token())

    def test_multiplication(self):
        ast = self.my_set_up("21 * 2 * i")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=0, imaginary=42),
                         interpreter.interpret_ret_token())

    def test_division(self):
        ast = self.my_set_up("84 / 2 / i")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=0, imaginary=-42),
                         interpreter.interpret_ret_token())

    def test_precedence(self):
        ast = self.my_set_up("5 + 2 * 21 * i")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=5, imaginary=42),
                         interpreter.interpret_ret_token())

    def test_multi_1(self):
        ast = self.my_set_up("5 + 2i + 3i - (5 / i) + 5 * i")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=5, imaginary=15),
                         interpreter.interpret_ret_token())

    def test_multi_2(self):
        ast = self.my_set_up("(4 + i) / (8 + i)")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=0.507, imaginary=0.061),
                         interpreter.interpret_ret_token())

    def test_multi_3(self):
        ast = self.my_set_up("(4 + i) * (8 + i)")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=31, imaginary=12),
                         interpreter.interpret_ret_token())

    def test_multi_4(self):
        ast = self.my_set_up("(4 + i) * (8 + i) * (4 + i) / (8 + i)")
        interpreter = Interpreter(ast)
        self.assertEqual(Imaginary(rational=15, imaginary=8),
                         interpreter.interpret_ret_token())


class TestInterpreterPower(unittest.TestCase):
    def my_set_up(self, cmd: str):
        token_list = tokenize(cmd)
        parser = Parser(token_list)
        ast = parser.generate()
        interpreter = Interpreter(ast)
        cmd_python = cmd.replace("^", "**")
        result = ""
        if "i" not in cmd:
            result = str(float(eval(cmd_python)))
        return interpreter, result

    def test_simple(self):
        interpreter, result = self.my_set_up("2 ^ 8")
        self.assertEqual(Rational(result),
                         interpreter.interpret_ret_token())

    def test_parenthesis(self):
        interpreter, result = self.my_set_up("(2 + 2) ^ 8")
        self.assertEqual(Rational(result),
                         interpreter.interpret_ret_token())

    def test_multi_parentesis(self):
        interpreter, result = self.my_set_up("(2 + 2) ^ (2 * 2)")
        self.assertEqual(Rational(result),
                         interpreter.interpret_ret_token())

    def test_multi_power(self):
        interpreter, result = self.my_set_up("2 ^ 2 ^ 2 ^ 2")
        self.assertEqual(Rational(result),
                         interpreter.interpret_ret_token())

    def test_power_imaginary(self):
        interpreter, _ = self.my_set_up("(2 + i) ^ 2")
        self.assertEqual(Imaginary(rational=3, imaginary=4),
                         interpreter.interpret_ret_token())

    def test_power_imaginary_2(self):
        interpreter, _ = self.my_set_up("(4 * i ) / (2 + i) ^ 2 ")
        self.assertEqual(Imaginary(rational=0.64, imaginary=0.48),
                         interpreter.interpret_ret_token())

    def test_imaginary_power(self):
        interpreter, _ = self.my_set_up("i ^ (2 + i)")
        self.assertRaises(InterpretException, interpreter.interpret_ret_token)

    def test_power_0(self):
        interpreter, result = self.my_set_up("2 ^ 0")
        self.assertEqual(Rational(result), interpreter.interpret_ret_token())

    def test_power_0_imaginary(self):
        interpreter, _ = self.my_set_up("i ^ 0")
        self.assertEqual(Rational("1"), interpreter.interpret_ret_token())


if __name__ == '__main__':
    unittest.main()
