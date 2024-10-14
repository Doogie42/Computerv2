from input import read_input
from Token import tokenize
from Parser import Parser
from Interpreter import Interpreter


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
