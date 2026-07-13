from app.services.knowledge_service import KnowledgeService
from app.rag.document_builder import KnowledgeDocumentBuilder
from app.vectorstore.pgvector_store import PGVectorStore


class KnowledgeIngestionService:

    def __init__(self):

        self.knowledge_service = KnowledgeService()
        self.document_builder = KnowledgeDocumentBuilder()
        self.vector_store = PGVectorStore()


    async def ingest(self):

        knowledge = await self.knowledge_service.load()

        documents = self.document_builder.build(
            knowledge
        )

        self.vector_store.add_documents(
            documents
        )

        return {
            "documents_added": len(documents)
        }