from abc import ABC
import re

# literal : varA
# number : 4.34325 5i
# operator : * / = + - ** % ^
# parenthesis : varA * (5 + 2)
# function : func(x)
# matrixes : [[1, 2]; [2, 4]]
# = ?


class TokenException(Exception):
    def __init__(self, msg):
        self.msg = msg


class Token(ABC):
    def __init__(self, value: str = None) -> None:
        super().__init__()
        self.value = value

    def __eq__(self, value: object) -> bool:
        return self.get_value() == value.get_value() and\
            type(self) is type(value)

    def get_value(self) -> str:
        return self.value

    def get_type(self) -> type:
        return type(self)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{type(self).__name__} {self.value}"


class Rational(Token):
    pass


class Imaginary(Token):
    pass


class Variable(Token):
    pass


class Operator(Token):
    pass


class Parenthesis(Token):
    pass


class Function(Token):
    pass


class Matrix(Token):
    pass


def tokenize(cmd: str) -> list[Token]:
    rules = {
         "\\b\\d+\\.\\d+[i]\\b": Imaginary,  # capture decimal
         "\\b\\d*[i]\\b": Imaginary,  # capture whole
         "\\b\\d+(\\.\\d+)?\\b": Rational,  # capture decimal
         "\\b(?!i\\b)[a-zA-Z]+\\b": Variable,
         "[\\+\\-\\*\\/\\%\\=\\^]": Operator,
         "\\(|\\)": Parenthesis,
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
    return token_list
