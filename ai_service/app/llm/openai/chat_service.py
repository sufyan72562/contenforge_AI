import json

from app.llm.openai.client import OpenAIClient


class OpenAIChatService:


    def __init__(self):

        self.client = OpenAIClient.get_client()


    async def generate(
        self,
        prompt: str
    ):


        response = self.client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )


        return json.loads(
            response.output_text
        )