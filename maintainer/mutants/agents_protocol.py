CASES = {
    "predict": {"prediction": 1},
    "contrast": {"contrast": [("limit", 9)]},
    "implement": {"parse": lambda raw: {"type": "final", "text": raw}},
    "break_cases": {"parse": lambda raw: {}},
    "transfer": {"archive_text": lambda replies: list(replies)},
}
