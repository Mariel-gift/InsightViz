from datetime import datetime
from enum import Enum
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db

# ====================================================================
# 0.  Énumérations Python  (liées aux ENUM Postgres)
# ====================================================================

class RoleEnum(str, Enum):
    ADMIN       = "admin"
    USER        = "user"
    SUPERADMIN  = "superadmin"

class TypePersonneEnum(str, Enum):
    TRANSPORTEUR = "transporteur"
    EXPEDITEUR   = "expediteur"

# ====================================================================
# 1.  Utilisateurs
# ====================================================================

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_role", "role"),
    )

    id             = db.Column(db.Integer, primary_key=True)
    full_name      = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(150), nullable=False, unique=True)
    _password_hash = db.Column("password_hash", db.Text, nullable=False)
    role           = db.Column(db.Enum(RoleEnum, name="role_enum"), default=RoleEnum.USER, nullable=False)

    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @hybrid_property
    def password(self):
        raise AttributeError("Le mot de passe n'est pas accessible.")

    @password.setter
    def password(self, raw_pwd):
        from flask_bcrypt import generate_password_hash
        self._password_hash = generate_password_hash(raw_pwd).decode("utf-8")

    def check_password(self, raw_pwd):
        from flask_bcrypt import check_password_hash
        return check_password_hash(self._password_hash, raw_pwd)

    def __repr__(self):
        return f"<User {self.id} {self.email} ({self.role})>"

# ====================================================================
# 2.  Personnes
# ====================================================================

class Personne(db.Model):
    __tablename__ = "personnes"

    id                = db.Column(db.Integer, primary_key=True)
    nom               = db.Column(db.String(100), nullable=False)
    region            = db.Column(db.String(100))
    email_contact     = db.Column(db.String(120))
    telephone         = db.Column(db.String(20))
    type              = db.Column(db.Enum(TypePersonneEnum, name="type_personne_enum"), nullable=False)
    taille_entreprise = db.Column(db.String(50))
    secteur_activite  = db.Column(db.String(100))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at        = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reponses = db.relationship("ReponseEnquete", back_populates="personne", cascade="all, delete-orphan")
    profils  = db.relationship("Profil", back_populates="personne", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Personne {self.id} - {self.nom}>"

# ====================================================================
# 3.  Campagnes
# ====================================================================

class Campagne(db.Model):
    __tablename__ = "campagnes"

    id           = db.Column(db.Integer, primary_key=True)
    nom          = db.Column(db.String(100), nullable=False)
    description  = db.Column(db.Text)
    groupe_cible = db.Column(db.String(20))
    date_debut   = db.Column(db.Date)
    date_fin     = db.Column(db.Date)
    statut       = db.Column(db.String(20), default="active")

    enquetes = db.relationship("Enquete", back_populates="campagne", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campagne {self.id} - {self.nom}>"

# ====================================================================
# 4.  Enquêtes & Questions
# ====================================================================

class Enquete(db.Model):
    __tablename__ = "enquetes"

    id             = db.Column(db.Integer, primary_key=True)
    titre          = db.Column(db.String(255), nullable=False)
    description    = db.Column(db.Text)
    date_creation  = db.Column(db.DateTime, default=datetime.utcnow)

    campagne_id = db.Column(db.Integer, db.ForeignKey("campagnes.id", ondelete="SET NULL"))
    campagne    = db.relationship("Campagne", back_populates="enquetes")

    questions = db.relationship("QuestionEnquete", back_populates="enquete", cascade="all, delete-orphan", order_by="QuestionEnquete.ordre")
    reponses  = db.relationship("ReponseEnquete",  back_populates="enquete", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Enquete {self.id} - {self.titre}>"

class QuestionEnquete(db.Model):
    __tablename__ = "questions_enquete"
    __table_args__ = (UniqueConstraint("enquete_id", "ordre", name="uq_enquete_ordre"),)

    id         = db.Column(db.Integer, primary_key=True)
    texte      = db.Column(db.Text, nullable=False)
    ordre      = db.Column(db.Integer, nullable=False)

    enquete_id = db.Column(db.Integer, db.ForeignKey("enquetes.id", ondelete="CASCADE"), nullable=False)
    enquete    = db.relationship("Enquete", back_populates="questions")

# ====================================================================
# 5.  Réponses aux enquêtes
# ====================================================================

class ReponseEnquete(db.Model):
    __tablename__ = "reponses_enquetes"
    __table_args__ = (
        UniqueConstraint("enquete_id", "personne_id", name="uq_reponse_enquete_personne"),
        Index("idx_reponses_enquete_enquete", "enquete_id"),
    )

    id              = db.Column(db.Integer, primary_key=True)
    enquete_id      = db.Column(db.Integer, db.ForeignKey("enquetes.id", ondelete="CASCADE"), nullable=False)
    personne_id     = db.Column(db.Integer, db.ForeignKey("personnes.id", ondelete="CASCADE"), nullable=False)
    donnees_reponse = db.Column(JSONB, nullable=False)
    submitted_at    = db.Column(db.DateTime, default=datetime.utcnow)

    enquete  = db.relationship("Enquete",   back_populates="reponses")
    personne = db.relationship("Personne",  back_populates="reponses")

# ====================================================================
# 6.  Profils
# ====================================================================

class Profil(db.Model):
    __tablename__ = "profils"

    id          = db.Column(db.Integer, primary_key=True)
    personne_id = db.Column(db.Integer, db.ForeignKey("personnes.id", ondelete="CASCADE"), nullable=False)
    score       = db.Column(db.Integer)
    segment     = db.Column(db.String(100))
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    personne    = db.relationship("Personne", back_populates="profils")

# ====================================================================
# 7.  Journaux d’analyses
# ====================================================================

class JournalAnalyse(db.Model):
    __tablename__ = "journaux_analyses"

    id              = db.Column(db.Integer, primary_key=True)
    type_execution  = db.Column(db.String(50))
    resume_resultat = db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<JournalAnalyse {self.id} - {self.type_execution}>"
