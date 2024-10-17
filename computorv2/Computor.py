from computorv2.Token import tokenize, TokenException, TokenType, Token
from computorv2.Parser import Parser, ParserException
from computorv2.Interpreter import Interpreter
from computorv2.Expression import InterpretException
from computorv2.BuiltinCmd import BuiltinCmd


class Computor():
    def __init__(self) -> None:
        self.variable_dict = {}

    def get_variable_dict(self) -> dict[str, Token]:
        return self.variable_dict

    def split_token_equal(self, token_list):
        self.token_before_equal = []
        self.token_after_equal = []
        before_equal = True
        for token in token_list:
            if token.get_type() == TokenType.EQUAL:
                if before_equal is False:
                    raise ParserException("Multi = sign detected")
                before_equal = False
                continue
            if before_equal:
                self.token_before_equal.append(token)
            else:
                self.token_after_equal.append(token)

    def run_builtin_cmd(self, cmd: str) -> str:
        builtin_list = BuiltinCmd.__subclasses__()
        for builtin in builtin_list:
            if cmd.lower() == builtin.__name__.lower():
                b = builtin()
                return b.execute(self)
        return ""

    def run_cmd(self, cmd: str) -> str:
        ret = self.run_builtin_cmd(cmd)
        if ret != "":
            return ret
        try:
            token_list = tokenize(cmd)
            self.split_token_equal(token_list)
            # No = => we interpret as whole expression
            token_list_to_parse = []
            assign_mode = False
            if len(self.token_before_equal) == len(token_list):
                token_list_to_parse = token_list
            elif len(self.token_before_equal) == 1:
                token_list_to_parse = self.token_after_equal
                assign_mode = True
            else:
                raise ParserException("Unknown equality")
            parser = Parser(token_list_to_parse)
            ast = parser.generate()
            interpreter = Interpreter(ast)
            result = interpreter.interpret_ret_token()
            if assign_mode:
                var_token = self.token_before_equal[0]
                if var_token.get_type() == TokenType.VARIABLE:
                    self.variable_dict[var_token.get_value()] = result

        except TokenException as e:
            return f"Token exception {e}"
        except ParserException as e:
            return f"Parser exception {e}"
        except InterpretException as e:
            return f"Interpret exception {e}"
        except Exception as e:
            print(f"ERROR FATAL: unhandled exception got {e}")
            print("Quitting")
            exit(1)
        return result