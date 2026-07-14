class ContextBuilder:

    def build(self, documents):

        context = {
            "products": [],
            "content": [],
            "brand": []
        }

        for doc in documents:

            doc_type = doc.metadata.get("type")

            if doc_type == "product":
                context["products"].append(
                    doc.page_content
                )

            elif doc_type == "content":
                context["content"].append(
                    doc.page_content
                )

            elif doc_type == "brand":
                context["brand"].append(
                    doc.page_content
                )

        return context