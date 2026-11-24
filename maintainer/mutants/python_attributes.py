class SharedField:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance, value):
        self.value = value


CASES = {
    "predict": {"prediction": "computed"},
    "contrast": {"contrast": "local"},
    "implement": {"bounded_int": lambda *args: SharedField()},
    "break_cases": {"bounded_int": lambda *args: object()},
    "transfer": {"reading_type": lambda schema: type("Reading", (), {})},
}
