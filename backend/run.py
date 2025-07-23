from app import create_app, db
import logging

app = create_app()

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()           
        print("Démarrage du serveur Flask en cours...")
        app.run(debug=True, host='0.0.0.0', port=5000)
        print("Serveur démarré avec succès sur http://0.0.0.0:5000")
    except Exception as e:
        logging.error("Erreur lors du démarrage du serveur : %s", e)
        print("Le serveur n'a pas pu démarrer. Vérifie ta configuration.")
