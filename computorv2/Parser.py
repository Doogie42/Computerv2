from computorv2.Token import Token, Operator, Rational, Parenthesis
from computorv2.Expression import Expression, Literal, Factor, Term


class ParserException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg


class Parser():
    def __init__(self, token_list: list[Token]) -> None:
        self.token_list = token_list
        self.current = 0
        self.expression_list = []

    def current_token(self) -> Token:
        if self.eotoken():
            raise ParserException("Expression ended prematurly")
        return self.token_list[self.current]

    def match_type(self, token: Token) -> bool:
        return self.current_token().get_type() == type(token)

    def match(self, token: Token) -> bool:
        return self.current_token() == token

    def eotoken(self) -> bool:
        return self.current >= len(self.token_list)

    def match_list(self, token_list: list[Token]) -> bool:
        if self.eotoken():
            return False
        for token in token_list:
            if self.current_token() == token:
                return True
        self.current_token() in token_list
        return False

    def match_consume(self, token: list[Token]) -> None:
        while self.token_list[self.current_token] not in token:
            self.current_token += 1

    def previous(self) -> Token:
        return self.token_list[self.current_token - 1]

    def advance(self, expect_type=None) -> Token:
        if self.eotoken():
            raise ParserException("End of token")
        if expect_type\
                and self.current_token().get_type() != expect_type:
            raise ParserException(f"Expected {expect_type} got \
                                  {self.current_token().get_type()}")
        self.current += 1
        return self.token_list[self.current - 1]

    def generate(self) -> Expression:
        result = self.parse()
        if not self.eotoken():
            raise ParserException(f"Error couldn't consume whole expression"
                                  f"last token was "
                                  f"{self.current_token()}")
        return result

    def parse(self) -> Expression:
        return self.term()

    def term(self) -> list[Expression]:
        left = self.factor()
        while self.match_list([Operator("+"), Operator("-")]):
            operator = Operator(self.advance(Operator))
            right = self.factor()
            left = Term(left, operator, right)
        return left

    def factor(self) -> list[Expression]:
        left = self.literal()

        while self.match_list([Operator("*"), Operator("/")]):
            operator = Operator(self.advance(Operator))
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
        raise ParserException(f"Invalid token got {self.current_token()}")
