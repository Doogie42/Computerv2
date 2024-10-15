from computorv2.input import read_input
from computorv2.Token import tokenize, TokenException
from computorv2.Parser import Parser, ParserException
from computorv2.Interpreter import Interpreter


def main():
    while True:
        cmd = read_input()
        if cmd == "exit":
            break
        try:
            token_list = tokenize(cmd)
        except TokenException:
            continue
        try:
            parser = Parser(token_list)
            ast = parser.generate()
        except ParserException as e:
            print(f"Parser exception {e}")
            continue
        interpreter = Interpreter(ast)
        result = interpreter.interpret()
        print(result)


if __name__ == "__main__":
    main()
