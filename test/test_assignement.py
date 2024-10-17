from computorv2.Token import Imaginary, Rational
from computorv2.Computor import Computor
import unittest


class TestAssignement(unittest.TestCase):
    def my_set_up(self, cmd: str):
        computor = Computor()
        computor.run_cmd(cmd)
        return computor

    def test_simple(self):
        computor = self.my_set_up("a = 2 + 2")
        variable_dict = computor.get_variable_dict()
        self.assertDictEqual(variable_dict, {"a": Rational("4.0")})

    def test_reassign(self):
        computor = self.my_set_up("a = 2 + 2")
        computor.run_cmd("a = 3 + 4")
        variable_dict = computor.get_variable_dict()
        self.assertDictEqual(variable_dict, {"a": Rational("7.0")})

    def test_assign_imaginary(self):
        computor = self.my_set_up("a = 2 + i")
        variable_dict = computor.get_variable_dict()
        self.assertDictEqual(variable_dict, {"a": Imaginary(rational=2,
                                                            imaginary=1)})

    def test_reassign_imaginary(self):
        computor = self.my_set_up("a = 2 + 2")
        computor.run_cmd("a = 3 + i")
        variable_dict = computor.get_variable_dict()
        self.assertDictEqual(variable_dict, {"a": Imaginary(rational=3,
                                                            imaginary=1)})

    def test_mix(self):
        computor = self.my_set_up("a = 2 + 2")
        computor.run_cmd("a = 3 + i")
        variable_dict = computor.get_variable_dict()
        self.assertDictEqual(variable_dict, {"a": Imaginary(rational=3,
                                                            imaginary=1)})

    def test_assign_var(self):
        computor = self.my_set_up("a = 2 + 2")
        computor.run_cmd("b = a + 2i")
        computor.run_cmd("c = a + b")
        variable_dict = computor.get_variable_dict()
        self.assertDictEqual(variable_dict, {
            "a": Rational("4.0"),
            "b": Imaginary(rational=4, imaginary=2),
            "c": Imaginary(rational=8, imaginary=2)
            })

    def test_precedence(self):
        computor = self.my_set_up("a = 2 + i")
        computor.run_cmd("b = a ^ 2")
        variable_dict = computor.get_variable_dict()
        self.assertDictEqual(variable_dict, {
            "a": Imaginary(rational=2, imaginary=1),
            "b": Imaginary(rational=3, imaginary=4)
            })
