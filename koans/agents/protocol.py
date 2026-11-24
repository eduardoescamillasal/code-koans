"""Treat a model response as an untrusted JSON message with an exact schema.
Accept either {"type":"final","text":string} or a call with type "call", a
nonempty string id, a nonempty string name, and an args object containing only
flat JSON scalars. Reject duplicate keys anywhere, unknown fields, non-finite
numbers, invalid JSON, and non-string input with ValueError. Never execute text.

For transfer, an archive stores replies from completed sessions. Extract final
text in order and ignore valid call messages. Propagate validation errors to
avoid returning an apparently complete archive of malformed replies.
"""

from koans import __

prediction = __
contrast = __


def parse(raw):
    raise AssertionError("Implement protocol")


def archive_text(replies):
    raise AssertionError("Implement archive_text")
