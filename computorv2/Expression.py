from abc import ABC
from computorv2.Token import Token, Operator

# term -> factor (- + ) factor
# factor -> unary (* /) unary
# unary -> % | ^ | literal
# Literal -> Number | variable | matrix | ( expression )


class InterpretException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg


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


# % ^
class Unary(Expression):
    pass


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
        if type(self.left) is Factor:
            self.left = self.left.evaluate()
        elif type(self.left) is Term:
            self.left = self.left.evaluate()
        if type(self.right) is Factor:
            self.right = self.right.evaluate()
        elif type(self.right) is Term:
            self.right = self.right.evaluate()
        # TODO: Implement the evaluation of the expression
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
