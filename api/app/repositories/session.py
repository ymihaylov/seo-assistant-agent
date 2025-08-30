from typing import Optional, List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session as OrmSession

from app.models import Session as SessionModel, Message


class SessionRepository:
    def __init__(self, db: OrmSession):
        self._db = db

    def create_session(self, user_id: str, title: str) -> SessionModel:
        session = SessionModel(user_id=user_id, title=title)
        self._db.add(session)
        self._db.flush()
        return session

    def get_session_by_id(
        self, session_id: str, user_id: str
    ) -> Optional[SessionModel]:
        return (
            self._db.query(SessionModel)
            .filter(SessionModel.id == session_id, SessionModel.user_id == user_id)
            .first()
        )

    def get_user_sessions(
        self, user_id: str, limit: int, offset: int
    ) -> List[tuple[SessionModel, Optional[str]]]:
        latest_message_subquery = (
            self._db.query(
                Message.session_id,
                func.max(Message.created_at).label("last_message_at"),
            )
            .group_by(Message.session_id)
            .subquery()
        )

        sessions_query = (
            self._db.query(SessionModel, latest_message_subquery.c.last_message_at)
            .outerjoin(
                latest_message_subquery,
                SessionModel.id == latest_message_subquery.c.session_id,
            )
            .filter(SessionModel.user_id == user_id)
            .order_by(
                desc(latest_message_subquery.c.last_message_at),
                desc(SessionModel.created_at),  # fallback for sessions without messages
            )
            .offset(offset)
            .limit(limit)
        )

        return sessions_query.all()

    def update_session(self, session: SessionModel, **kwargs) -> SessionModel:
        for key, value in kwargs.items():
            setattr(session, key, value)

        self._db.commit()
        self._db.refresh(session)

        return session

    def delete_session(self, session: SessionModel) -> None:
        self._db.delete(session)
        self._db.commit()
