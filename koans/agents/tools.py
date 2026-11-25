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

    def test_registration_and_permission_are_independent(self) -> None:
        registered = {"read", "write"}
        allowed = {"read", "export"}
        self.assertEqual(__, "write" in registered and "write" in allowed)
        self.assertEqual(__, "export" in registered and "export" in allowed)
        self.assertEqual(__, "read" in registered and "read" in allowed)

    def test_an_extra_argument_is_a_schema_mismatch(self) -> None:
        required = {"quantity": int}
        valid = {"quantity": 2}
        extra = {"quantity": 2, "destination": "other"}
        self.assertEqual(__, valid.keys() == required.keys())
        self.assertEqual(__, extra.keys() == required.keys())

    def test_building_keyword_arguments_does_not_invoke_a_tool(self) -> None:
        seen: list[int] = []

        def lookup(key: int) -> int:
            seen.append(key)
            return key * 10

        args = {"key": 3}
        self.assertEqual(__, seen.copy())
        self.assertEqual(__, lookup(**args))
        self.assertEqual(__, seen)


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
