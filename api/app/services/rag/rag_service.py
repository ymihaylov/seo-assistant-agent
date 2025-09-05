from .vector_store_service import VectorStoreService


class RAGService:
    def __init__(self, vector_store: VectorStoreService):
        self.vector_store = vector_store

    def get_relevant_context(self, query: str, session_title: str = None) -> str:
        search_query = query
        if session_title:
            search_query = f"{session_title} {query}"

        # Retrieve relevant documents
        relevant_docs = self.vector_store.search_similar(search_query, n_results=3)

        if not relevant_docs:
            return ""

        # Format context for the AI agent
        context_parts = []
        context_parts.append("## Relevant SEO Knowledge:")

        for i, doc in enumerate(relevant_docs, 1):
            category = doc["metadata"].get("category", "general")
            importance = doc["metadata"].get("importance", "medium")

            context_parts.append(
                f"\n{i}. **{category.replace('_', ' ').title()}** ({importance} importance):\n"
                f"   {doc['content']}"
            )

        context_parts.append("\n## Instructions:")
        context_parts.append(
            "Use the above SEO knowledge to inform your recommendations. "
            "Ensure your suggestions align with these best practices."
        )

        return "\n".join(context_parts)

    def enhance_prompt_with_context(self, original_prompt: str, context: str) -> str:
        if not context:
            return original_prompt

        enhanced_prompt = f"""{context}

## User Request:
{original_prompt}

Please provide SEO recommendations that incorporate the relevant knowledge above."""

        return enhanced_prompt
