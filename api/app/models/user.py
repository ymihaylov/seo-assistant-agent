import uuid

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.timestamp_mixin import SofiaTimestampMixin


class User(Base, SofiaTimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    auth_sub: Mapped[str | None] = mapped_column(
        String(255), unique=True, index=True, nullable=True
    )
    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, index=True, nullable=True
    )
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    profile: Mapped[dict | None] = mapped_column(JSON, nullable=True)
