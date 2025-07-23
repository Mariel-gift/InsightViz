from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from enum import Enum


# ==============================================================
# 1. UTILISATEURS (administration)
# ==============================================================

class Role(Enum):
    UTILISATEUR = "utilisateur"
    ADMIN       = "admin"
    SUPERADMIN  = "super_admin"


class Utilisateur(db.Model):
    __tablename__ = "utilisateurs"

    id             = db.Column(db.Integer, primary_key=True)
    email          = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.Text, nullable=False)
    role           = db.Column(db.Enum(Role), default=Role.UTILISATEUR, nullable=False)
    date_creation  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Utilisateur {self.id} – {self.email}>"


# ==============================================================
# 2. PERSONNES  (transporteur / expéditeur)
# ==============================================================

class TypePersonne(Enum):
    TRANSPORTEUR = "transporteur"
    EXPEDITEUR   = "expediteur"


class Personne(db.Model):
    __tablename__ = "personnes"

    id                = db.Column(db.Integer, primary_key=True)
    nom               = db.Column(db.String(100), nullable=False)
    region            = db.Column(db.String(100))
    email_contact     = db.Column(db.String(100))
    telephone         = db.Column(db.String(20))
    type              = db.Column(db.Enum(TypePersonne), nullable=False)
    taille_entreprise = db.Column(db.String(50))      # transporteur
    secteur_activite  = db.Column(db.String(100))     # expéditeur
    date_creation     = db.Column(db.DateTime, default=datetime.utcnow)

    # ---- relations ----
    profils           = db.relationship("Profil", back_populates="personne",
                                         cascade="all, delete-orphan")
    reponses          = db.relationship("ReponseEnquete", back_populates="personne",
                                         cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Personne {self.id} – {self.nom} ({self.type.value})>"


# ==============================================================
# 3. CAMPAGNES MARKETING
# ==============================================================

class Campagne(db.Model):
    __tablename__ = "campagnes"

    id           = db.Column(db.Integer, primary_key=True)
    nom          = db.Column(db.String(100), nullable=False)
    description  = db.Column(db.Text)
    groupe_cible = db.Column(db.String(50))         # 'expediteur', 'transporteur', 'les deux'
    date_debut   = db.Column(db.Date)
    date_fin     = db.Column(db.Date)
    statut       = db.Column(db.String(20), default="active")

    # ---- relations ----
    enquetes = db.relationship("Enquete", back_populates="campagne",
                               cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campagne {self.id} – {self.nom}>"


# ==============================================================
# 4. ENQUÊTES
# ==============================================================

class Enquete(db.Model):
    __tablename__ = "enquetes"

    id            = db.Column(db.Integer, primary_key=True)
    titre         = db.Column(db.String(255), nullable=False)
    description   = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    # FK campagne (nullable)
    campagne_id   = db.Column(db.Integer, db.ForeignKey("campagnes.id",
                                                        ondelete="SET NULL"))
    campagne      = db.relationship("Campagne", back_populates="enquetes")

    # ---- relations ----
    reponses = db.relationship("ReponseEnquete", back_populates="enquete",
                               cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Enquete {self.id} – {self.titre}>"


# ==============================================================
# 5. RÉPONSES AUX ENQUÊTES
# ==============================================================

class ReponseEnquete(db.Model):
    __tablename__ = "reponses_enquetes"

    id              = db.Column(db.Integer, primary_key=True)

    enquete_id      = db.Column(db.Integer,
                                db.ForeignKey("enquetes.id", ondelete="CASCADE"),
                                nullable=False)
    personne_id     = db.Column(db.Integer,
                                db.ForeignKey("personnes.id", ondelete="CASCADE"),
                                nullable=False)

    donnees_reponse = db.Column(db.JSON, nullable=False)
    date_soumission = db.Column(db.DateTime, default=datetime.utcnow)

    # ---- relations ----
    enquete         = db.relationship("Enquete", back_populates="reponses")
    personne        = db.relationship("Personne", back_populates="reponses")

    def __repr__(self):
        return f"<Reponse {self.id} – Enquête {self.enquete_id} / Personne {self.personne_id}>"


# ==============================================================
# 6. PROFILS (segmentation / scoring)
# ==============================================================

class Profil(db.Model):
    __tablename__ = "profils"

    id               = db.Column(db.Integer, primary_key=True)
    personne_id      = db.Column(db.Integer,
                                 db.ForeignKey("personnes.id", ondelete="CASCADE"),
                                 nullable=False)
    score            = db.Column(db.Integer)
    segment          = db.Column(db.String(100))
    date_mise_a_jour = db.Column(db.DateTime, default=datetime.utcnow)

    # ---- relations ----
    personne         = db.relationship("Personne", back_populates="profils")

    def __repr__(self):
        return f"<Profil {self.id} – P{self.personne_id} (score={self.score})>"


# ==============================================================
# 7. JOURNAUX D’ANALYSES AUTOMATIQUES
# ==============================================================

class JournalAnalyse(db.Model):
    __tablename__ = "journaux_analyses"

    id             = db.Column(db.Integer, primary_key=True)
    type_execution = db.Column(db.String(50))   # ex: 'analyse_tendance'
    resume_resultat = db.Column(db.Text)
    date_creation   = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<JournalAnalyse {self.id} – {self.type_execution}>"

