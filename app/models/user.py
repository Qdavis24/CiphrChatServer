from datetime import datetime, timezone

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class User(db.Model):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(String(60), primary_key=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __init__(self, username: str, password_hash: str) -> None:
        self.username = username
        self.password_hash = password_hash

    def __repr__(self) -> str:
        return f"<User {self.username}>"
