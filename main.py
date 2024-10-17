from computorv2.input import read_input
from computorv2.Computor import Computor


def main():
    computor = Computor()
    while True:
        cmd = read_input()
        if cmd == "exit":
            break
        result = computor.run_cmd(cmd)
        print(f"{result}")


if __name__ == "__main__":
    main()
