from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.models.user import User  # Assure-toi que le modèle est bien importé

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    start = request.args.get('start')
    end = request.args.get('end')

    # Parsing dates si fournis
    try:
        start_date = datetime.strptime(start, '%Y-%m-%d') if start else None
        end_date = datetime.strptime(end, '%Y-%m-%d') if end else None
    except ValueError:
        return jsonify({"error": "Format de date invalide"}), 400

    # Remplacer par des vrais modèles plus tard
    stats = {
        "enquêtes": 15,
        "campagnes": 4,
        "réponses": 84,
        "objections": 7
    }

    return jsonify(stats)


@dashboard_bp.route('/api/utilisateurs', methods=['GET'])
def get_utilisateurs():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "nom": u.full_name if hasattr(u, 'full_name') else "N/A",
            "email": u.email,
            "date_inscription": u.terms_agreed_at.strftime('%Y-%m-%d') if u.terms_agreed_at else ""
        })
    return jsonify(result)
