from __future__ import annotations

from langchain_core.documents import Document

from app.schemas.knowledge_bundle import KnowledgeBundle


class KnowledgeDocumentBuilder:

    def build(
        self,
        knowledge: KnowledgeBundle,
    ) -> list[Document]:

        documents: list[Document] = []

        documents.extend(
            self._build_product_documents(
                knowledge
            )
        )

        documents.append(
            self._build_brand_document(
                knowledge
            )
        )

        documents.extend(
            self._build_content_documents(
                knowledge
            )
        )

        return documents


    def _build_product_documents(
        self,
        knowledge: KnowledgeBundle,
    ) -> list[Document]:

        documents = []

        for product in knowledge.products:

            content = f"""
Product Name:
{product.product_name}

Category:
{product.category}

Purpose:
{product.main_purpose}

Description:
{product.short_description}

Benefits:
{product.key_benefits}

Hero Ingredients:
{product.hero_ingredients}

Full Ingredients:
{product.full_ingredients}

Usage:
{product.usage}

Skin Type:
{product.skin_type}

Texture:
{product.texture}

Finish:
{product.finish}
"""

            documents.append(
                Document(
                    page_content=content.strip(),

                    metadata={
                        "type": "product",
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "category": product.category,
                    },
                )
            )

        return documents


    def _build_brand_document(
        self,
        knowledge: KnowledgeBundle,
    ) -> Document:

        brand = knowledge.brand_memory

        content = f"""
Brand Name:
{brand.brand_name}

Audience:
{brand.target_audience}

Personality:
{brand.brand_personality}

Voice:
{brand.brand_voice}

Preferred Words:
{brand.preferred_words}

Avoid Words:
{brand.avoid_words}

Avoid Claims:
{brand.avoid_claims}

CTA:
{brand.cta_default}
"""

        return Document(
            page_content=content.strip(),

            metadata={
                "type": "brand_memory",
                "brand_name": brand.brand_name,
            },
        )


    def _build_content_documents(
        self,
        knowledge: KnowledgeBundle,
    ) -> list[Document]:

        documents = []

        for item in knowledge.content_library:

            content = f"""
Content Type:
{item.content_type}

Marketing Angle:
{item.marketing_angle}

Psychology:
{item.psychology}

Objective:
{item.objective}

Hook Instruction:
{item.hook_instruction}

Content Structure:
{item.content_structure}

CTA Style:
{item.cta_style}
"""

            documents.append(
                Document(
                    page_content=content.strip(),

                    metadata={
                        "type": "content_idea",
                        "content_id": item.content_id,
                    },
                )
            )

        return documents