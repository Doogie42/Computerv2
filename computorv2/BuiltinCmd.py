from abc import ABC, abstractmethod


class BuiltinCmd(ABC):
    def __init__(self) -> None:
        super().__init__()
        pass

    @abstractmethod
    def execute(self):
        pass


class ListVariable(BuiltinCmd):
    def execute(self, computor) -> str:
        variable_dict = computor.get_variable_dict()
        s = ""
        for name, variable in variable_dict.items():
            s += f"{name} = {variable}\n"
        s = s[:-1]  # renove last \n
        return s
