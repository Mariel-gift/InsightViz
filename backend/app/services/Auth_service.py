from ..models.admin import User
from .. import db
from flask_jwt_extended import create_access_token

def register_user(data):
    """
    Service pour enregistrer un nouvel utilisateur.
    Contient la logique métier.
    """
    email = data.get('email')
    if User.query.filter_by(email=email).first():
        # Lève une exception si l'email existe déjà
        raise ValueError('Cette adresse email est déjà utilisée.')

    # Crée une nouvelle instance de User
    new_user = User(
        full_name=data.get('full_name'),
        company=data.get('company'),
        email=email,
        newsletter_subscribed=data.get('newsletter_subscribed', False)
    )
    # Le mot de passe est hashé via la méthode set_password
    new_user.set_password(data.get('password'))

    # Sauvegarde en base de données
    db.session.add(new_user)
    db.session.commit()
    
    return new_user

def login_user(email, password):
    """
    Service pour connecter un utilisateur.
    Retourne un token JWT si les identifiants sont valides, sinon None.
    """
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # Création du token JWT
        access_token = create_access_token(identity=user.id)
        return access_token
    return None