from flask import request
from flask_socketio import emit

from app.extensions import socketio
from .helpers import (
    connected_users,
    decode_token,
    get_username_from_sid,
    get_sid_from_username,
    user_exists,
)


@socketio.on("connect")
def on_connect():
    token = request.args.get("token")
    sid: str = request.sid  # type: ignore

    username = decode_token(token) if token else None
    if not username:
        return False

    connected_users[username] = sid


@socketio.on("disconnect")
def on_disconnect():
    sid: str = request.sid  # type: ignore

    username = get_username_from_sid(sid)
    if username:
        del connected_users[username]
        emit("user_offline", {"username": username}, broadcast=True)


@socketio.on("announce_online")
def on_announce_online():
    sid: str = request.sid  # type: ignore
    username = get_username_from_sid(sid)
    if username:
        emit("user_online", {"username": username}, broadcast=True, include_self=False)


@socketio.on("contact_request")
def on_contact_request(data: dict):
    sid: str = request.sid  # type: ignore
    to_username = data.get("to_username")
    from_pubkey = data.get("from_pubkey")

    from_username = get_username_from_sid(sid)
    target_sid = get_sid_from_username(to_username) if to_username else None

    if not from_username or not to_username or not from_pubkey:
        return {"status": "error", "reason": "Missing required fields"}

    if not user_exists(to_username):
        return {"status": "error", "reason": "User does not exist"}

    if not target_sid:
        return {"status": "error", "reason": "User is not online"}

    emit("contact_request", {"from_username": from_username, "from_pubkey": from_pubkey}, to=target_sid)
    return {"status": "ok"}


@socketio.on("contact_accept")
def on_contact_accept(data: dict):
    sid: str = request.sid  # type: ignore
    to_username = data.get("to_username")
    from_pubkey = data.get("from_pubkey")

    from_username = get_username_from_sid(sid)
    target_sid = get_sid_from_username(to_username) if to_username else None

    if not from_username or not to_username or not from_pubkey:
        return {"status": "error", "reason": "Missing required fields"}

    if not user_exists(to_username):
        return {"status": "error", "reason": "User does not exist"}

    if not target_sid:
        return {"status": "error", "reason": "User is not online"}

    emit("contact_accept", {"from_username": from_username, "from_pubkey": from_pubkey}, to=target_sid)
    return {"status": "ok"}


@socketio.on("send_message")
def on_send_message(data: dict):
    sid: str = request.sid  # type: ignore
    to_username = data.get("to_username")
    content = data.get("content")

    print(content)
    
    from_username = get_username_from_sid(sid)
    target_sid = get_sid_from_username(to_username) if to_username else None

    if not from_username or not to_username or not content:
        return {"status": "error", "reason": "Missing required fields"}

    if not target_sid:
        return {"status": "error", "reason": "User is not online"}

    emit("message", {"from_username": from_username, "content": content}, to=target_sid)
    return {"status": "ok"}
