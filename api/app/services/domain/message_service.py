from typing import List, Optional, Dict, Any

from app.models.message import Message
from app.repositories.message import MessageRepository
from app.schemas.message import MessageOut


class MessageTransformer:
    def to_message_out(self, message: Message) -> MessageOut:
        return MessageOut(
            id=message.id,
            role=message.role,
            message_content=message.message_content or "",
            suggested_page_title=message.suggested_page_title,
            suggested_page_content=message.suggested_page_content,
            suggested_title_tag=message.suggested_title_tag,
            suggested_meta_description=message.suggested_meta_description,
            suggested_meta_keywords=message.suggested_meta_keywords,
            created_at=message.created_at.isoformat() if message.created_at else "",
            updated_at=message.updated_at.isoformat() if message.updated_at else "",
        )

    def normalize_suggestions(self, suggestions: dict) -> dict:
        return {
            "page_title": suggestions.get("page_title") or None,
            "page_content": suggestions.get("page_content") or "",
            "title_tag": suggestions.get("title_tag") or None,
            "meta_description": suggestions.get("meta_description") or None,
            "meta_keywords": list(suggestions.get("meta_keywords") or []),
        }


class MessageService:
    def __init__(
        self,
        message_repo: MessageRepository,
        transformer: MessageTransformer,
    ):
        self._message_repo = message_repo
        self._transformer = transformer

    def create_user_message(self, session_id: str, content: str) -> Message:
        return self._message_repo.create_user_message(session_id, content)

    def create_agent_message(
        self, session_id: str, raw_suggestions: dict
    ) -> MessageOut:
        normalized_suggestions = self._transformer.normalize_suggestions(
            raw_suggestions
        )
        message = self._message_repo.create_agent_message(
            session_id, normalized_suggestions
        )

        return self._transformer.to_message_out(message)

    def get_session_messages(
        self, session_id: str, limit: int = 100, offset: int = 0
    ) -> List[MessageOut]:
        messages = self._message_repo.get_session_messages(session_id, limit, offset)

        return [self._transformer.to_message_out(msg) for msg in messages]

    def get_first_message(self, session_id: str) -> Optional[Message]:
        return self._message_repo.get_first_message_of_session(session_id)

    def get_last_agent_message(self, session_id: str) -> Optional[Message]:
        return self._message_repo.get_last_agent_message(session_id)

    def extract_suggestions(self, message: Message) -> Dict[str, Any]:
        suggestions = {}

        field_mapping = {
            "suggested_page_title": "page_title",
            "suggested_page_content": "page_content",
            "suggested_title_tag": "title_tag",
            "suggested_meta_description": "meta_description",
            "suggested_meta_keywords": "meta_keywords",
        }

        for db_field, context_field in field_mapping.items():
            value = getattr(message, db_field, None)
            if value is not None:
                suggestions[context_field] = value

        return suggestions
