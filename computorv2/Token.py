from abc import ABC
import re
import math
from computorv2.Exception import InterpretException
import enum
# literal : varA
# number : 4.34325 5i
# operator : * / = + - ** % ^
# parenthesis : varA * (5 + 2)
# function : func(x)
# matrixes : [[1, 2]; [2, 4]]
# = ?


class TokenType(enum.Enum):
    RATIONAL = 1
    IMAGINARY = 2
    OPERATOR = 3
    PARENTHESIS = 4
    FUNCTION = 5
    MATRIX = 6
    UNARY_OPERATOR = 7
    VARIABLE = 8
    EQUAL = 9


class TokenException(Exception):
    def __init__(self, msg):
        self.msg = msg


class Token(ABC):
    def __init__(self, value: str = None) -> None:
        super().__init__()
        self.token_type = None
        if value and not isinstance(value, str):
            raise Exception("Wrong type")
        self.value = value

    def __eq__(self, value: object) -> bool:
        return self.get_value() == value.get_value() and\
            self.get_type() == value.get_type()

    def get_value(self) -> str:
        return self.value

    def get_type(self) -> TokenType:
        return self.token_type

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{type(self).__name__} {self.value}"


class Number(Token):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)

    def __add__(self, rhs):
        if isinstance(self, Rational) and\
                isinstance(rhs, Rational):
            return Rational(str(self.rational_expr + rhs.rational_expr))
        else:
            rational = self.rational_expr + rhs.rational_expr
            imaginary = self.imaginary_expr + rhs.imaginary_expr
            if imaginary == 0:
                return Rational(str(rational))
            return Imaginary(rational=rational,
                             imaginary=imaginary)

    def __sub__(self, rhs):
        if isinstance(self, Rational) and\
                isinstance(rhs, Rational):
            return Rational(str(self.rational_expr - rhs.rational_expr))
        else:
            rational = self.rational_expr - rhs.rational_expr
            imaginary = self.imaginary_expr - rhs.imaginary_expr
            if imaginary == 0:
                return Rational(str(rational))
            return Imaginary(rational=rational,
                             imaginary=imaginary)

    # (a + ib) (c + id) = (ac - bd) + i(ad + bc).
    def __mul__(self, rhs):
        if isinstance(self, Rational) and\
                isinstance(rhs, Rational):
            return Rational(str(self.rational_expr * rhs.rational_expr))
        else:
            rational = self.rational_expr * rhs.rational_expr -\
                        self.imaginary_expr * rhs.imaginary_expr
            imaginary = self.rational_expr * rhs.imaginary_expr +\
                self.imaginary_expr * rhs.rational_expr
            if imaginary == 0:
                return Rational(str(rational))
            return Imaginary(rational=rational,
                             imaginary=imaginary)

    # (c + di ) / (a + bi) = ((ca+bd) / a^2+b^2) + ((ad−cb) / a^2+b^2) i
    def __truediv__(self, rhs):
        if isinstance(self, Rational) and\
                isinstance(rhs, Rational):
            if rhs.rational_expr == 0:
                raise ZeroDivisionError
            return Rational(str(self.rational_expr / rhs.rational_expr))
        else:
            denominator = rhs.rational_expr ** 2 + rhs.imaginary_expr ** 2
            if denominator == 0:
                raise ZeroDivisionError
            rational_part = self.rational_expr * rhs.rational_expr +\
                self.imaginary_expr * rhs.imaginary_expr
            rational_part = rational_part / denominator
            imaginary_part = rhs.rational_expr * self.imaginary_expr -\
                self.rational_expr * rhs.imaginary_expr
            imaginary_part = imaginary_part / denominator
            if imaginary_part == 0:
                return Rational(str(rational_part))
            return Imaginary(imaginary=imaginary_part,
                             rational=rational_part)
    # (a+ib)^N=r^N(cos(Nθ)+isin(Nθ))
    # and r = sqrt(a^2 + b ^ 2) and θ = arctan(b / a)

    def __pow__(self, rhs):
        if isinstance(rhs, Imaginary):
            raise InterpretException("Cannot use imaginary number in power")
        if isinstance(self, Rational):
            return Rational(str(self.rational_expr ** rhs.rational_expr))
        else:
            N = rhs.rational_expr
            if N == 0:
                return Rational("1")
            theta = math.atan(self.imaginary_expr / self.rational_expr)
            r = math.sqrt(self.imaginary_expr ** 2 + self.rational_expr ** 2)
            rational = r ** N * (math.cos(N * theta))
            imaginary = r ** N * (math.sin(N * theta))
            if (imaginary == 0):
                return Rational(str(rational))
            else:
                return Imaginary(rational=rational,
                                 imaginary=imaginary)

    def __mod__(self, rhs):
        if isinstance(self, Imaginary) or\
                isinstance(rhs, Imaginary):
            raise InterpretException("Cannot use imaginary number in modulo")
        if rhs.rational_expr == 0:
            raise InterpretException("Division by zero")
        return Rational(str(self.rational_expr % rhs.rational_expr))


class Rational(Number):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        if (value):
            self.rational_expr = float(self.value)
            self.imaginary_expr = 0
        self.token_type = TokenType.RATIONAL

    def get_rational_coefficient(self) -> str:
        return self.value

    def get_imaginary_coefficient(self) -> str:
        return ""

    def __str__(self) -> str:
        return f"{self.rational_expr:g}"


class Imaginary(Number):
    def __init__(self,
                 value: str = None,
                 rational: float = None,
                 imaginary: float = None) -> None:
        super().__init__(value)
        self.min_prec = 0.001
        self.token_type = TokenType.IMAGINARY

        # when we initialize our Imaginary we only get i
        # later when we do operation we can have 5 + i or 5 * i
        if (value):
            self.rational_expr = 0
            value = value.replace("i", "")
            if value == "":
                value = "1"
            self.imaginary_expr = float(value)
        else:
            self.rational_expr = rational
            self.imaginary_expr = imaginary
            self.value = None

    def get_rational_coefficient(self) -> str:
        # remove i from value
        return self.value[:len(self.value) - 1]

    def __str__(self) -> str:
        if self.value:
            return super().__repr__()
        else:
            sign = " + " if self.imaginary_expr >= 0 else " "
            s = ""
            if self.rational_expr != 0:
                s = f"{self.rational_expr:g}"
                s += sign
            if self.imaginary_expr != 0:
                s += f"{self.imaginary_expr:g}" + " * i"
            return s

    def __eq__(self, value: object) -> bool:
        diff_rat = abs(self.rational_expr - value.rational_expr)
        diff_imag = abs(self.imaginary_expr - value.imaginary_expr)
        return diff_rat < self.min_prec and diff_imag < self.min_prec
    pass


class Variable(Token):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        self.token_type = TokenType.VARIABLE


class Operator(Token):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        self.token_type = TokenType.OPERATOR


class Parenthesis(Token):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        self.token_type = TokenType.PARENTHESIS


class Function(Token):
    pass


class Matrix(Token):
    pass


class Equal(Token):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        self.token_type = TokenType.EQUAL


class UnaryOperator(Token):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        self.token_type = TokenType.UNARY_OPERATOR
    pass


def add_mult_operator(token_list: list[Token]) -> list[Token]:
    new_token_list = []
    iterable = iter(token_list)
    for token in iterable:
        new_token_list.append(token)
        try:
            next_token = next(iterable)
        except StopIteration:
            break
        if (token.get_type() == TokenType.RATIONAL or
            token.get_type() == TokenType.IMAGINARY)\
            and\
            (next_token.get_type() == TokenType.VARIABLE or
             next_token.get_value() == "("):
            new_token_list.append(Operator("*"))

        new_token_list.append(next_token)
    return new_token_list


def tokenize(cmd: str) -> list[Token]:
    rules = {
         "\\b\\d+\\.\\d+[i]\\b": Imaginary,  # capture decimal
         "\\b\\d*[i]\\b": Imaginary,  # capture whole
         "\\b\\d+(\\.\\d+)?": Rational,  # capture decimal
         "\\b(?!i\\b)[a-zA-Z]+\\b": Variable,
         "[\\+\\-\\*\\/]": Operator,
         "\\(|\\)": Parenthesis,
         "\\^|\\%": UnaryOperator,
         "=": Equal
    }

    token_list = []
    while len(cmd) > 0 and not cmd.isspace():
        rule_found = False
        for rule, token in rules.items():
            match = re.match(rule, cmd)
            if match:
                token_list.append(token(match[0]))
                cmd = cmd[match.span()[1]:].lstrip()
                rule_found = True
                break
        if rule_found:
            continue
        if len(cmd) == 0 or cmd.isspace():
            break
        raise TokenException(f"unkown token {cmd.split()[0]}")
    token_list = add_mult_operator(token_list)
    return token_list
