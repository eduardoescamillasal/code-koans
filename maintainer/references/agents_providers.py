from koans.agents._providers import Message, Payload, Provider, ProviderError, Reply, Transport


prediction = ("user",)
contrast = ("system", "user")


class ProviderClient:
    def __init__(self, transport: Transport) -> None:
        self.transport = transport

    def call(self, provider: Provider, policy: str, messages: tuple[Message, ...]) -> Reply:
        history = [{"role": message.role, "content": message.text} for message in messages]
        payload: Payload
        if provider == "claude":
            payload = {"system": policy, "messages": history}
            fields = "content", "input_tokens", "output_tokens"
        else:
            payload = {"messages": [{"role": "system", "content": policy}, *history]}
            fields = "text", "prompt_tokens", "completion_tokens"
        result = self.transport.send(provider, payload)
        content, incoming, outgoing = (result.get(key) for key in fields)
        if not isinstance(content, str) or type(incoming) is not int or type(outgoing) is not int:
            raise ValueError("malformed provider reply")
        if incoming < 0 or outgoing < 0:
            raise ValueError("negative token count")
        return Reply(provider, content, incoming + outgoing)

    def answer(self, policy: str, messages: tuple[Message, ...]) -> Reply:
        try:
            return self.call("claude", policy, messages)
        except ProviderError as error:
            if error.status not in (429, 503):
                raise
        return self.call("azure", policy, messages)
