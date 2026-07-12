from __future__ import annotations

from pydantic import BaseModel

from app.schemas.brand_memory import BrandMemory
from app.schemas.content_library import ContentLibraryItem
from app.schemas.product_knowledge import ProductKnowledge


class KnowledgeBundle(BaseModel):
    products: list[ProductKnowledge]
    brand_memory: BrandMemory
    content_library: list[ContentLibraryItem]