from app import create_app, db
from app.models.admin import User  # Assure-toi que ce chemin est correct
from app.models.Utilisateur import Utilisateur  # Assure-toi que ce chemin est correct
app = create_app()

with app.app_context():
    db.create_all()
    print("Tables créées avec succès")

    # Création d’un super admin si non existant
    super_admin_email = "mihajamariel@gmail.com"
    existing_user = User.query.filter_by(email=super_admin_email).first()

    if not existing_user:
        admin = User(
            email=super_admin_email,
            is_admin=True
        )
        admin.set_password("Mariel2005")
        db.session.add(admin)
        db.session.commit()
        print("Super administrateur créé avec succès.")
    else:
        print("Le super administrateur existe déjà.")
