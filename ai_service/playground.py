# # from app.rag.retriever import KnowledgeRetriever
# # from app.prompts.prompt_builder import PromptBuilder


# # retriever = KnowledgeRetriever()

# # documents = retriever.retrieve(
# #     "Create an educational Instagram post for sunscreen",
# #     k=3
# # )


# # builder = PromptBuilder()


# # prompt = builder.build(
# #     query="Create an educational Instagram post for sunscreen",
# #     documents=documents
# # )


# # print(prompt)

# import base64
# import os

# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )




# prompt = """
# Create a premium square (1080x1080) social media marketing post for a skincare brand.

# IMPORTANT PRODUCT RULES:
# - Use the uploaded Splush Face Wash image exactly as provided.
# - DO NOT redesign, modify, redraw, or recreate the product.
# - DO NOT change the product packaging, logo, colors, label, typography, cap, proportions, reflections, or any printed text.
# - Preserve every detail of the original product image.
# - Use the product as the hero element in the final design.

# POST STYLE:
# Modern luxury skincare advertisement.
# Premium Instagram marketing post.
# Clean, elegant, high-end cosmetic branding.
# Pink and white color palette matching the product.
# Professional typography.
# Soft gradients, glossy lighting, water splash elements, subtle bubbles, fresh skincare aesthetic.

# LAYOUT:
# Left side (70% visual storytelling):
# Show a young South Asian woman looking concerned while touching her face.
# Around her face display realistic circular close-up skin textures representing common skin concerns.

# Problem 1:
# Dull & Tired Skin
# Small description:
# "Skin bejaan aur rough feel hoti hai"

# Problem 2:
# Excess Oil & Clogged Pores
# Small description:
# "Chehra jaldi oily ho jata hai"

# Problem 3:
# Dead Skin Build-up
# Small description:
# "Skin fresh aur smooth nahi lagti"

# Problem 4:
# Makeup Doesn't Sit Well
# Small description:
# "Uneven texture ki wajah se makeup patchy lagta hai"

# Use arrows or connecting lines from the face to each skin concern.

# RIGHT SIDE:
# Place the original Splush Face Wash product prominently with premium lighting and realistic shadows.

# Next to the product add feature icons.

# ✔ Deep Cleansing
# ✔ Removes Dirt & Excess Oil
# ✔ Gentle Daily Cleanser
# ✔ Fresh Skin Feel

# BOTTOM SECTION:
# Modern premium footer with brand identity.

# Headline:
# "Healthy Skin Starts with Proper Cleansing"

# Small CTA:
# "Take care of your skin every day."

# Brand logo area.
# Website placeholder.

# DESIGN REQUIREMENTS:
# Highly realistic.
# Luxury cosmetic advertisement.
# Professional social media campaign.
# Magazine-quality composition.
# Minimal but informative.
# Excellent typography hierarchy.
# Balanced spacing.
# High readability.
# Premium skincare branding.
# Ultra high detail.
# Photorealistic.

# NEGATIVE PROMPT:
# No product redesign.
# No AI-generated replacement packaging.
# No different logo.
# No altered label.
# No spelling mistakes.
# No extra bottles.
# No duplicate products.
# No cropped product.
# No distorted hands.
# No deformed faces.
# No low quality.
# No watermark.
# No random decorative objects.
# No unrealistic skin.
# No excessive text.
# """

# result = client.images.edit(
#     model="gpt-image-2",
#     image=[
#         open(os.path.join(os.path.dirname(__file__), "app/images/facewash.png"), "rb")
#     ],
#     prompt=prompt,
#     size="1024x1024"
# )


# image_base64 = result.data[0].b64_json

# image_bytes = base64.b64decode(image_base64)

# with open("facewash_generated.png", "wb") as f:
#     f.write(image_bytes)

# print("Done")

# # print("result: ", result)
# # image_base64 = result.output[0].content[0].image_base64

# with open("facewash_generated.png", "wb") as f:
#     f.write(base64.b64decode(image_base64))

# print("Image saved as facewash_generated.png")
import asyncio

from app.services.ai_generation_service import AIGenerationService

from app.rag.rag_service import RAGService
from app.prompts.prompt_builder import PromptBuilder
from app.llm.openai.chat_service import OpenAIChatService
from app.llm.openai.image_service import OpenAIImageService



async def main():

    ai_service = AIGenerationService(
        rag_service=RAGService(),
        prompt_builder=PromptBuilder(),
        chat_service=OpenAIChatService(),
        image_service=OpenAIImageService(),
    )


    result = await ai_service.generate(
        query="Create Instagram post for Glint C Serum",
        product_image="app/images/glint_c_serum.png"
    )


    print(result["caption"])
    print(result["hashtags"])


    with open(
        "generated_post.png",
        "wb"
    ) as f:
        f.write(
            result["image"]
        )



asyncio.run(main())