class ProviderError(RuntimeError):
    pass


class Provider:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn

    def ask(self, prompt: str) -> str:
        return self.fn(prompt)


class FallbackChain:
    """Try providers in sequence until one succeeds."""

    def __init__(self, providers):
        self.providers = providers

    def run(self, prompt: str) -> dict:
        last_error = None
        for provider in self.providers:
            try:
                result = provider.ask(prompt)
                return {"provider": provider.name, "result": result}
            except Exception as exc:  # pragma: no cover
                last_error = str(exc)
        raise ProviderError(f"All providers failed. last_error={last_error}")
