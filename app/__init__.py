import dotenv
dotenv.load_dotenv()

from flask import Flask
from flask_cors import CORS

from .config import config_map
from .extensions import db, socketio
from .routes import auth_bp, users_bp
from .routes import socket_events


def create_app() -> Flask:

    app = Flask(__name__)
    app.config.from_object(config_map["development"])

    db.init_app(app)

    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

    return app
