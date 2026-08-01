from flask import Flask

from .config import Config
from .extensions import db, migrate, bcrypt, jwt
from .auth import auth_bp
from .routes import workout_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app=app, db=db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(workout_bp)
    
    from . import models

    return app