def read_input() -> str:
    try:
        return input("cv2> ")
    except KeyboardInterrupt:
        return "exit"
    except Exception:
        return "exit"
