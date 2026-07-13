from langchain_postgres import PGVector

from app.embeddings.embedding_service import EmbeddingService
from app.core.config import get_settings


class PGVectorStore:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vector_store = PGVector(
            embeddings=self.embedding_service.embeddings,
            collection_name="elegancea_knowledge",
            connection=get_settings().DATABASE_URL,
            use_jsonb=True,
        )


    def add_documents(self, documents):

        self.vector_store.add_documents(
            documents
        )


    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):

        return self.vector_store.similarity_search(
            query,
            k=k
        )