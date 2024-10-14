from Token import tokenize
from Parser import Parser
from Interpreter import Interpreter
import unittest


class TestInterpreter(unittest.TestCase):
    def my_set_up(self, cmd: str):
        token_list = tokenize(cmd)
        parser = Parser(token_list)
        ast = parser.generate()
        return ast

    def test_addition(self):
        ast = self.my_set_up("5 + 2")
        interpreter = Interpreter(ast)
        self.assertEqual("7", interpreter.interpret())

    def test_subtraction(self):
        ast = self.my_set_up("44 - 2")
        interpreter = Interpreter(ast)
        self.assertEqual("42", interpreter.interpret())

    def test_multiplication(self):
        ast = self.my_set_up("21 * 2")
        interpreter = Interpreter(ast)
        self.assertEqual("42", interpreter.interpret())

    def test_division(self):
        ast = self.my_set_up("84 / 2")
        interpreter = Interpreter(ast)
        self.assertEqual("42.0", interpreter.interpret())

    def test_precedence(self):
        ast = self.my_set_up("5 + 2 * 21")
        interpreter = Interpreter(ast)
        self.assertEqual("47", interpreter.interpret())

    def test_parenthesis(self):
        ast = self.my_set_up("(5 + 16) * 2")
        interpreter = Interpreter(ast)
        self.assertEqual("42", interpreter.interpret())


if __name__ == '__main__':
    unittest.main()
