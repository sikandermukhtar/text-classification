import uuid
from sqlalchemy import String, ForeignKey, Text, DateTime, func, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from config.base import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_auth import UserAuth
    from .verification_token import VerificationToken

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    phone_number: Mapped[str] = mapped_column(String(18), unique=True, nullable=True)
    profile_img_url: Mapped[str] = mapped_column(Text, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    auth: Mapped["UserAuth"] = relationship("UserAuth", back_populates="user", cascade="all, delete-orphan")
    verification_token: Mapped["VerificationToken"] = relationship("VerificationToken", back_populates="user", cascade="all, delete-orphan")

    