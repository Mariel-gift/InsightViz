# create_db.py
from app import create_app
from app.extensions import db, bcrypt
from app.models.Base_de_donne import (
    User, Enquete, QuestionEnquete, ReponseEnquete, Campagne,
    Personne, Profil
)

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès.")

    # ============================================================
    # SUPER ADMIN
    # ============================================================
    super_admin_email = "mihajamariel@gmail.com"
    existing_user = User.query.filter_by(email=super_admin_email).first()

    if not existing_user:
        admin = User(
            full_name="Admin Mariel",
            email=super_admin_email,
            role="admin"
        )
        admin.password = "Mariel2005"
        db.session.add(admin)
        db.session.commit()
        print("✅ Super administrateur créé avec succès.")
    else:
        print("ℹ️  Le super administrateur existe déjà.")

    # ============================================================
    # DONNÉES DE TEST : Campagne + Enquête + Questions
    # ============================================================
    if not Campagne.query.first():
        campagne = Campagne(
            nom="Campagne Test",
            description="Campagne d’essai pour tests initiaux",
            groupe_cible="les deux"
        )
        db.session.add(campagne)
        db.session.flush()  # Pour avoir campagne.id

        enquete = Enquete(
            titre="Enquête de satisfaction",
            campagne_id=campagne.id
        )
        db.session.add(enquete)
        db.session.flush()

        questions = [
            QuestionEnquete(
                texte="Êtes-vous satisfait du service ?",
                ordre=1,
                enquete_id=enquete.id
            ),
            QuestionEnquete(
                texte="Recommanderiez-vous notre service ?",
                ordre=2,
                enquete_id=enquete.id
            )
        ]
        db.session.add_all(questions)
        db.session.commit()
