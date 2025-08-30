import uuid

from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.enums import JobStatus
from app.models.timestamp_mixin import SofiaTimestampMixin


class Job(Base, SofiaTimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), nullable=False, index=True
    )
    session_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_message_id: Mapped[str] = mapped_column(
        String, ForeignKey("messages.id"), nullable=False, index=True
    )
    agent_message_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("messages.id"), nullable=True, index=True
    )

    status: Mapped[JobStatus] = mapped_column(
        String, nullable=False, default=JobStatus.PENDING, index=True
    )

    processing_time_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    user_message: Mapped["Message"] = relationship(
        "Message", foreign_keys=[user_message_id], post_update=True
    )
    agent_message: Mapped["Message"] = relationship(
        "Message", foreign_keys=[agent_message_id], post_update=True
    )
