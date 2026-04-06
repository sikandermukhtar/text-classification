import uuid
from sqlalchemy import String, ForeignKey, Text, DateTime, text, func, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.config.base import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    token: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_used: Mapped[bool] = mapped_column(
        Boolean, server_default=text("'false'"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="verification_token")
