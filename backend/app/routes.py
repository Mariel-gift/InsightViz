from datetime import datetime
from flask import Blueprint, request, jsonify, abort
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.Base_de_donne import User, Enquete, QuestionEnquete, ReponseEnquete, Campagne, RoleEnum
import time

main = Blueprint("main", __name__)

# =========================================================
# 0. PAGE D'ACCUEIL
# =========================================================
@main.route("/")
def index():
    return "Bienvenue sur le serveur Flask !"

# =========================================================
# 1. AUTHENTIFICATION / UTILISATEURS
# =========================================================

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Valider les champs
    if not full_name or not email or not password or role not in RoleEnum._value2member_map_:
        return jsonify({'error': 'Champs invalides'}), 400

    # Créer l'utilisateur
    new_user = User(
        full_name=full_name,
        email=email,
        role=RoleEnum(role)
    )
    new_user.password = password  # hash automatique

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email déjà utilisé'}), 409

    # Redirection selon rôle
    if role == 'admin' or role == 'superadmin':
        redirect = '/admin'
    else:
        redirect = '/dashboard'

    return jsonify({'message': 'Utilisateur créé avec succès', 'redirect': redirect}), 201

@main.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return "", 200

    start = time.time()

    data = request.get_json()
    email    = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Champs requis manquants"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        print(f"[LOGIN] Temps de traitement : {time.time() - start:.2f} sec (ECHEC)")
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401

    print(f"[LOGIN] Temps de traitement : {time.time() - start:.2f} sec (SUCCÈS)")

    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role.value if hasattr(user.role, "value") else user.role,
        },
        "redirect": "/admin" if user.role == RoleEnum.ADMIN else "/dashboard"
    }), 200


# ----------- CRUD utilisateurs simplifiés avec pagination ----------------
@main.route("/utilisateurs", methods=["GET", "OPTIONS"])
def get_utilisateurs():
    if request.method == "OPTIONS":
        return "", 200

    # Pagination (exemple simple)
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("limit", 10))
    except ValueError:
        page = 1
        per_page = 10

    query = User.query.order_by(User.created_at.desc())
    users_paginated = query.limit(per_page).offset((page - 1) * per_page).all()

    total = query.count()

    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "utilisateurs": [
            {
                "id": u.id,
                "nom": u.full_name,
                "email": u.email,
                "date_inscription": u.created_at.strftime("%Y-%m-%d") if u.created_at else "",
            }
            for u in users_paginated
        ]
    }), 200


@main.route("/utilisateurs", methods=["POST"])
def create_utilisateur():
    data = request.get_json()
    nom         = data.get("nom")
    email       = data.get("email")
    motdepasse  = data.get("motdepasse")
    role        = data.get("role", "user")

    if not all([nom, email, motdepasse, role]):
        return jsonify({"error": "Tous les champs sont requis"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email déjà utilisé"}), 409

    new_user = User(
        full_name=nom,
        email=email,
        role=RoleEnum(role) if role in RoleEnum._value2member_map_ else RoleEnum.USER,
        created_at=datetime.utcnow(),
    )
    new_user.password = motdepasse
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utilisateur créé avec succès"}), 201


# =========================================================
# 2. CAMPAGNES (liste pour le <select>)
# =========================================================
@main.route("/campagnes", methods=["GET"])
def list_campagnes():
    campagnes = Campagne.query.order_by(Campagne.nom).all()
    return jsonify([
        {
            "id": c.id,
            "nom": c.nom,
            "description": c.description,
            "groupe_cible": c.groupe_cible,
            "date_debut": c.date_debut.isoformat() if c.date_debut else None,
            "date_fin": c.date_fin.isoformat() if c.date_fin else None,
            "statut": c.statut
        }
        for c in campagnes
    ]), 200

# ➕ Créer une campagne
@main.route("/campagnes", methods=["POST"])
def create_campagne():
    data = request.get_json()

    campagne = Campagne(
        nom=data.get("nom"),
        description=data.get("description"),
        groupe_cible=data.get("groupe_cible"),
        date_debut=data.get("date_debut"),
        date_fin=data.get("date_fin"),
        statut=data.get("statut", "active")
    )

    db.session.add(campagne)
    db.session.commit()

    return jsonify({"message": "Campagne créée", "id": campagne.id}), 201

# 🟡 Obtenir une campagne spécifique (édition)
@main.route("/campagnes/<int:id>", methods=["GET"])
def get_campagne(id):
    campagne = Campagne.query.get_or_404(id)
    return jsonify({
        "id": campagne.id,
        "nom": campagne.nom,
        "description": campagne.description,
        "groupe_cible": campagne.groupe_cible,
        "date_debut": campagne.date_debut.isoformat() if campagne.date_debut else None,
        "date_fin": campagne.date_fin.isoformat() if campagne.date_fin else None,
        "statut": campagne.statut
    })

# 📝 Modifier une campagne
@main.route("/campagnes/<int:id>", methods=["PUT"])
def update_campagne(id):
    data = request.get_json()
    campagne = Campagne.query.get_or_404(id)

    campagne.nom = data.get("nom", campagne.nom)
    campagne.description = data.get("description", campagne.description)
    campagne.groupe_cible = data.get("groupe_cible", campagne.groupe_cible)
    campagne.date_debut = data.get("date_debut", campagne.date_debut)
    campagne.date_fin = data.get("date_fin", campagne.date_fin)
    campagne.statut = data.get("statut", campagne.statut)

    db.session.commit()
    return jsonify({"message": "Campagne mise à jour"}), 200
# ❌ Supprimer une campagne
@main.route('/campagnes/<int:id>', methods=['DELETE'])
def delete_campagne(id):
    campagne = Campagne.query.get(id)
    if not campagne:
        return jsonify({"message": "Campagne non trouvée"}), 404

    try:
        db.session.delete(campagne)
        db.session.commit()
        return jsonify({"message": "Campagne supprimée avec succès ✅"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erreur serveur ❌", "error": str(e)}), 500

# =========================================================
# 3. ENQUÊTES (dashboard + création)
# =========================================================
@main.route("/enquetes", methods=["GET"])
def list_enquetes():
    rows = (
        db.session.query(
            Enquete.id,
            Enquete.titre,
            Enquete.date_creation,
            func.count(ReponseEnquete.id).label("nb_rep"),
        )
        .outerjoin(ReponseEnquete)
        .group_by(Enquete.id)
        .order_by(Enquete.date_creation.desc())
        .all()
    )
    return jsonify([
        {
            "id": r.id,
            "titre": r.titre,
            "date_creation": r.date_creation.isoformat() if r.date_creation else None,
            "answered": r.nb_rep > 0,
        }
        for r in rows
    ]), 200


@main.route("/enquetes", methods=["POST"])
def create_enquete():
    data  = request.get_json(force=True) or {}
    titre = (data.get("titre") or "").strip()
    campagne_id = data.get("campagne_id")

    if not titre:
        abort(400, "Le champ 'titre' est obligatoire")

    
    if not campagne_id or not Campagne.query.get(campagne_id):
        abort(400, "Campagne invalide ou manquante")

    enquete = Enquete(
        titre=titre,
        campagne_id=campagne_id,
        date_creation=datetime.utcnow()
    )
    db.session.add(enquete)
    db.session.flush()  
    lignes = [
        l.strip() for l in (data.get("description") or "").splitlines() if l.strip()
    ]
    for ordre, texte in enumerate(lignes, start=1):
        if ":" in texte and texte.split(":", 1)[0].upper().startswith("Q"):
            texte = texte.split(":", 1)[1].strip()
        db.session.add(
            QuestionEnquete(texte=texte, ordre=ordre, enquete_id=enquete.id)
        )

    db.session.commit()
    return jsonify({"id": enquete.id}), 201


@main.route("/enquetes/<int:enq_id>", methods=["GET"])
def get_enquete(enq_id):
    e = Enquete.query.get_or_404(enq_id)
    return jsonify({
        "id": e.id,
        "titre": e.titre,
        "campagne_id": e.campagne_id
    }), 200
@main.route("/enquetes/<int:enq_id>", methods=["PUT"])
def update_enquete(enq_id):
    e = Enquete.query.get_or_404(enq_id)
    data = request.get_json(force=True) or {}

    titre = (data.get("titre") or "").strip()
    campagne_id = data.get("campagne_id")

    if not titre:
        abort(400, "Le champ titre est obligatoire.")
    if not campagne_id or not Campagne.query.get(campagne_id):
        abort(400, "Campagne invalide.")
    e.titre = titre
    e.campagne_id = campagne_id
    e.questions.clear()
    for ordre, texte in enumerate(
        (l.strip() for l in data.get("description", "").splitlines() if l.strip()),
        start=1
    ):
        if ":" in texte and texte.upper().startswith("Q"):
            texte = texte.split(":", 1)[1].strip()
        e.questions.append(QuestionEnquete(ordre=ordre, texte=texte))

    db.session.commit()
    return jsonify({"msg": "OK"}), 200

