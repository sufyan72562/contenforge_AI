from langchain_core.documents import Document


class PromptBuilder:


    def build(
        self,
        query: str,
        documents: list[Document]
    ) -> str:


        context = self._prepare_context(
            documents
        )


        prompt = f"""
You are an AI marketing assistant for Elegancea skincare brand.

Your task:
{query}


Brand Knowledge:
{context}


Instructions:
- Follow brand tone
- Avoid medical claims
- Keep content trustworthy
- Do not make false promises

Generate the response.
"""


        return prompt


    def _prepare_context(
        self,
        documents: list[Document]
    ) -> str:

        return "\n\n".join(
            [
                doc.page_content
                for doc in documents
            ]
        )