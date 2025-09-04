from typing import List, Optional

from sqlalchemy.orm import Session as OrmSession

from app.models import Message


class MessageRepository:
    def __init__(self, db: OrmSession):
        self._db = db

    def create_user_message(self, session_id: str, content: str) -> Message:
        message = Message(
            session_id=session_id,
            role="user",
            message_content=content,
        )
        self._db.add(message)
        self._db.flush()

        return message

    def create_agent_message(self, session_id: str, suggestions: dict) -> Message:
        message = Message(
            session_id=session_id,
            role="agent",
            message_content="",
            suggested_page_title=suggestions.get("page_title"),
            suggested_page_content=suggestions.get("page_content"),
            suggested_title_tag=suggestions.get("title_tag"),
            suggested_meta_description=suggestions.get("meta_description"),
            suggested_meta_keywords=suggestions.get("meta_keywords"),
        )
        self._db.add(message)
        self._db.flush()

        return message

    def get_session_messages(
        self, session_id: str, limit: int, offset: int
    ) -> List[Message]:
        return (
            self._db.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.created_at.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_first_message_of_session(self, session_id: str) -> Optional[Message]:
        return (
            self._db.query(Message)
            .filter(Message.session_id == session_id, Message.role == "user")
            .order_by(Message.created_at.asc())
            .first()
        )

    def get_last_agent_message(self, session_id: str) -> Optional[Message]:
        return (
            self._db.query(Message)
            .filter(Message.session_id == session_id, Message.role == "agent")
            .order_by(Message.created_at.desc())
            .first()
        )
