from abc import ABC
from computorv2.Token import Token, Rational, Operator

# term -> factor (- + ) factor
# factor -> unary (* /) unary
# unary -> % | ^ | primary
# Literal -> Number | variable | matrix | ( expression )


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

    def __repr__(self) -> str:
        return self.value.get_value()


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
        result = eval(f"{self.left.get_value()} {self.operator.get_value()}\
                      {self.right.get_value()}")
        return Rational(str(result))


# =
class Equality(Expression):
    def __init__(self, value: Token) -> None:
        self.value = value.get_value()

    def __repr__(self) -> str:
        return self.value
    pass


# * /
class Factor(Binary):
    pass


# + -
class Term(Binary):
    pass
