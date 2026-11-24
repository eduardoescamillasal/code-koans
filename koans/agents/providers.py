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

from koans import __
from koans.agents._providers import Message, Payload, Provider, ProviderError, Reply, Transport

prediction = __
contrast = __



class ProviderClient:
    def __init__(self, transport: Transport) -> None:
        self.transport = transport

    def call(self, provider: Provider, policy: str, messages: tuple[Message, ...]) -> Reply:
        raise AssertionError("Implement call")

    def answer(self, policy: str, messages: tuple[Message, ...]) -> Reply:
        raise AssertionError("Implement answer")
