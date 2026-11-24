"""Create a typed adapter around a fake transport. Normalize provider-specific
requests and responses. For both providers map each Message to a role/content
dict. Claude carries policy in the top-level system key. Azure prepends a
system message. The simplified Claude response uses content (a text string)
and input_tokens/output_tokens. The simplified Azure response uses text and
prompt_tokens/completion_tokens. Counters must be nonnegative exact ints.
Missing or malformed response fields raise ValueError.
For transfer, route Claude first, falling back to Azure once only on 429 or
503. Propagate other errors immediately. These payloads are fixtures; live
SDKs wrap them in additional fields and have their own schemas."""

from unittest import TestCase

from koans import Exercise, __, todo
from koans.agents._providers import Message, Payload, Provider, ProviderError, Reply, Transport


def predict(t: TestCase, *answers: object) -> None:
    payload = {"system": "policy", "messages": [{"role": "user"}]}
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple(msg["role"] for msg in payload["messages"]))


def contrast(t: TestCase, *answers: object) -> None:
    history = [{"role": "system"}, {"role": "user"}]
    expected: object = __
    t.assertEqual(answers[0] if answers else expected, tuple(msg["role"] for msg in history))


class ProviderClient:
    def __init__(self, transport: Transport) -> None:
        self.transport = transport

    def call(self, provider: Provider, policy: str, messages: tuple[Message, ...]) -> Reply:
        history = [{"role": message.role, "content": message.text} for message in messages]
        payload: Payload
        if provider == "claude":
            payload = {"system": policy, "messages": history}
            fields = ("content", "input_tokens", "output_tokens")
        else:
            todo("package policy for Azure and name its response fields")

        result = self.transport.send(provider, payload)
        content, incoming, outgoing = (result.get(key) for key in fields)
        todo("validate normalized text and usage, then construct the reply")

    def answer(self, policy: str, messages: tuple[Message, ...]) -> Reply:
        try:
            return self.call("claude", policy, messages)
        except ProviderError as error:
            todo("propagate terminal errors and make one fallback for retryable statuses")


class _ClaudeSample:
    def send(self, provider: Provider, payload: Payload) -> dict[str, object]:
        return {"content": "example", "input_tokens": 2, "output_tokens": 3}


class _FallbackSample:
    def send(self, provider: Provider, payload: Payload) -> dict[str, object]:
        if provider == "claude":
            raise ProviderError(429)
        return {"text": "backup", "prompt_tokens": 1, "completion_tokens": 2}


def practice(t: TestCase, exercise: Exercise) -> None:
    client = exercise.ProviderClient(_ClaudeSample())
    t.assertEqual(client.call("claude", "policy", (Message("user", "hello"),)),
                  Reply("claude", "example", 5))


def practice_break(t: TestCase, exercise: Exercise) -> None:
    class Malformed:
        def send(self, provider: Provider, payload: Payload) -> dict[str, object]:
            return {"content": "text", "input_tokens": True, "output_tokens": 2}

    with t.assertRaises(ValueError):
        exercise.ProviderClient(Malformed()).call("claude", "policy", ())


def practice_transfer(t: TestCase, exercise: Exercise) -> None:
    client = exercise.ProviderClient(_FallbackSample())
    t.assertEqual(client.answer("policy", ()), Reply("azure", "backup", 3))
