from collections.abc import Mapping
from types import SimpleNamespace
from unittest import TestCase

from koans.agents._providers import Message, Payload, Provider, ProviderError, Reply


class FakeTransport:
    def __init__(self, replies: list[Mapping[str, object] | ProviderError]) -> None:
        self.replies = iter(replies)
        self.calls: list[tuple[Provider, Payload]] = []

    def send(self, provider: Provider, payload: Payload) -> Mapping[str, object]:
        self.calls.append((provider, payload))
        reply = next(self.replies)
        if isinstance(reply, ProviderError):
            raise reply
        return reply


def implement(t: TestCase, s: SimpleNamespace) -> None:
    transport = FakeTransport([
        {"content": "A", "input_tokens": 4, "output_tokens": 2},
        {"text": "B", "prompt_tokens": 3, "completion_tokens": 4},
    ])
    client = s.ProviderClient(transport)
    request = (Message("user", "question"),)
    t.assertEqual(client.call("claude", "policy", request), Reply("claude", "A", 6))
    t.assertEqual(client.call("azure", "policy", request), Reply("azure", "B", 7))
    user = {"role": "user", "content": "question"}
    t.assertEqual(transport.calls, [
        ("claude", {"system": "policy", "messages": [user]}),
        ("azure", {"messages": [{"role": "system", "content": "policy"}, user]}),
    ])


def break_cases(t: TestCase, s: SimpleNamespace) -> None:
    transport = FakeTransport([
        {"content": "A", "input_tokens": True, "output_tokens": 2},
        {"content": "A", "input_tokens": -1, "output_tokens": 2},
        {"content": ["A"], "input_tokens": 3, "output_tokens": 2},
        {"content": "A", "input_tokens": 3},
    ])
    client = s.ProviderClient(transport)
    for _ in range(4):
        with t.assertRaises(ValueError):
            client.call("claude", "policy", ())


def transfer(t: TestCase, s: SimpleNamespace) -> None:
    primary = FakeTransport([{"content": "A", "input_tokens": 4, "output_tokens": 2}])
    t.assertEqual(s.ProviderClient(primary).answer("policy", ()), Reply("claude", "A", 6))
    t.assertEqual([provider for provider, _ in primary.calls], ["claude"])

    for status in (429, 503):
        transport = FakeTransport([ProviderError(status), {"text": "B", "prompt_tokens": 2, "completion_tokens": 1}])
        t.assertEqual(s.ProviderClient(transport).answer("policy", ()), Reply("azure", "B", 3))
        t.assertEqual([provider for provider, _ in transport.calls], ["claude", "azure"])
    transport = FakeTransport([ProviderError(401)])
    with t.assertRaises(ProviderError) as error:
        s.ProviderClient(transport).answer("policy", ())
    t.assertEqual(error.exception.status, 401)
    t.assertEqual(len(transport.calls), 1)
    transport = FakeTransport([ProviderError(503), ProviderError(503)])
    with t.assertRaises(ProviderError):
        s.ProviderClient(transport).answer("policy", ())
    t.assertEqual(len(transport.calls), 2)
