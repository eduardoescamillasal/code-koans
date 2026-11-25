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


from koans import Koan, __, todo
from koans.agents._providers import Message, Payload, Provider, ProviderError, Reply, Transport


class AboutProviderAdapters(Koan):
    def test_claude_policy_lives_outside_message_history(self) -> None:
        payload = {"system": "policy", "messages": [{"role": "user"}]}
        self.assertEqual(__, tuple(msg["role"] for msg in payload["messages"]))

    def test_azure_history_can_start_with_policy(self) -> None:
        history = [{"role": "system"}, {"role": "user"}]
        self.assertEqual(__, tuple(msg["role"] for msg in history))

    def test_input_and_output_counters_measure_different_parts_of_usage(self) -> None:
        claude = {"input_tokens": 8, "output_tokens": 3}
        azure = {"prompt_tokens": 2, "completion_tokens": 9}
        self.assertEqual(__, claude["input_tokens"] == azure["prompt_tokens"])
        self.assertEqual(__, sum(claude.values()) == sum(azure.values()))

    def test_a_boolean_can_look_like_a_token_count(self) -> None:
        raw = {"input_tokens": True, "output_tokens": 6}
        self.assertEqual(__, sum(raw.values()))
        self.assertEqual(__, type(raw["input_tokens"]) is int)

    def test_the_exception_retains_status_for_the_routing_decision(self) -> None:
        statuses = (401, 429, 503)
        retries = []
        for status in statuses:
            try:
                raise ProviderError(status)
            except ProviderError as error:
                if error.status in {429, 503}:
                    retries.append(error.status)
        self.assertEqual(__, retries)
        self.assertEqual(__, len(statuses) - len(retries))


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
