import json
import math

prediction = 9
contrast = [("limit", 1), ("limit", 9)]


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate key")
        obj[key] = value
    return obj


def parse(raw):
    if not isinstance(raw, str):
        raise ValueError("expected text")
    try:
        msg = json.loads(raw, object_pairs_hook=unique_object)
    except RecursionError as error:
        raise ValueError("excessive nesting") from error
    if isinstance(msg, dict):
        if msg.keys() == {"type", "text"} and msg["type"] == "final" and isinstance(msg["text"], str):
            return msg
        if (msg.keys() == {"type", "id", "name", "args"} and msg["type"] == "call"
                and all(isinstance(msg[key], str) and msg[key] for key in ("id", "name"))
                and isinstance(msg["args"], dict)):
            if all(value is None or type(value) in (bool, str, int)
                   or (type(value) is float and math.isfinite(value)) for value in msg["args"].values()):
                return msg
    raise ValueError("invalid message")


def archive_text(replies):
    texts = []
    for raw in replies:
        msg = parse(raw)
        if msg["type"] == "final":
            texts.append(msg["text"])
    return texts
