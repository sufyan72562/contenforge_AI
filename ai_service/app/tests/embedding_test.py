from app.embeddings.embedding_service import EmbeddingService


service = EmbeddingService()


vector = service.embed_query(
    "meri skin dry hai mujhe hydration chahiye"
)


print("Vector length:", len(vector))
print("First values:", vector[:5])