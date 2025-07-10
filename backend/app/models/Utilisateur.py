from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    mot_de_passe_hash = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.String(100))  # ← Champ pour le nom complet
    terms_agreed_at = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Hash du mot de passe."""
        self.mot_de_passe_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe donné par rapport au hash."""
        return check_password_hash(self.mot_de_passe_hash, password)

    def __repr__(self):
        return f'<Utilisateur {self.email}>'
