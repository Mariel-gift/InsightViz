from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from datetime import datetime
from app.models import Utilisateur
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "Bienvenue sur le serveur Flask !"


@main.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()

    full_name = data.get('full_name')
    company = data.get('company')
    email = data.get('email')
    password = data.get('password')
    wants_newsletter = data.get('wants_newsletter', False)
    agree_to_terms = data.get('agree_to_terms', False)

    if not full_name or not company or not email or not password or not agree_to_terms:
        return jsonify({"error": "Champs manquants ou conditions non acceptées"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email déjà utilisé"}), 409

    new_user = User(
        full_name=full_name,
        company=company,
        email=email,
        wants_newsletter=wants_newsletter,
        terms_agreed_at=datetime.utcnow()
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Inscription réussie"}), 201


@main.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Champs manquants"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Email ou mot de passe incorrect."}), 401

    return jsonify({
        "tokens": {
            "access": "fake_access_token",
            "refresh": "fake_refresh_token"
        },
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200


@main.route('/api/utilisateurs', methods=['GET', 'OPTIONS'])
def get_utilisateurs():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "nom": getattr(u, 'full_name', 'N/A'),
            "email": u.email,
            "date_inscription": u.terms_agreed_at.strftime('%Y-%m-%d') if u.terms_agreed_at else ""
        })
    return jsonify(result), 200


@main.route('/utilisateurs', methods=['POST'])
def create_utilisateur():
    data = request.get_json()

    nom = data.get('nom')  # ← Nouveau champ
    email = data.get('email')
    motdepasse = data.get('motdepasse')
    role = data.get('role')

    if not nom or not email or not motdepasse or not role:
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email déjà utilisé'}), 409

    new_user = User(
        full_name=nom,  # ← Enregistrement du nom
        email=email,
        role=role,
        terms_agreed_at=datetime.utcnow()
    )
    new_user.set_password(motdepasse)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Utilisateur créé avec succès'}), 201
