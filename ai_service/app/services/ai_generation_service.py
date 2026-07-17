class AIGenerationService:


    def __init__(
        self,
        rag_service,
        prompt_builder,
        chat_service,
        image_service,
    ):

        self.rag = rag_service
        self.prompt_builder = prompt_builder
        self.chat = chat_service
        self.image = image_service



    async def generate(
        self,
        query: str,
        product_image: str | None = None,
    ):


        # 1. Retrieve knowledge
        context = await self.rag.get_context(
            query
        )


        # 2. Build prompt
        prompt = self.prompt_builder.build(
            query=query,
            context=context
        )


        # 3. Generate caption + image prompt
        content = await self.chat.generate(
            prompt
        )


        result = {
            "caption": content["caption"],
            "hashtags": content["hashtags"],
            "image": None
        }


        # 4. Generate image if required
        if product_image:

            image = await self.image.generate(
                prompt=content["image_prompt"],
                image_path=product_image
            )


            result["image"] = image


        return result