from openai import OpenAI

from app.core.config import get_settings


class OpenAIClient:

    _client = None

    @classmethod
    def get_client(cls) -> OpenAI:

        if cls._client is None:
            cls._client = OpenAI(
                api_key=get_settings().OPENAI_API_KEY,
            )

        return cls._client