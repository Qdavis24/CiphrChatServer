import jwt
from flask import current_app

from app.models import User

connected_users: dict[str, str] = {}  # username -> sid


def make_token(user: User) -> str:
    payload = {
        "sub": user.username,
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None


def get_username_from_sid(sid: str) -> str | None:
    for u, s in connected_users.items():
        if sid == s:
            return u
    return None


def get_sid_from_username(username: str) -> str | None:
    return connected_users.get(username)


def user_exists(username: str) -> bool:
    return User.query.filter_by(username=username).first() is not None
