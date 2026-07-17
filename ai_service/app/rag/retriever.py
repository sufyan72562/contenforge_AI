from app.vectorstore.pgvector_store import PGVectorStore


class KnowledgeRetriever:

    def __init__(self):

        self.vector_store = PGVectorStore()


    async def retrieve(
        self,
        query: str,
        k: int = 5
    ):

        return self.vector_store.search(
            query=query,
            k=k
        )