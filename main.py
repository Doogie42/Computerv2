from input import read_input
from Token import tokenize

def main():
    # while True:
        # cmd = read_input()
        # if cmd == "exit":
        #     break
        cmd = "2 * 21 * 4"
        token_list = tokenize(cmd)
        print(token_list)

if __name__ == "__main__":
    main()