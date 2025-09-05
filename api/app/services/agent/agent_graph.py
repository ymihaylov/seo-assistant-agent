# app/services/agent_graph.py
from __future__ import annotations

from typing import List

from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field, ValidationError

from .llm import chat_json
from .prompt_builder import SEOPromptBuilder
from .prompts import SYSTEM_PROMPT
from .score import score_result
from ..rag.rag_service import RAGService
from ..rag.vector_store_service import VectorStoreService


class Suggestion(BaseModel):
    page_title: str | None = None
    page_content: str = ""
    title_tag: str | None = None
    meta_description: str | None = None
    meta_keywords: List[str] = Field(default_factory=list)


prompt_builder = SEOPromptBuilder()

# Initialize RAG components
vector_store = VectorStoreService()
rag_service = RAGService(vector_store)

vector_store.initialize_seo_knowledge()


async def suggest_node(state: dict):
    user_query = state.get("instructions", "")
    session_title = state.get("session_title", "")

    rag_context = rag_service.get_relevant_context(user_query, session_title)
    if rag_context:
        state["rag_context"] = rag_context

    raw = await chat_json(SYSTEM_PROMPT, prompt_builder.build_user_payload(state))

    suggestions = {
        "page_title": raw.get("page_title") or raw.get("suggested_page_title"),
        "page_content": raw.get("page_content")
        or raw.get("suggested_page_content")
        or "",
        "title_tag": raw.get("title_tag") or raw.get("suggested_title_tag"),
        "meta_description": raw.get("meta_description")
        or raw.get("suggested_meta_description"),
        "meta_keywords": raw.get("meta_keywords")
        or raw.get("suggested_meta_keywords")
        or [],
    }

    return {"suggestions": suggestions}


def validate_node(state: dict):
    data = state["suggestions"]
    try:
        valid = Suggestion.model_validate(data).model_dump()
    except ValidationError:
        valid = Suggestion(
            page_title=data.get("page_title") or None,
            page_content=str(data.get("page_content") or ""),
            title_tag=data.get("title_tag") or None,
            meta_description=data.get("meta_description") or None,
            meta_keywords=list(data.get("meta_keywords") or []),
        ).model_dump()

    # compute score here (optional)
    score = score_result(valid)
    return {"suggestions": valid, "score": score}


_graph = StateGraph(dict)
_graph.add_node("suggest", suggest_node)
_graph.add_node("validate", validate_node)

_graph.set_entry_point("suggest")

_graph.add_edge("suggest", "validate")
_graph.add_edge("validate", END)

seo_graph = _graph.compile()
