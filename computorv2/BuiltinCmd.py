from abc import ABC, abstractmethod


class BuiltinCmd(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.short_name = ""

    @abstractmethod
    def execute(self):
        pass

    def get_short_name(self) -> str:
        return self.short_name


class ListVariable(BuiltinCmd):
    def __init__(self) -> None:
        super().__init__()
        self.short_name = "lv"

    def execute(self, computor) -> str:
        variable_dict = computor.get_variable_dict()
        if len(variable_dict) == 0:
            return "No variable found"
        s = "Variable list:\n"
        s += "*****************************\n"
        for name, variable in variable_dict.items():
            s += f"{name} = {variable}\n"
        s += "*****************************"
        return s


class test(BuiltinCmd):
    def __init__(self) -> None:
        super().__init__()
        self.short_name = "hello"

    def execute(self, computor) -> str:
        return "hello"
