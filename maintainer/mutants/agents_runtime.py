from maintainer.references.agents_runtime import reserve_stock, run


def discard_events(*args, **kwargs):
    status, text, _ = run(*args, **kwargs)
    return status, text, []


def drop_duplicate_guard(model, parse, execute, **kwargs):
    counter = 0

    def parse_as_unique(raw):
        nonlocal counter
        event = parse(raw)
        if event["type"] == "call":
            counter += 1
            event["id"] = str(counter)
        return event

    return run(model, parse_as_unique, execute, **kwargs)


def accept_boolean(stock, model, parse, **kwargs):
    def coerce(raw):
        event = parse(raw)
        if event["type"] == "call" and type(event["args"].get("qty")) is bool:
            event["args"]["qty"] = int(event["args"]["qty"])
        return event

    return reserve_stock(stock, model, coerce, **kwargs)


CASES = {
    "predict": {"prediction": ("system", "document")},
    "contrast": {"contrast": ("system", "system")},
    "implement": {"run": discard_events},
    "break_cases": {"run": drop_duplicate_guard},
    "transfer": {"reserve_stock": accept_boolean},
}
