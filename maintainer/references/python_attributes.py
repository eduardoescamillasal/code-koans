prediction = "local"
contrast = "computed"


def bounded_int(low, high):
    class BoundedInt:
        def __set_name__(self, owner, name):
            self.name = name

        def __get__(self, instance, owner):
            if instance is None:
                return self
            try:
                return instance.__dict__[self]
            except KeyError:
                raise AttributeError(self.name) from None

        def __set__(self, instance, value):
            if type(value) is not int or not low <= value <= high:
                raise ValueError(self.name)
            instance.__dict__[self] = value

    return BoundedInt()


def reading_type(schema):
    fields = {name: bounded_int(low, high) for name, (low, high) in schema.items()}
    return type("Reading", (), fields)
