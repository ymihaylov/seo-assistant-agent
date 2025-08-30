from typing import List, Optional

from app.models.session import Session as SessionModel
from app.repositories.session import SessionRepository
from app.schemas.session import (
    SessionListResponse,
    SessionUpdateRequest,
    SessionUpdateResponse,
)


class AutoTitleGenerator:
    def generate_title(self, message: str, max_length: int = 30) -> str:
        text = " ".join(message.split())
        return (
            (text[: max_length - 1] + "…")
            if len(text) > max_length
            else (text or "New session")
        )


class SessionService:
    def __init__(
        self,
        session_repo: SessionRepository,
        title_generator: AutoTitleGenerator,
    ):
        self._session_repo = session_repo
        self._title_generator = title_generator

    def create_session(
        self, user_id: str, title: Optional[str], first_message: str
    ) -> SessionModel:
        session_title = title or self._title_generator.generate_title(first_message)

        return self._session_repo.create_session(user_id, session_title)

    def get_session(self, session_id: str, user_id: str) -> Optional[SessionModel]:
        return self._session_repo.get_session_by_id(session_id, user_id)

    def get_user_sessions(
        self, user_id: str, limit: int = 50, offset: int = 0
    ) -> List[SessionListResponse]:
        sessions_data = self._session_repo.get_user_sessions(user_id, limit, offset)

        return [
            SessionListResponse(
                id=session.id,
                title=session.title,
                created_at=session.created_at.isoformat(),
                updated_at=session.updated_at.isoformat(),
                last_message_at=(
                    last_message_at.isoformat()
                    if last_message_at
                    else session.created_at.isoformat()
                ),
            )
            for session, last_message_at in sessions_data
        ]

    def update_session(
        self, session_id: str, user_id: str, update_data: SessionUpdateRequest
    ) -> Optional[SessionUpdateResponse]:
        session = self.get_session(session_id, user_id)
        if not session:
            return None

        update_fields = {}
        if update_data.title is not None:
            update_fields["title"] = update_data.title

        if update_fields:
            updated_session = self._session_repo.update_session(
                session, **update_fields
            )

            return SessionUpdateResponse(
                id=updated_session.id,
                title=updated_session.title,
                updated_at=updated_session.updated_at.isoformat(),
            )

        return SessionUpdateResponse(
            id=session.id,
            title=session.title,
            updated_at=session.updated_at.isoformat(),
        )

    def delete_session(self, session_id: str, user_id: str) -> bool:
        session = self.get_session(session_id, user_id)

        if not session:
            return False

        self._session_repo.delete_session(session)
        return True
