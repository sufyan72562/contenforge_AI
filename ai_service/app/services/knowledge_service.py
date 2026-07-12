from __future__ import annotations

import asyncio

from app.repositories.knowledge.brand_memory_repository import (
    BrandMemoryRepository,
)
from app.repositories.knowledge.content_library_repository import (
    ContentLibraryRepository,
)
from app.repositories.knowledge.product_repository import (
    ProductKnowledgeRepository,
)
from app.schemas.knowledge_bundle import (
    KnowledgeBundle,
)


class KnowledgeService:

    def __init__(
        self,
        product_repository: ProductKnowledgeRepository | None = None,
        brand_repository: BrandMemoryRepository | None = None,
        content_repository: ContentLibraryRepository | None = None,
    ) -> None:

        self._product_repository = (
            product_repository
            or ProductKnowledgeRepository()
        )

        self._brand_repository = (
            brand_repository
            or BrandMemoryRepository()
        )

        self._content_repository = (
            content_repository
            or ContentLibraryRepository()
        )

    async def load(
        self,
    ) -> KnowledgeBundle:

        products_task = (
            self._product_repository.list_products()
        )

        brand_task = (
            self._brand_repository.get_brand_memory()
        )

        content_task = (
            self._content_repository.list_content()
        )

        (
            products,
            brand_memory,
            content_library,
        ) = await asyncio.gather(
            products_task,
            brand_task,
            content_task,
        )

        return KnowledgeBundle(
            products=products,
            brand_memory=brand_memory,
            content_library=content_library,
        )