from datetime import timedelta
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    SQLALCHEMY_DATABASE_URI = "sqlite:///workout.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
