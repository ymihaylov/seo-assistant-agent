from datetime import datetime

import pytz
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

SOFIA_TZ = pytz.timezone("Europe/Sofia")


def sofia_now():
    return datetime.now(SOFIA_TZ)


class SofiaTimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=sofia_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=sofia_now,
        onupdate=sofia_now,
        nullable=False,
    )
