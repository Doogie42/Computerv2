from computorv2.input import read_input
from computorv2.Token import tokenize
from computorv2.Parser import Parser
from computorv2.Interpreter import Interpreter


def main():
    while True:
        cmd = read_input()
        if cmd == "exit":
            break
        token_list = tokenize(cmd)
        parser = Parser(token_list)
        ast = parser.generate()
        interpreter = Interpreter(ast)
        result = interpreter.interpret()
        print(result)


if __name__ == "__main__":
    main()
