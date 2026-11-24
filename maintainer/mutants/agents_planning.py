CASES = {
    "predict": {"prediction": ("compile", "test")},
    "contrast": {"contrast": ("package",)},
    "implement": {"plan": lambda graph: sorted(graph)},
    "break_cases": {"plan": lambda graph: sorted(graph)},
    "transfer": {"rebuild": lambda dependencies, changed: [changed]},
}
