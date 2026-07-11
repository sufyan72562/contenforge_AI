from fastapi import FastAPI, HTTPException

from app.repositories.exceptions import (
    ProductKnowledgeRepositoryError,
)
from app.repositories.knowledge.product_repository import (
    ProductKnowledgeRepository,
)


app = FastAPI(title="ContentForge AI Service")


@app.get("/test/products")
async def list_products() -> dict:
    repository = ProductKnowledgeRepository()

    try:
        products = await repository.list_products()

        return {
            "count": len(products),
            "products": products,
        }

    except ProductKnowledgeRepositoryError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@app.get("/test/products/{product_id}")
async def get_product(product_id: str) -> dict:
    repository = ProductKnowledgeRepository()

    try:
        product = await repository.get_product_by_id(product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found.",
            )

        return product

    except ProductKnowledgeRepositoryError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc