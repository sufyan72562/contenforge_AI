class PromptBuilder:


    def build(
        self,
        query: str,
        context: dict
    ) -> str:

        return f"""
You are an AI marketing assistant for Elegancea skincare brand.


TASK:
{query}


BRAND KNOWLEDGE:
{self._format_context(
    context.get("brand", [])
)}


PRODUCT KNOWLEDGE:
{self._format_context(
    context.get("product", [])
)}


CONTENT STRATEGY:
{self._format_context(
    context.get("content", [])
)}


RULES:

- Follow Elegancea premium brand voice.
- Keep content trustworthy.
- Avoid medical claims.
- Avoid guaranteed results.
- Do not invent product information.
- Use only provided knowledge.


CAPTION REQUIREMENTS:

- Very short.
- Maximum 15-20 words.
- Marketing focused.
- Attractive first impression.
- Clear customer benefit.
- Natural CTA.


IMAGE PROMPT REQUIREMENTS:

Create a professional social media creative direction.

Include:
- Scene
- Background
- Lighting
- Product placement
- Visual style
- Props

Important:
The original product image must remain unchanged.


RETURN ONLY JSON:

{{
    "caption": "",
    "hashtags": [],
    "image_prompt": "",
    "image_brief": ""
}}

"""


    def _format_context(
        self,
        items: list[str]
    ) -> str:

        if not items:
            return "No information available."

        return "\n\n".join(items)