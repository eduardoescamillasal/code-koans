from koans.agents._webhooks import Delivery, Receipt
from maintainer.references.agents_webhooks import DeliveryInbox


class NoReplay(DeliveryInbox):
    def receive(self, delivery: Delivery, now: int) -> Receipt:
        self._completed.clear()
        return super().receive(delivery, now)


class IgnoreTimestamp(DeliveryInbox):
    def receive(self, delivery: Delivery, now: int) -> Receipt:
        return super().receive(delivery, delivery.timestamp)


class NoRetry(DeliveryInbox):
    def redrive(self, deliveries: tuple[Delivery, ...], now: int) -> tuple[Receipt, ...]:
        return tuple(self.receive(delivery, now) for delivery in deliveries)


CASES = {
    "predict": {"prediction": (True, True)},
    "contrast": {"contrast": False},
    "implement": {"DeliveryInbox": NoReplay},
    "break_cases": {"DeliveryInbox": IgnoreTimestamp},
    "transfer": {"DeliveryInbox": NoRetry},
}
