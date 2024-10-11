import sys

def read_input() ->str:
    try:
        return input("cv2> ")
    except Exception:
        return "exit"