CASES = {
    "predict": {"prediction": False},
    "contrast": {"contrast": True},
    "implement": {"dispatch": lambda *args: None},
    "break_cases": {"dispatch": lambda registry, allowed, name, args: None},
    "transfer": {"preview_batch": lambda registry, requests: [("ok", None) for _ in requests]},
}
