from Token import Token, Operator, Rational, Parenthesis
from Expression import Expression, Literal, Factor, Term


class Parser():
    def __init__(self, token_list: list[Token]) -> None:
        self.token_list = token_list
        self.current = 0
        self.expression_list = []

    def match_type(self, token: Token) -> bool:
        return self.token_list[self.current].get_type() == type(token)

    def match(self, token: Token) -> bool:
        return self.token_list[self.current] == token

    def eotoken(self) -> bool:
        return self.current >= len(self.token_list)

    def match_list(self, token_list: list[Token]) -> bool:
        if self.eotoken():
            return False
        for token in token_list:
            if self.token_list[self.current] == token:
                return True
        self.token_list[self.current] in token_list
        return False

    def match_consume(self, token: list[Token]) -> None:
        while self.token_list[self.current_token] not in token:
            self.current_token += 1

    def previous(self) -> Token:
        return self.token_list[self.current_token - 1]

    def advance(self) -> Token:
        if self.eotoken():
            raise Exception("End of token")
        self.current += 1
        return self.token_list[self.current - 1]

    def generate(self) -> Expression:
        return self.parse()

    def parse(self) -> Expression:
        return self.term()

    def term(self) -> list[Expression]:
        left = self.factor()
        while self.match_list([Operator("+"), Operator("-")]):
            operator = Operator(self.advance())
            right = self.factor()
            left = Term(left, operator, right)
        return left

    def factor(self) -> list[Expression]:
        left = self.literal()

        while self.match_list([Operator("*"), Operator("/")]):
            operator = Operator(self.advance())
            right = self.literal()
            left = Factor(left, operator, right)

        return left

    def literal(self):
        if (self.match_type(Rational())):
            return Literal(self.advance())

        if (self.match(Parenthesis("("))):
            self.advance()
            expression = self.parse()
            self.advance()
            return expression
