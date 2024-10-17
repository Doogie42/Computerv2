from computorv2.Token import tokenize, Rational, Imaginary, Variable, \
                                Operator, Parenthesis, TokenException, \
                                UnaryOperator, Equal
import unittest


class TestRational(unittest.TestCase):
    def test_rational(self):
        token_list = tokenize("4242")
        self.assertListEqual([Rational("4242")], token_list)

    def test_rational_decimal(self):
        token_list = tokenize("42.42")
        self.assertListEqual([Rational("42.42")], token_list)

    def test_rational_leading_dot(self):
        self.assertRaises(TokenException, tokenize, ".42")

    def test_rational_trailing_dot(self):
        self.assertRaises(TokenException, tokenize, "42.")

    def test_rational_double_dot(self):
        self.assertRaises(TokenException, tokenize, "42.42.")

    def test_rational_double_dot_with_number(self):
        self.assertRaises(TokenException, tokenize, "42.42.42")


class TestImaginary(unittest.TestCase):
    def test_imaginary(self):
        token_list = tokenize("4242i")
        self.assertListEqual([Imaginary("4242i")], token_list)

    def test_imaginary_list(self):
        token_list = tokenize("4242i 2121i")
        self.assertListEqual([Imaginary("4242i"), Imaginary("2121i")],
                             token_list)

    def test_imaginary_i_alone(self):
        self.assertListEqual([Imaginary("i")], tokenize("i"))

    def test_imaginary_decimal(self):
        self.assertListEqual([Imaginary("42.42i")], tokenize("42.42i"))

    def test_imaginary_leading_dot(self):
        self.assertRaises(TokenException, tokenize, ".42i")

    def test_imaginary_trailing_dot(self):
        self.assertRaises(TokenException, tokenize, "42.i")

    def test_imaginary_double_dot(self):
        self.assertRaises(TokenException, tokenize, "42.42.i")

    def test_imaginary_i_between(self):
        self.assertRaises(TokenException, tokenize, "42i42")

    def test_imaginary_decimal_i_between(self):
        self.assertRaises(TokenException, tokenize, "42i.4242")


class TestVariable(unittest.TestCase):
    def test_variable(self):
        token_list = tokenize("variable")
        self.assertListEqual([Variable("variable")], token_list)

    def test_variable_list(self):
        token_list = tokenize("variable variableA")
        self.assertListEqual([Variable("variable"), Variable("variableA")],
                             token_list)

    def test_variable_with_bad_char(self):
        self.assertRaises(TokenException, tokenize, "variable1")


class TestOperator(unittest.TestCase):
    def test_operator(self):
        token_list = tokenize("+")
        self.assertListEqual([Operator("+")], token_list)

    def test_operator_list(self):
        token_list = tokenize("+ - * /")
        self.assertListEqual([Operator("+"), Operator("-"),
                              Operator("*"), Operator("/")], token_list)

    def test_operator_no_space(self):
        self.assertEqual([Operator("*"), Operator("*")], tokenize("**"))


class TestPower(unittest.TestCase):
    def test_power(self):
        token_list = tokenize("^")
        self.assertListEqual([UnaryOperator("^")], token_list)

    def test_power_numbe(self):
        token_list = tokenize("2 ^ 2")
        self.assertListEqual([Rational("2"), UnaryOperator("^"),
                              Rational("2")], token_list)


class TestMixed(unittest.TestCase):
    def test_mixed(self):
        token_list = tokenize("4242 4242i variable = 42")
        self.assertListEqual([Rational("4242"), Imaginary("4242i"),
                              Variable("variable"), Equal("="),
                              Rational("42")], token_list)

    def test_mixed_with_bad_char(self):
        self.assertRaises(TokenException, tokenize, "abc32 variable")

    def test_many_space(self):
        token_list = tokenize("4242  4242i   \t \t variable")
        self.assertListEqual([Rational("4242"), Imaginary("4242i"),
                              Variable("variable")], token_list)

    def test_with_parenthesis(self):
        token_list = tokenize("(4242 + 4242i) * variable")
        self.assertListEqual([Parenthesis("("), Rational("4242"),
                              Operator("+"), Imaginary("4242i"),
                              Parenthesis(")"), Operator("*"),
                              Variable("variable")], token_list)

    def test_factor_no_operator(self):
        token_list = tokenize("42x")
        self.assertListEqual([Rational("42"), Operator("*"),
                              Variable("x")], token_list)

    def test_factor_two_i(self):
        token_list = tokenize("42ii")
        self.assertListEqual([Rational("42"), Operator("*"),
                              Variable("ii")], token_list)

    def test_factor_parenthesis(self):
        token_list = tokenize("42(x)")
        self.assertListEqual([Rational("42"), Operator("*"), Parenthesis("("),
                              Variable("x"), Parenthesis(")")], token_list)

    def test_factor_parenthesis_i(self):
        token_list = tokenize("42(i)")
        self.assertListEqual([Rational("42"), Operator("*"), Parenthesis("("),
                              Imaginary("i"), Parenthesis(")")], token_list)

    def test_factor_parenthesis_i_between(self):
        # here i42 can be a variable or i * 42 => we raise exception
        self.assertRaises(TokenException, tokenize, "42i42")


if __name__ == '__main__':
    unittest.main()
