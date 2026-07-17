import base64

from app.llm.openai.client import OpenAIClient


class OpenAIImageService:


    def __init__(self):

        self.client = OpenAIClient.get_client()


    async def generate(
        self,
        prompt: str,
        image_path: str
    ):


        with open(image_path, "rb") as image:

            response = self.client.images.edit(
                model="gpt-image-1.5",
                image=image,
                prompt=prompt
            )


        return base64.b64decode(
            response.data[0].b64_json
        )