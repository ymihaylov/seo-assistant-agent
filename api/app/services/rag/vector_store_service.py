from typing import List, Dict, Any

import chromadb
import openai


class VectorStoreService:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = "seo_knowledge"

        try:
            self.openai_client = openai.OpenAI()
            self.use_openai_embeddings = True
        except Exception as e:
            self.use_openai_embeddings = False
            # Use ChromaDB's default embedding function as fallback
            from chromadb.utils import embedding_functions

            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        try:
            return self.client.get_collection(name=self.collection_name)
        except Exception:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "SEO knowledge base for RAG"},
            )

    def add_documents(self, documents: List[Dict[str, str]]) -> None:
        """Add documents to the vector store.

        Args:
            documents: List of dicts with 'content', 'metadata' keys
        """
        texts = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        ids = [f"doc_{i}" for i in range(len(documents))]

        # Generate embeddings
        if self.use_openai_embeddings:
            embeddings = []
            for text in texts:
                response = self.openai_client.embeddings.create(
                    input=text, model="text-embedding-3-small"
                )
                embeddings.append(response.data[0].embedding)
        else:
            # Use ChromaDB's default embedding function
            embeddings = self.embedding_function(texts)

        self.collection.add(
            embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids
        )

    def search_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search for similar documents based on query.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        if self.use_openai_embeddings:
            response = self.openai_client.embeddings.create(
                input=query, model="text-embedding-3-small"
            )
            query_embedding = [response.data[0].embedding]
        else:
            # Use ChromaDB's default embedding function
            query_embedding = self.embedding_function([query])

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        # Format results
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append(
                    {
                        "content": doc,
                        "metadata": (
                            results["metadatas"][0][i] if results["metadatas"] else {}
                        ),
                        "distance": (
                            results["distances"][0][i] if results["distances"] else 0.0
                        ),
                    }
                )

        return formatted_results

    def initialize_seo_knowledge(self) -> None:
        seo_documents = [
            {
                "content": "Title tags should be 50-60 characters long and include primary keywords near the beginning. They appear in search results and browser tabs.",
                "metadata": {"category": "title_tags", "importance": "high"},
            },
            {
                "content": "Meta descriptions should be 150-160 characters, compelling, and include target keywords. They influence click-through rates from search results.",
                "metadata": {"category": "meta_description", "importance": "high"},
            },
            {
                "content": "Page content should be comprehensive, original, and provide value to users. Aim for 300+ words with natural keyword integration.",
                "metadata": {"category": "content", "importance": "high"},
            },
            {
                "content": "Header tags (H1, H2, H3) create content hierarchy. Use one H1 per page with primary keyword, and H2-H6 for subheadings.",
                "metadata": {"category": "headers", "importance": "medium"},
            },
            {
                "content": "Internal linking helps search engines understand site structure and distributes page authority. Use descriptive anchor text.",
                "metadata": {"category": "internal_linking", "importance": "medium"},
            },
            {
                "content": "Page loading speed affects SEO rankings. Optimize images, minimize CSS/JS, and use CDNs for better performance.",
                "metadata": {"category": "performance", "importance": "high"},
            },
            {
                "content": "Mobile-first design is crucial as Google uses mobile-first indexing. Ensure responsive design and fast mobile loading.",
                "metadata": {"category": "mobile", "importance": "high"},
            },
            {
                "content": "Schema markup helps search engines understand content context. Use structured data for rich snippets and better visibility.",
                "metadata": {"category": "schema", "importance": "medium"},
            },
        ]

        count = self.collection.count()
        if count == 0:
            self.add_documents(seo_documents)
            print(
                f"Initialized vector store with {len(seo_documents)} SEO knowledge documents"
            )
        else:
            print(f"Vector store already contains {count} documents")
