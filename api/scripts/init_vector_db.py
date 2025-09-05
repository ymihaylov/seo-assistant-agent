#!/usr/bin/env python3
"""
Script to initialize the vector database with SEO knowledge.
Run this script to set up the RAG system for the first time.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.rag.vector_store_service import VectorStoreService


def main():
    """Initialize the vector database with SEO knowledge."""
    print("Initializing SEO knowledge vector database...")

    try:
        # Initialize vector store
        vector_store = VectorStoreService()

        # Initialize with SEO knowledge
        vector_store.initialize_seo_knowledge()

        print("Vector database initialized successfully!")
        print(f"Database location: {vector_store.persist_directory}")

        # Test the search functionality
        print("\nTesting search functionality...")
        test_results = vector_store.search_similar(
            "title tag optimization", n_results=2
        )

        if test_results:
            print(f"Found {len(test_results)} relevant documents:")
            for i, result in enumerate(test_results, 1):
                print(f"  {i}. {result['content'][:100]}...")
        else:
            print("No results found in test search")

    except Exception as e:
        print(f"Error initializing vector database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
