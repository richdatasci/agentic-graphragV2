class AzureOpenAIProvider:
    def __init__(self, api_key: str = "INSERT API KEY HERE", endpoint: str = "") -> None:
        self.api_key = api_key
        self.endpoint = endpoint
