from maintainer.references.python_special_methods import Vector


class ReusesLeft(Vector):
    def __add__(self, other):
        return self


class Truncates(Vector):
    def __add__(self, other):
        return Vector(*(a + b for a, b in zip(self.coordinates, other.coordinates)))


class AddsProductsIncorrectly(Vector):
    def __matmul__(self, other):
        return sum(self.coordinates) * sum(other.coordinates)


CASES = {
    "predict": {"prediction": ['init', 'new']},
    "contrast": {"contrast": ('seven', 'Cell(7)', '[seven]')},
    "implement": {"Vector": ReusesLeft},
    "break_cases": {"Vector": Truncates},
    "transfer": {"Vector": AddsProductsIncorrectly},
}
