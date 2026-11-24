from koans.agents._providers import Message, Provider, Reply
from maintainer.references.agents_providers import ProviderClient


class NoUsage(ProviderClient):
    def call(self, provider: Provider, policy: str, messages: tuple[Message, ...]) -> Reply:
        reply = super().call(provider, policy, messages)
        return Reply(provider, reply.text, 0)


class LooseReply(ProviderClient):
    def call(self, provider: Provider, policy: str, messages: tuple[Message, ...]) -> Reply:
        return Reply(provider, "A", 0)


class NoFallback(ProviderClient):
    def answer(self, policy: str, messages: tuple[Message, ...]) -> Reply:
        try:
            return self.call("claude", policy, messages)
        except Exception:
            return Reply("claude", "", 0)


CASES = {
    "predict": {"prediction": ("system", "user")},
    "contrast": {"contrast": ("user",)},
    "implement": {"ProviderClient": NoUsage},
    "break_cases": {"ProviderClient": LooseReply},
    "transfer": {"ProviderClient": NoFallback},
}
