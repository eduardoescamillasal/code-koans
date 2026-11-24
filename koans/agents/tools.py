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

from collections.abc import Callable, Iterable, Mapping, Set
from typing import Literal

from koans import Koan, __, todo


class AboutToolPermissions(Koan):
    def test_booleans_are_integer_instances(self) -> None:
        self.assertEqual(__, isinstance(True, int))

    def test_exact_types_reject_booleans_as_integers(self) -> None:
        self.assertEqual(__, type(True) is int)

    def test_a_registered_tool_still_needs_permission(self) -> None:
        def preview(qty: int) -> int:
            return qty + 2

        registry = {"preview": ({"qty": int}, preview)}
        self.assertEqual(dispatch(registry, {"preview"}, "preview", {"qty": 5}), 7)
        with self.assertRaises(PermissionError):
            dispatch(registry, set(), "preview", {"qty": 5})

    def test_invalid_arguments_do_not_invoke_a_tool(self) -> None:
        invoked: list[int] = []

        def write(count: int) -> None:
            invoked.append(count)

        with self.assertRaises(ValueError):
            dispatch({"write": ({"count": int}, write)}, {"write"}, "write", {"count": True})
        self.assertEqual(invoked, [])

    def test_preview_results_distinguish_rejection(self) -> None:
        registry: Registry = {"preview": ({"qty": int}, lambda qty: abs(qty))}
        batch = [("preview", {"qty": -4}), ("missing", {})]
        self.assertEqual(preview_batch(registry, batch), [("ok", 4), ("rejected", None)])


Registry = Mapping[str, tuple[Mapping[str, type], Callable[..., object]]]
Arguments = Mapping[str, object]
Outcome = tuple[Literal["ok", "rejected"], object]


def dispatch(registry: Registry, allowed: Set[str], name: str, args: Arguments) -> object:
    if name not in allowed or name not in registry:
        raise PermissionError("tool unavailable")
    schema, tool = registry[name]
    # A value like True is an int subclass, but the schema requires exact types.
    todo("validate argument names and exact types before calling the tool")


def preview_batch(registry: Registry, requests: Iterable[tuple[str, Arguments]]) -> list[Outcome]:
    outcomes: list[Outcome] = []
    for name, args in requests:
        todo("dispatch one read-only request and distinguish rejection from success")
    return outcomes
