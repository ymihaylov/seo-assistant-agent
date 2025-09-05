# RAG Integration with SEO Assistant

This document describes the RAG (Retrieval-Augmented Generation) integration added to the SEO Assistant project.

## Overview

The RAG system enhances the SEO agent by providing contextual knowledge retrieval from a curated SEO knowledge base. This allows the AI to give more informed, accurate, and comprehensive SEO recommendations.

## Architecture

```
User Query → RAG Service → Vector Store → Relevant Context → AI Agent → Enhanced Response
```

### Components

1. **VectorStoreService** (`app/services/rag/vector_store_service.py`)
   - Manages ChromaDB vector database
   - Handles document embedding and storage
   - Supports both OpenAI embeddings and ChromaDB default embeddings
   - Provides semantic search functionality

2. **RAGService** (`app/services/rag/rag_service.py`)
   - Orchestrates knowledge retrieval
   - Formats context for AI agent consumption
   - Enhances prompts with relevant SEO knowledge

3. **Enhanced Agent Graph** (`app/services/agent/agent_graph.py`)
   - Integrates RAG context into the suggestion pipeline
   - Retrieves relevant knowledge before AI processing

## Features

### Knowledge Base
The system includes curated SEO knowledge covering:
- Title tag optimization (50-60 characters, keyword placement)
- Meta descriptions (150-160 characters, compelling copy)
- Content strategy (300+ words, natural keyword integration)
- Header tag hierarchy (H1-H6 structure)
- Internal linking best practices
- Page performance optimization
- Mobile-first design principles
- Schema markup benefits

### Embedding Strategy
- **Primary**: OpenAI text-embedding-3-small (when API key available)
- **Fallback**: ChromaDB default embedding function
- Automatic fallback ensures system works without OpenAI API key

### Search & Retrieval
- Semantic similarity search
- Configurable result count (default: 3 documents)
- Metadata-enriched results with importance levels
- Distance-based relevance scoring

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Vector Database
```bash
python scripts/init_vector_db.py
```

### 3. Optional: Set OpenAI API Key
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Basic RAG Query
```python
from app.services.rag.vector_store_service import VectorStoreService
from app.services.rag.rag_service import RAGService

# Initialize services
vector_store = VectorStoreService()
rag_service = RAGService(vector_store)

# Get relevant context
context = rag_service.get_relevant_context(
    "How to optimize title tags",
    "E-commerce Product Page"
)
```

### SEO Agent with RAG
The RAG integration is automatic in the SEO agent pipeline:

```python
from app.services.agent.agent_graph import seo_graph

# Your query automatically gets RAG enhancement
result = await seo_graph.ainvoke({
    "session_title": "E-commerce SEO",
    "instructions": "Optimize my product page title tags",
    "constraints": {"title_max": 60}
})
```

## Testing

Run the comprehensive test suite:
```bash
python test_rag_integration.py
```

This tests:
- Vector store functionality
- RAG service context generation
- Complete SEO agent with RAG enhancement
- Knowledge retrieval scenarios

## File Structure

```
app/services/rag/
├── __init__.py
├── vector_store_service.py    # Vector database management
└── rag_service.py            # RAG orchestration

scripts/
└── init_vector_db.py         # Database initialization

test_rag_integration.py       # Comprehensive test suite
```

## Configuration

### Vector Store Settings
- **Database Path**: `./chroma_db` (configurable)
- **Collection Name**: `seo_knowledge`
- **Embedding Model**: `text-embedding-3-small` (OpenAI) or ChromaDB default

### RAG Settings
- **Default Results**: 3 documents per query
- **Context Format**: Markdown with importance levels
- **Search Strategy**: Semantic similarity with metadata filtering

## Performance Notes

- Initial embedding generation may take time for large knowledge bases
- ChromaDB provides persistent storage - no re-embedding needed
- OpenAI embeddings offer better semantic understanding but require API key
- Fallback embedding ensures system works offline

## Extending the Knowledge Base

Add new SEO knowledge by modifying the `initialize_seo_knowledge()` method in `VectorStoreService`:

```python
new_documents = [
    {
        'content': "Your SEO knowledge here...",
        'metadata': {'category': 'new_category', 'importance': 'high'}
    }
]
vector_store.add_documents(new_documents)
```

## Troubleshooting

### Common Issues

1. **ChromaDB Import Errors**
   - Ensure compatible numpy version: `pip install "numpy<2.0.0"`
   - Check ChromaDB version compatibility

2. **OpenAI API Errors**
   - System automatically falls back to ChromaDB embeddings
   - Set `OPENAI_API_KEY` environment variable for enhanced embeddings

3. **Empty Search Results**
   - Run initialization script: `python scripts/init_vector_db.py`
   - Check database path and permissions

### Performance Optimization

- Use OpenAI embeddings for better semantic understanding
- Adjust `n_results` parameter based on context window limits
- Consider batch processing for large knowledge base updates

## Integration Benefits

1. **Enhanced Accuracy**: AI responses backed by curated SEO knowledge
2. **Consistency**: Standardized SEO recommendations across all queries
3. **Contextual Relevance**: Dynamic knowledge retrieval based on user queries
4. **Scalability**: Easy to extend knowledge base without retraining
5. **Fallback Support**: Works with or without external API dependencies

## Future Enhancements

- Dynamic knowledge base updates from SEO industry sources
- User-specific knowledge customization
- Advanced filtering by SEO category or importance
- Integration with real-time SEO data sources
- Multi-language SEO knowledge support
