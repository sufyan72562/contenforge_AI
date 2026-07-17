from app.rag.retriever import KnowledgeRetriever
from app.rag.context_builder import ContextBuilder


class RAGService:

    def __init__(self):

        self.retriever = KnowledgeRetriever()
        self.context_builder = ContextBuilder()


    async def get_context(
        self,
        query: str,
        k: int = 5,
    ):

        documents = await self.retriever.retrieve(
            query=query,
            k=k,
        )


        return self.context_builder.build(
            documents
        )