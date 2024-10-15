from computorv2.Expression import Expression


class Interpreter():
    def __init__(self, expression: Expression) -> None:
        self.expression = expression
        pass

    def interpret(self) -> str:
        self.result = self.expression.evaluate()
        return self.result.get_value()
