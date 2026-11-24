CASES = {
    "predict": {"prediction": -6},
    "contrast": {"contrast": 0},
    "implement": {"diagnose": lambda trace: "loss decreasing"},
    "break_cases": {"diagnose": lambda trace: "check learning rate"},
    "transfer": {"training_report": lambda rate: ("final", "loss decreasing", [])},
}
