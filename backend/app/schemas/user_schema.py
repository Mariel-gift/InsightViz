from .. import ma
from ..models.admin import User
from marshmallow import fields, validate

class UserRegisterSchema(ma.SQLAlchemyAutoSchema):
    # Schéma pour l'inscription
    full_name = fields.Str(required=True, validate=validate.Length(min=2))
    company = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8), load_only=True)

    class Meta:
        model = User
        fields = ("full_name", "company", "email", "password", "wants_newsletter", "agreeToTerms")
        load_instance = True # Permet de créer un objet User directement

class UserSchema(ma.SQLAlchemyAutoSchema):
    # Schéma pour afficher les infos de l'utilisateur (SANS le mot de passe)
    class Meta:
        model = User
        fields = ("id", "full_name", "company", "email", "wants_newsletter", "created_at")

# Instancier les schémas
user_register_schema = UserRegisterSchema()
user_schema = UserSchema()