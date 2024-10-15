import unittest
from computorv2.Token import tokenize
from computorv2.Parser import Parser, ParserException


class TestParserException(unittest.TestCase):
    def my_set_up(self, cmd: str):
        token_list = tokenize(cmd)
        parser = Parser(token_list)
        return parser

    def test_leading_operator(self):
        cmd = "+ 1"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_trailing_operator(self):
        cmd = "1 +"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_double_operator(self):
        cmd = "1 + + 1"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_no_operator(self):
        cmd = "1 1"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_no_operand(self):
        cmd = "+"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_no_closing_parenthesis(self):
        cmd = "(1 + 1"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_no_opening_parenthesis(self):
        cmd = "1 + 1)"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_too_many_closing_parenthesis(self):
        cmd = "(1 + 1))"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_too_many_opening_parentesis(self):
        cmd = "((1 + 1)"
        parser = self.my_set_up(cmd)
        self.assertRaises(ParserException, parser.generate)

    def test_no_exception(self):
        cmd = "1 + 1"
        parser = self.my_set_up(cmd)
        parser.generate()
