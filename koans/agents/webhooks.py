"""Handle signed events delivered by a mock workflow. The signature is a lowercase
HMAC-SHA256 hex digest over ASCII decimal timestamp, a period, and the exact
body bytes. Compare digests with compare_digest. Return 401 for invalid signatures
or timestamps more than 60 seconds from now in either direction, before parsing
or calling the processor. Signature input may be malformed. The body must be UTF-8
JSON containing exactly a nonblank string id and positive exact integer amount.
Duplicate keys or invalid input return 422.

A successful call returns 200 with its integer result. Cache successful results
by event ID and amount. Return the prior receipt for the same ID and amount;
return 409 if an already completed ID arrives with a different amount. Treat
RuntimeError from the processor as a transient 503 and leave the event eligible
for replay. Other processor exceptions propagate. This ledger is sequential
and local to one instance. A processor raising RuntimeError has made no changes.

For transfer, process a batch in order, retrying a 503 exactly once before
moving to the next delivery. Return the final receipt for each delivery."""

from koans import __
from koans.agents._webhooks import Delivery, Event, Processor, Receipt

prediction = __
contrast = __



class DeliveryInbox:
    def __init__(self, secret: bytes, process: Processor) -> None:
        self.secret = secret
        self.process = process

    def receive(self, delivery: Delivery, now: int) -> Receipt:
        raise AssertionError("Implement receive")

    def redrive(self, deliveries: tuple[Delivery, ...], now: int) -> tuple[Receipt, ...]:
        raise AssertionError("Implement redrive")
