from typing import Optional
from sqlalchemy import CheckConstraint, or_
from app.infrastructure.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(unique=True)
    password: Mapped[Optional[str]] = mapped_column()
    google_access_token: Mapped[Optional[str]] = mapped_column()
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    name: Mapped[Optional[str]] = mapped_column()
