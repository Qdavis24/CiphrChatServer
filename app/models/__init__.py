from app.extensions import db

from .user import User  # noqa: E402, F401

__all__ = ["db", "User"]
