from app.rag.retriever import KnowledgeRetriever
from app.prompts.prompt_builder import PromptBuilder


retriever = KnowledgeRetriever()

documents = retriever.retrieve(
    "Create an educational Instagram post for sunscreen",
    k=3
)


builder = PromptBuilder()


prompt = builder.build(
    query="Create an educational Instagram post for sunscreen",
    documents=documents
)


print(prompt)