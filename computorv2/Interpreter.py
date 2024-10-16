from computorv2.Expression import Expression
from computorv2.Expression import Token


class Interpreter():
    def __init__(self, expression: Expression) -> None:
        self.expression = expression
        pass

    def interpret(self) -> str:
        self.result = self.expression.evaluate()
        return self.result

    def interpret_ret_token(self) -> Token:
        self.result = self.expression.evaluate()
        return self.result.get_token()
