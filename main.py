from computorv2.input import read_input
from computorv2.Token import tokenize, TokenException
from computorv2.Parser import Parser, ParserException
from computorv2.Interpreter import Interpreter
from computorv2.Expression import InterpretException


def main():
    while True:
        cmd = read_input()
        if cmd == "exit":
            break
        try:
            token_list = tokenize(cmd)
        except TokenException as e:
            print(f"Token exception {e}")
            continue
        try:
            parser = Parser(token_list)
            ast = parser.generate()
        except ParserException as e:
            print(f"Parser exception {e}")
            continue
        interpreter = Interpreter(ast)
        try:
            result = interpreter.interpret_ret_token()
        except InterpretException as e:
            print(f"Interpret exception {e}")
            continue

        print(f"RESULT {result}")


if __name__ == "__main__":
    main()
