from pydantic import BaseModel, ConfigDict


class BrandMemory(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    brand_name: str
    website: str

    target_audience: str
    brand_personality: str
    brand_voice: str

    primary_color: str
    secondary_color: str
    accent_color: str

    logo_url: str = ""

    target_market: str
    language: str

    emoji_usage: str

    cta_default: str

    facebook: str = ""
    instagram: str = ""
    tiktok: str = ""

    avoid_claims: str
    preferred_words: str
    avoid_words: str

    image_style: str

    post_length: str

    hashtags_default: str