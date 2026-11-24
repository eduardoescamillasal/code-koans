prediction = 6.0
contrast = 3.0


class Value:
    def __init__(self, data, edges=()):
        self.data = data
        self.grad = 0.0
        self._edges = edges

    def __add__(self, other):
        return Value(self.data + other.data, ((self, 1), (other, 1)))

    def __mul__(self, other):
        return Value(self.data * other.data, ((self, other.data), (other, self.data)))

    def backward(self, seed=1.0):
        order = []
        seen = set()
        stack = [(self, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                order.append(node)
            elif node not in seen:
                seen.add(node)
                stack.append((node, True))
                stack.extend((parent, False) for parent, _ in node._edges)

        for node in order:
            node.grad = 0.0
        self.grad = seed
        for node in reversed(order):
            for parent, local in node._edges:
                parent.grad += local * node.grad


def fit_slope(samples, rate, steps):
    weight = 0.0
    for _ in range(steps):
        parameter = Value(weight)
        loss = Value(0)
        for feature, target in samples:
            error = parameter * Value(feature) + Value(-target)
            loss = loss + error * error
        loss.backward()
        weight -= rate * parameter.grad
    return weight
