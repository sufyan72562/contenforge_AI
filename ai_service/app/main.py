from fastapi import FastAPI, HTTPException

from app.vectorstore.pgvector_store import PGVectorStore
from app.repositories.knowledge.brand_memory_repository import BrandMemoryRepository
from app.repositories.exceptions import (
    ProductKnowledgeRepositoryError,
)
from app.repositories.knowledge.content_library_repository import ContentLibraryRepository
from app.repositories.knowledge.product_repository import (
    ProductKnowledgeRepository,
)
from app.services.knowledge_service import KnowledgeService
from app.rag.document_builder import KnowledgeDocumentBuilder
from app.embeddings.embedding_service import EmbeddingService
from app.rag.ingestion_service import KnowledgeIngestionService

app = FastAPI(title="ContentForge AI Service")


@app.get("/test/products")
async def list_products() -> dict:
    repo = BrandMemoryRepository()

    memory = await repo.get_brand_memory()

    print(memory.brand_name)

    print(memory.cta_default)

    print(memory.preferred_words)

    return {
        "brand_name": memory.brand_name,
        "cta_default": memory.cta_default,
        "preferred_words": memory.preferred_words,
    }

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
        

content_repo = ContentLibraryRepository()


@app.get("/test/content-library")
async def test_content_library():

    data = await content_repo.list_content()

    return {
        "count": len(data),
        "items": [
            item.model_dump()
            for item in data
        ],
    }

knowledge_service = KnowledgeService()


@app.get("/test/embeddings")
async def test_embeddings():

    service = EmbeddingService()


    vector = service.embed_query(
        "meri skin dry hai mujhe hydration chahiye"
    )
    
    return {
        "vector_length": len(vector),
        "first_values": vector[:5],
    }

    print("Vector length:", len(vector))
    print("First values:", vector[:5])

    # knowledge = await knowledge_service.load()

    # return knowledge.model_dump()




knowledge_service = KnowledgeService()
builder = KnowledgeDocumentBuilder()


@app.get("/test/documents")
async def test_documents():

    knowledge = await knowledge_service.load()

    documents = builder.build(
        knowledge
    )

    return {
        "count": len(documents),
        "documents": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in documents
        ],
    }



@app.post("/knowledge/ingest")
async def ingest():
    vector_store = PGVectorStore()
    results = vector_store.similarity_search(
    query="I need only serum",
    k=3
)
    return {
        "results": [
            {
                "content": result.page_content,
                "metadata": result.metadata,
            }
            for result in results
        ],
    }

    # service = KnowledgeIngestionService()

    # return await service.ingest()