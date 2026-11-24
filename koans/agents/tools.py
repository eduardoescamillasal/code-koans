"""Treat registration and permission as separate decisions.
Implement dispatch(registry, allowed, name, args). The registry maps names to
(schema, callable) pairs. Schema maps required field names to exact Python
types. Reject forbidden or unknown tools with PermissionError and bad arguments
with ValueError before invoking any callable. Invoke valid tools with kwargs.

For transfer, inspect a batch of simulated order requests (tool name, arguments).
Return an entry per request. Only preview is available in this workflow.
Use ("ok", result) on success and ("rejected", None) for authorization or
argument errors. Unexpected exceptions propagate. The supplied registry is
trusted and preview itself does not raise these validation exceptions.
"""

from koans import __

prediction = __
contrast = __


def dispatch(registry, allowed, name, args):
    raise AssertionError("Implement tools")


def preview_batch(registry, requests):
    raise AssertionError("Implement preview_batch")
