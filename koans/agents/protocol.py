"""Treat a model response as an untrusted JSON message with an exact schema.
Accept either {"type":"final","text":string} or a call with type "call", a
nonempty string id, a nonempty string name, and an args object containing only
flat JSON scalars. Reject duplicate keys anywhere, unknown fields, non-finite
numbers, invalid JSON, and non-string input with ValueError. Never execute text.

For transfer, an archive stores replies from completed sessions. Extract final
text in order and ignore valid call messages. Propagate validation errors to
avoid returning an apparently complete archive of malformed replies.
"""

import json
from collections.abc import Iterable
import math
from typing import Literal, TypedDict
from unittest import TestCase

from koans import Exercise, __, todo


def predict(t: TestCase, *answers: object) -> None:
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, json.loads('{"limit":1,"limit":9}')["limit"])


def contrast(t: TestCase, *answers: object) -> None:
    grouped = json.loads('{"limit":1,"limit":9}', object_pairs_hook=list)
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, grouped)


Scalar = bool | int | float | str | None


class FinalMessage(TypedDict):
    type: Literal["final"]
    text: str


class ToolCall(TypedDict):
    type: Literal["call"]
    id: str
    name: str
    args: dict[str, Scalar]


Message = FinalMessage | ToolCall


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        # json.loads normally discards earlier values for a duplicate key.
        todo("reject duplicates and keep the current field")
    return result


def _valid_argument(value: object) -> bool:
    if type(value) is float:
        return math.isfinite(value)
    todo("accept the remaining flat JSON scalar types")


def parse(raw: object) -> Message:
    if not isinstance(raw, str):
        raise ValueError("expected text")
    try:
        decoded = json.loads(raw, object_pairs_hook=_unique_object)
    except RecursionError as error:
        raise ValueError("excessive nesting") from error
    if not isinstance(decoded, dict):
        raise ValueError("message must be an object")
    if decoded.get("type") == "final":
        todo("validate the exact final-message fields")
    if decoded.get("type") == "call":
        todo("validate the call fields and each argument with _valid_argument")
    raise ValueError("unknown message type")


def archive_text(replies: Iterable[str]) -> list[str]:
    archive: list[str] = []
    # Narrow the union using its type field before reading text.
    todo("validate every reply and collect final text in order")


def practice(t: TestCase, exercise: Exercise) -> None:
    t.assertEqual(exercise.parse('{"type":"final","text":"ok"}'), {"type": "final", "text": "ok"})
    with t.assertRaises(ValueError):
        exercise.parse('{"type":"final","text":7}')


def practice_break(t: TestCase, exercise: Exercise) -> None:
    with t.assertRaises(ValueError):
        exercise.parse('{"type":"call","id":"a","name":"read","args":{"limit":1,"limit":2}}')


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    replies = ['{"type":"call","id":"a","name":"read","args":{}}',
               '{"type":"final","text":"ready"}']
    t.assertEqual(exercise.archive_text(replies), ["ready"])
