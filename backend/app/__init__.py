# app/__init__.py

from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt
from flask_cors import CORS
from app.models.Base_de_donne import User, Enquete, QuestionEnquete, ReponseEnquete, Campagne, Personne, Profil
from app.routes import main

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    from app.routes import main
    app.register_blueprint(main)

    return app
