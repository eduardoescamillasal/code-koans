from koans.agents._webhooks import Delivery, Event, Processor, Receipt


import hmac
import json

prediction = (True, False)
contrast = True


def unique_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
    fields: dict[str, object] = {}
    for key, value in pairs:
        if key in fields:
            raise ValueError("duplicate JSON field")
        fields[key] = value
    return fields


class DeliveryInbox:
    def __init__(self, secret: bytes, process: Processor) -> None:
        self.secret = secret
        self.process = process
        self._completed: dict[str, tuple[int, Receipt]] = {}

    def receive(self, delivery: Delivery, now: int) -> Receipt:
        if abs(now - delivery.timestamp) > 60 or not delivery.signature.isascii():
            return Receipt(401)
        authenticated = str(delivery.timestamp).encode("ascii") + b"." + delivery.body
        expected = hmac.digest(self.secret, authenticated, "sha256").hex()
        if not hmac.compare_digest(delivery.signature, expected):
            return Receipt(401)

        try:
            data = json.loads(delivery.body.decode("utf-8"), object_pairs_hook=unique_fields)
        except (ValueError, RecursionError):
            return Receipt(422)
        if not isinstance(data, dict) or data.keys() != {"id", "amount"}:
            return Receipt(422)
        event_id, amount = data["id"], data["amount"]
        if not isinstance(event_id, str) or not event_id.strip() or type(amount) is not int or amount < 1:
            return Receipt(422)

        previous = self._completed.get(event_id)
        if previous is not None:
            prior_amount, receipt = previous
            return receipt if prior_amount == amount else Receipt(409)
        try:
            receipt = Receipt(200, self.process(Event(event_id, amount)))
        except RuntimeError:
            return Receipt(503)
        self._completed[event_id] = (amount, receipt)
        return receipt

    def redrive(self, deliveries: tuple[Delivery, ...], now: int) -> tuple[Receipt, ...]:
        results: list[Receipt] = []
        for delivery in deliveries:
            result = self.receive(delivery, now)
            if result.status == 503:
                result = self.receive(delivery, now)
            results.append(result)
        return tuple(results)
