from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token

from ..schemas.user_schema import user_register_schema, user_schema
from .. import db

auth_bp = Blueprint('auth', __name__)

# Route OPTIONS pour /register (CORS preflight)
@auth_bp.route('/register', methods=['OPTIONS'])
def register_options():
    return '', 200

@auth_bp.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        # Valider et désérialiser les données
        data = user_register_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists"}), 409

    # Créer un nouvel utilisateur
    new_user = User(
        full_name=data['full_name'],
        company=data['company'],
        email=data['email'],
        wants_newsletter=data.get('newsletter', False),
        terms_agreed_at=datetime.utcnow() if data.get('agreeToTerms') else None
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    
    email = json_data.get('email')
    password = json_data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Créer les tokens JWT
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            "message": "Logged in successfully",
            "tokens": {
                "access": access_token,
                "refresh": refresh_token
            },
            "user": user_schema.dump(user) # Renvoyer les infos de l'utilisateur
        }), 200
    
    return jsonify({"message": "Invalid email or password"}), 401