from datetime import datetime
from flask import Blueprint, request, jsonify, abort
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.Base_de_donne import User, Enquete, QuestionEnquete, ReponseEnquete, Campagne, RoleEnum, Personne, TypePersonneEnum
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
@main.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([
        {
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at.strftime("%Y-%m-%d")
        }
        for u in users
    ]), 200

# ➕ POST - Créer un nouvel utilisateur
@main.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not all(k in data for k in ("full_name", "email", "password", "role")):
        return jsonify({"error": "Champs manquants"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email déjà utilisé"}), 409

    try:
        user = User(
            full_name=data["full_name"],
            email=data["email"],
            role=data["role"]
        )
        user.password = data["password"]  # setter hash automatiquement
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Utilisateur créé", "id": user.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erreur lors de la création"}), 500

# ✏️ PUT - Modifier un utilisateur
@main.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.full_name = data.get("full_name", user.full_name)
    user.email = data.get("email", user.email)
    user.role = data.get("role", user.role)

    try:
        db.session.commit()
        return jsonify({"message": "Utilisateur mis à jour"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erreur lors de la mise à jour"}), 500

# ❌ DELETE - Supprimer un utilisateur
@main.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Utilisateur supprimé"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erreur lors de la suppression"}), 500
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
    data = request.get_json(force=True) or {}
    titre = (data.get("titre") or "").strip()
    campagne_id = data.get("campagne_id")
    questions_data = data.get("questions", [])

    if not titre:
        abort(400, "Le champ 'titre' est obligatoire")
    if not campagne_id or not Campagne.query.get(campagne_id):
        abort(400, "Campagne invalide ou manquante")
    if not isinstance(questions_data, list) or not all(isinstance(q, dict) for q in questions_data):
        abort(400, "Format questions invalide")

    enquete = Enquete(
        titre=titre,
        campagne_id=campagne_id,
        date_creation=datetime.utcnow()
    )
    db.session.add(enquete)
    db.session.flush()  # pour avoir enquete.id

    for q in questions_data:
        ordre = q.get("ordre")
        texte = q.get("texte", "").strip()
        if not texte:
            continue
        db.session.add(QuestionEnquete(ordre=ordre, texte=texte, enquete_id=enquete.id))

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
    questions_data = data.get("questions", [])

    if not titre:
        abort(400, "Le champ titre est obligatoire.")
    if not campagne_id or not Campagne.query.get(campagne_id):
        abort(400, "Campagne invalide.")
    if not isinstance(questions_data, list) or not all(isinstance(q, dict) for q in questions_data):
        abort(400, "Format questions invalide")

    e.titre = titre
    e.campagne_id = campagne_id
    e.questions.clear()

    for q in questions_data:
        ordre = q.get("ordre")
        texte = q.get("texte", "").strip()
        if not texte:
            continue
        e.questions.append(QuestionEnquete(ordre=ordre, texte=texte))

    db.session.commit()
    return jsonify({"msg": "OK"}), 200


@main.route("/enquetes/<int:enq_id>/questions", methods=["GET"])
def get_questions(enq_id):
    enquete = Enquete.query.get_or_404(enq_id)
    questions = (
        QuestionEnquete.query
        .filter_by(enquete_id=enq_id)
        .order_by(QuestionEnquete.ordre)
        .all()
    )

    return jsonify([
        {
            "id": q.id,
            "ordre": q.ordre,
            "texte": q.texte
        } for q in questions
    ]), 200
    

@main.route("/api/backoffice/stats", methods=["GET"])
def get_backoffice_stats():
    current_year = datetime.now().year

    # Nombre total
    total_enquetes = Enquete.query.count()
    total_reponses = ReponseEnquete.query.count()
    total_campagnes = Campagne.query.count()
    total_utilisateurs = User.query.count()

    # Enquêtes par mois (nombre d'enquêtes créées par mois cette année)
    monthly_counts = [0] * 12
    results = (
        db.session.query(
            func.extract('month', Enquete.date_creation).label('mois'),
            func.count(Enquete.id)
        )
        .filter(func.extract('year', Enquete.date_creation) == current_year)
        .group_by('mois')
        .all()
    )

    for mois, count in results:
        monthly_counts[int(mois) - 1] = count

    return jsonify({
        "enquetes": total_enquetes,
        "reponses": total_reponses,
        "campagnes": total_campagnes,
        "utilisateurs": total_utilisateurs,
        "months": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Aoû", "Sep", "Oct", "Nov", "Déc"],
        "enquetesMonthly": monthly_counts
    }), 200




# =========================================================
# 4. PERSONNES (CRUD)
# =========================================================

# 🔍 Lister les personnes (GET)
@main.route("/personnes", methods=["GET"])
def list_personnes():
    personnes = Personne.query.order_by(Personne.created_at.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "nom": p.nom,
            "region": p.region,
            "email_contact": p.email_contact,
            "telephone": p.telephone,
            "type": p.type.value if p.type else None,
            "taille_entreprise": p.taille_entreprise,
            "secteur_activite": p.secteur_activite,
            "created_at": p.created_at.isoformat()
        }
        for p in personnes
    ]), 200


# ➕ Créer une personne (POST)
@main.route("/personnes", methods=["POST"])
def create_personne():
    data = request.get_json()
    required = ["nom", "type"]

    if not all(data.get(f) for f in required):
        return jsonify({"error": "Champs requis manquants"}), 400

    try:
        type_enum = TypePersonneEnum(data.get("type"))
    except ValueError:
        return jsonify({"error": "Type invalide"}), 400

    personne = Personne(
        nom=data.get("nom"),
        region=data.get("region"),
        email_contact=data.get("email_contact"),
        telephone=data.get("telephone"),
        type=type_enum,
        taille_entreprise=data.get("taille_entreprise") if type_enum == TypePersonneEnum.TRANSPORTEUR else None,
        secteur_activite=data.get("secteur_activite") if type_enum == TypePersonneEnum.EXPEDITEUR else None
    )

    db.session.add(personne)
    db.session.commit()
    return jsonify({"message": "Personne créée avec succès"}), 201


# 📝 Modifier une personne (PUT)
@main.route("/personnes/<int:id>", methods=["PUT"])
def update_personne(id):
    personne = Personne.query.get_or_404(id)
    data = request.get_json()

    if "type" in data:
        try:
            personne.type = TypePersonneEnum(data.get("type"))
        except ValueError:
            return jsonify({"error": "Type invalide"}), 400

    personne.nom = data.get("nom", personne.nom)
    personne.region = data.get("region", personne.region)
    personne.email_contact = data.get("email_contact", personne.email_contact)
    personne.telephone = data.get("telephone", personne.telephone)

    if personne.type == TypePersonneEnum.TRANSPORTEUR:
        personne.taille_entreprise = data.get("taille_entreprise")
        personne.secteur_activite = None
    elif personne.type == TypePersonneEnum.EXPEDITEUR:
        personne.secteur_activite = data.get("secteur_activite")
        personne.taille_entreprise = None

    db.session.commit()
    return jsonify({"message": "Personne mise à jour"}), 200


# ❌ Supprimer une personne (DELETE)
@main.route("/personnes/<int:id>", methods=["DELETE"])
def delete_personne(id):
    personne = Personne.query.get(id)
    if not personne:
        return jsonify({"error": "Personne non trouvée"}), 404

    db.session.delete(personne)
    db.session.commit()
    return jsonify({"message": "Personne supprimée avec succès"}), 200


# === GET: récupérer toutes les réponses ===
@main.route('/reponses-enquetes', methods=['GET'])
def get_reponses_enquetes():
    reponses = ReponseEnquete.query.all()
    result = []
    for r in reponses:
        result.append({
            'id': r.id,
            'enquete_id': r.enquete_id,
            'type_repondant': r.type_repondant,
            'personne_id': r.personne_id,
            'donnees_reponse': r.donnees_reponse,
            'date_reponse': r.date_reponse.isoformat() if r.date_reponse else None
        })
    return jsonify(result), 200

# === POST: créer une réponse ===
@main.route('/reponses-enquetes', methods=['POST'])
def create_reponse_enquete():
    data = request.get_json()
    nouvelle_reponse = ReponseEnquete(
        enquete_id=data.get('enquete_id'),
        type_repondant=data.get('type_repondant'),
        personne_id=data.get('personne_id'),
        donnees_reponse=data.get('donnees_reponse')
    )
    db.session.add(nouvelle_reponse)
    db.session.commit()
    return jsonify({"message": "Réponse enregistrée avec succès."}), 201

# === PUT: modifier une réponse existante ===
@main.route('/reponses-enquetes/<int:id>', methods=['PUT'])
def update_reponse_enquete(id):
    data = request.get_json()
    reponse = ReponseEnquete.query.get_or_404(id)

    reponse.enquete_id = data.get('enquete_id', reponse.enquete_id)
    reponse.type_repondant = data.get('type_repondant', reponse.type_repondant)
    reponse.personne_id = data.get('personne_id', reponse.personne_id)
    reponse.donnees_reponse = data.get('donnees_reponse', reponse.donnees_reponse)

    db.session.commit()
    return jsonify({"message": "Réponse mise à jour avec succès."}), 200

# === DELETE: supprimer une réponse ===
@main.route('/reponses-enquetes/<int:id>', methods=['DELETE'])
def delete_reponse_enquete(id):
    reponse = ReponseEnquete.query.get_or_404(id)
    db.session.delete(reponse)
    db.session.commit()
    return jsonify({"message": "Réponse supprimée avec succès."}), 200