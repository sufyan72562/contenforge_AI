from pydantic import BaseModel


class GeneratedContent(BaseModel):

    caption: str

    hashtags: list[str]

    image_prompt: str

    image_brief: str