#!/usr/bin/env python3
"""
Test script to verify RAG integration with the SEO agent.
This script tests the complete pipeline from query to RAG-enhanced response.
"""

import asyncio
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from app.services.rag.vector_store_service import VectorStoreService
from app.services.rag.rag_service import RAGService
from app.services.agent.agent_graph import seo_graph


async def test_rag_integration():
    """Test the complete RAG integration with SEO agent."""
    print("Testing RAG Integration with SEO Agent")
    print("=" * 50)

    # Test 1: Vector Store Functionality
    print("\nTesting Vector Store...")
    vector_store = VectorStoreService()

    # Test search functionality
    search_results = vector_store.search_similar(
        "title tag best practices", n_results=2
    )
    print(f"Found {len(search_results)} relevant documents")
    for i, result in enumerate(search_results, 1):
        print(f" {i}. {result['content'][:80]}...")

    # Test 2: RAG Service
    print("\n2️Testing RAG Service...")
    rag_service = RAGService(vector_store)

    context = rag_service.get_relevant_context(
        "How to optimize title tags for SEO", "E-commerce Product Page"
    )
    print(f"Generated context: {len(context)} characters")
    print(f"Context preview: {context[:200]}...")

    # Test 3: Complete SEO Agent with RAG
    print("\nTesting RAG-Enhanced SEO Agent...")

    # Test case 1: New session with title tag optimization
    test_state_1 = {
        "session_title": "E-commerce Product Page SEO",
        "instructions": "Help me optimize the title tag for my product page selling wireless headphones",
        "constraints": {
            "title_max": 60,
            "meta_description_min": 150,
            "meta_description_max": 160,
        },
    }

    print("   🔄 Processing: Title tag optimization query...")
    try:
        result_1 = await seo_graph.ainvoke(test_state_1)
        suggestions_1 = result_1.get("suggestions", {})

        print("   ✅ SEO Agent Response:")
        print(f"      📋 Page Title: {suggestions_1.get('page_title', 'N/A')}")
        print(f"      🏷️  Title Tag: {suggestions_1.get('title_tag', 'N/A')}")
        print(
            f"      📝 Meta Description: {suggestions_1.get('meta_description', 'N/A')[:50]}..."
        )
        print(f"      🔍 Keywords: {', '.join(suggestions_1.get('meta_keywords', []))}")

    except Exception as e:
        print(f"   ❌ Error in SEO Agent: {e}")

    # Test case 2: Content optimization query
    test_state_2 = {
        "session_title": "Blog Post SEO",
        "instructions": "I need help creating SEO-optimized content structure for a blog post about sustainable fashion",
        "constraints": {
            "title_max": 60,
            "meta_description_min": 150,
            "meta_description_max": 160,
        },
    }

    print("\n   🔄 Processing: Content structure optimization query...")
    try:
        result_2 = await seo_graph.ainvoke(test_state_2)
        suggestions_2 = result_2.get("suggestions", {})

        print("   ✅ SEO Agent Response:")
        print(f"      📋 Page Title: {suggestions_2.get('page_title', 'N/A')}")
        print(
            f"      📄 Content Preview: {suggestions_2.get('page_content', 'N/A')[:100]}..."
        )
        print(f"      🔍 Keywords: {', '.join(suggestions_2.get('meta_keywords', []))}")

    except Exception as e:
        print(f"   ❌ Error in SEO Agent: {e}")

    # Test 4: RAG Context Verification
    print("\n4️⃣ Verifying RAG Context Usage...")

    # Check if RAG context was actually used in the agent
    if "rag_context" in test_state_1:
        print("   ✅ RAG context was successfully integrated into agent state")
    else:
        print("   ⚠️  RAG context may not have been properly integrated")

    print("\n🎉 RAG Integration Test Complete!")
    print("=" * 50)

    return True


async def test_knowledge_retrieval():
    """Test specific knowledge retrieval scenarios."""
    print("\n🔍 Testing Knowledge Retrieval Scenarios")
    print("-" * 40)

    vector_store = VectorStoreService()
    rag_service = RAGService(vector_store)

    test_queries = [
        "meta description length",
        "mobile SEO optimization",
        "page loading speed",
        "internal linking strategy",
        "schema markup benefits",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        context = rag_service.get_relevant_context(query)

        if context:
            # Extract the first relevant knowledge point
            lines = context.split("\n")
            relevant_line = next(
                (line for line in lines if line.strip() and not line.startswith("#")),
                "",
            )
            print(f"   📚 Retrieved: {relevant_line[:100]}...")
        else:
            print("   ❌ No relevant context found")

    return True


if __name__ == "__main__":

    async def main():
        await test_rag_integration()
        await test_knowledge_retrieval()

    asyncio.run(main())
