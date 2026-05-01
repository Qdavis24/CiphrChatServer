import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", None)
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", None)


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
