from maintainer.references.deep_learning_autodiff import Value


class Constant(Value):
    def __add__(self, other):
        return Constant(self.data + other.data)

    def __mul__(self, other):
        return Constant(self.data * other.data)


class FirstPassOnly(Value):
    def __add__(self, other):
        return FirstPassOnly(self.data + other.data, ((self, 1), (other, 1)))

    def __mul__(self, other):
        return FirstPassOnly(self.data * other.data, ((self, other.data), (other, self.data)))

    def backward(self, seed=1.0):
        super().backward()

CASES = {
    "predict": {"prediction": 3},
    "contrast": {"contrast": 6},
    "implement": {"Value": Constant},
    "break_cases": {"Value": FirstPassOnly},
    "transfer": {"fit_slope": lambda samples, rate, steps: samples[0][1] / samples[0][0]},
}
