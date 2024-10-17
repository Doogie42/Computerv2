from abc import ABC
from computorv2.Token import Token, Operator, UnaryOperator, Imaginary
from computorv2.Exception import InterpretException


class Expression(ABC):
    def __init__(self) -> None:
        super().__init__()

    def get_value(self):
        return self.value.get_value()


# number / Variable / function / matrixe / parenthesis
class Literal(Expression):
    def __init__(self, value: Token) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return self.value.__str__()

    def __repr__(self) -> str:
        return self.value.get_value()

    def get_token(self) -> Token:
        return self.value

    def __add__(self, rhs):
        return Literal(self.get_token() + rhs.get_token())

    def __sub__(self, rhs):
        return Literal(self.get_token() - rhs.get_token())

    def __mul__(self, rhs):
        return Literal(self.get_token() * rhs.get_token())

    def __truediv__(self, rhs):
        return Literal(self.get_token() / rhs.get_token())

    def __pow__(self, rhs):
        return Literal(self.get_token() ** rhs.get_token())

    def __mod__(self, rhs):
        return Literal(self.get_token() % rhs.get_token())


# % ^
class Unary(Expression):
    def __init__(self,
                 left: Expression,
                 unary: UnaryOperator,
                 right: Expression) -> None:
        self.left = left
        self.right = right
        self.unary = unary

    def evaluate(self) -> Literal:
        if type(self.right) is not Literal:
            self.right = self.right.evaluate()
        if type(self.left) is not Literal:
            self.left = self.left.evaluate()
        if self.unary == UnaryOperator("^"):
            if isinstance(self.right, Imaginary):
                raise InterpretException(
                    "Cannot use imaginary number in power")
            return self.left ** self.right
        elif self.unary == UnaryOperator("%"):
            return self.left % self.right


# + - * / =
class Binary(Expression):
    def __init__(self,
                 left: Expression,
                 operator: Operator,
                 right: Expression) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        return f"left :\n{self.left} op {self.operator} right {self.right}\n"

    def evaluate(self) -> Literal:
        if type(self.left) is not Literal:
            self.left = self.left.evaluate()

        if type(self.right) is not Literal:
            self.right = self.right.evaluate()

        match self.operator:
            case Operator(value="+"):
                return self.left + self.right
            case Operator(value="-"):
                return self.left - self.right
            case Operator(value="*"):
                return self.left * self.right
            case Operator(value="/"):
                try:
                    return self.left / self.right
                except ZeroDivisionError:
                    raise InterpretException("Division by 0")
            case _: raise InterpretException("Unknown operator")


# * /
class Factor(Binary):
    pass


# + -
class Term(Binary):
    pass
