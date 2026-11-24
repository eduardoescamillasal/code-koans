from dataclasses import replace
import hmac
import json
from types import SimpleNamespace
from unittest import TestCase

from koans.agents._webhooks import Delivery, Event, Receipt

SECRET = b"fixture only"


def sign(body: bytes, timestamp: int = 100) -> Delivery:
    signed = str(timestamp).encode("ascii") + b"." + body
    return Delivery(timestamp, body, hmac.digest(SECRET, signed, "sha256").hex())


def predict(t: TestCase, s: SimpleNamespace) -> None:
    left, right = b'{"amount":2}', b'{"amount": 2}'
    t.assertEqual(s.prediction, (json.loads(left) == json.loads(right),
                              sign(left).signature == sign(right).signature))


def contrast(t: TestCase, s: SimpleNamespace) -> None:
    left, right = b'{"amount":2}', b'{"amount": 2}'
    reencoded = tuple(json.dumps(json.loads(body), separators=(",", ":")).encode("utf-8")
                      for body in (left, right))
    t.assertEqual(s.contrast, sign(reencoded[0]).signature == sign(reencoded[1]).signature)


def implement(t: TestCase, s: SimpleNamespace) -> None:
    calls: list[Event] = []

    def process(event: Event) -> int:
        calls.append(event)
        return event.amount * 3

    inbox = s.DeliveryInbox(SECRET, process)
    event = sign(b'{"id":"alpha","amount":3}')
    t.assertEqual(inbox.receive(event, 100), Receipt(200, 9))
    t.assertEqual(inbox.receive(sign(b'{ "amount": 3, "id": "alpha" }', 101), 101), Receipt(200, 9))
    t.assertEqual(inbox.receive(sign(b'{"id":"alpha","amount":4}'), 101), Receipt(409))
    t.assertEqual(calls, [Event("alpha", 3)])


def break_cases(t: TestCase, s: SimpleNamespace) -> None:
    calls: list[Event] = []

    def process(event: Event) -> int:
        calls.append(event)
        return 0

    inbox = s.DeliveryInbox(SECRET, process)
    event = sign(b'{"id":"x","amount":2}')
    for bad, now in ((event, 39), (event, 161), (replace(event, signature="é"), 100),
                     (replace(event, body=b'{"id":"x","amount": 2}'), 100),
                     (replace(event, timestamp=101), 100)):
        t.assertEqual(inbox.receive(bad, now), Receipt(401))
    for invalid in (b'{"id":"x","amount":true}', b'{"id":"x","amount":1,"amount":2}',
                    b'[]', b'\xff', b'{"id":" ","amount":1}'):
        t.assertEqual(inbox.receive(sign(invalid), 100), Receipt(422))
    t.assertEqual(calls, [])
    t.assertEqual(inbox.receive(event, 160), Receipt(200, 0))
    t.assertEqual(calls, [Event("x", 2)])


def transfer(t: TestCase, s: SimpleNamespace) -> None:
    attempts: list[str] = []

    def process(event: Event) -> int:
        attempts.append(event.id)
        if event.id == "bad" or (event.id == "retry" and attempts.count("retry") == 1):
            raise RuntimeError("workflow busy")
        return event.amount

    inbox = s.DeliveryInbox(SECRET, process)
    retry = sign(b'{"id":"retry","amount":1}')
    bad = sign(b'{"id":"bad","amount":2}')
    skipped = replace(retry, signature="invalid")
    t.assertEqual(inbox.redrive((retry, bad, retry, skipped), 100),
                  (Receipt(200, 1), Receipt(503), Receipt(200, 1), Receipt(401)))
    t.assertEqual(attempts, ["retry", "retry", "bad", "bad"])
