import uuid

from sqlalchemy import String, Text, ForeignKey, JSON, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.timestamp_mixin import SofiaTimestampMixin


class Message(Base, SofiaTimestampMixin):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # 'user' or 'agent'
    role: Mapped[str] = mapped_column(String(10), nullable=False, index=True)

    message_content: Mapped[str] = mapped_column(Text, nullable=True)

    # Agent Responses
    suggested_page_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    suggested_page_content: Mapped[str] = mapped_column(Text, nullable=True)
    suggested_title_tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    suggested_meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggested_meta_keywords: Mapped[list[str] | None] = mapped_column(
        JSON, nullable=True
    )

    session: Mapped["Session"] = relationship("Session", back_populates="messages")

    __table_args__ = (
        CheckConstraint("role IN ('user','agent')", name="ck_messages_role"),
    )
