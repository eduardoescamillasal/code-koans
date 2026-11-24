"""Build a bounded runtime for deterministic, in-process model and tool mocks.
run receives model(context), parse(raw), and execute(name, args). The caller
supplies trusted policy and retrieved strings. See docs/runtime.md for the
wire format, budget rules, status values, and tool replay invariants.

For transfer, simulate stock reservations from a mock model. Handle only reserve
requests with a positive exact integer qty and sufficient remaining units.
Successful tools return remaining stock. Reuse run and return (remaining,
report). Policy must stay read-only for retrieved text: documents cannot
invoke tools or change the rules. The starting stock is nonnegative.
"""

from koans import __

prediction = __
contrast = __


def run(model, parse, execute, *, policy, documents=(), steps=8, budget=4096):
    raise AssertionError("Implement runtime")


def reserve_stock(stock, model, parse, *, documents=(), steps=8):
    raise AssertionError("Implement reserve_stock")
