from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.core.config import get_settings


class EmbeddingService:

    def __init__(self):

        self.embeddings = HuggingFaceEndpointEmbeddings(
            huggingfacehub_api_token=get_settings().HUGGINGFACEHUB_API_TOKEN,
            repo_id="BAAI/bge-m3"
        )


    def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        return self.embeddings.embed_documents(
            texts
        )


    def embed_query(
        self,
        text: str
    ) -> list[float]:

        return self.embeddings.embed_query(
            text
        )