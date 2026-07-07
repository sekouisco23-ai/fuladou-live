import os
from flask import Flask, request, jsonify
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

app = Flask(__name__)

# ===========================================================================
# ⚙️ CONFIGURATION STRICTE DE VOTRE PLATEFORME
# ===========================================================================
# L'adresse officielle de votre site sur Render (SANS le slash / à la fin)
BASE_URL = "https://onrender.com"

# Votre clé API Brevo (à remplacer par votre vraie clé si nécessaire)
BREVO_API_KEY = "VOTRE_CLE_API_BREVO_ICI"  

# L'adresse de l'Artiste/Patron qui doit recevoir les demandes (et qui sert d'expéditeur)
EMAIL_ARTISTE_PATRON = "kingdou2004@gmail.com"  

# Configuration de l'API Brevo
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# Fonction universelle pour envoyer un e-mail via Brevo
def envoyer_email(destinataire, sujet, contenu_html):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": destinataire}],
        sender={"name": "Fuladou Live Assistant", "email": EMAIL_ARTISTE_PATRON},
        subject=sujet,
        html_content=contenu_html
    )
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        print(f"Erreur Brevo : {e}")
        return False

# ===========================================================================
# 🤖 ROUTE 1 : Appelée par l'IA (Envoi du mail avec boutons à l'Artiste)
# ===========================================================================
@app.route('/notifier-artiste', methods=['POST'])
def notifier_artiste():
    donnees = request.json
    id_reservation = donnees.get('id', 'TEST_ID')
    nom_client = donnees.get('nom_client', 'Client')
    email_client = donnees.get('email_client')
    details = donnees.get('details', donnees.get('type_evenement', 'Prestation'))
    
    sujet = f"🔔 Nouvelle demande de réservation de {nom_client}"
    
    # Liens parfaits utilisant l'adresse de votre serveur Render et l'adresse du client masquée
    url_confirmer = f"{BASE_URL}/confirmer/{id_reservation}?client={email_client}"
    url_refuser = f"{BASE_URL}/refuser/{id_reservation}?client={email_client}"
    
    html_contenu = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #eee; max-width: 600px;">
        <h2>Bonjour ! Une nouvelle demande est en attente :</h2>
        <p><b>Client :</b> {nom_client}</p>
        <p><b>Détails :</b> {details}</p>
        <br>
        <p><b>Acceptez-vous cette réservation ?</b></p>
        <div style="margin-top: 20px;">
            <a href="{url_confirmer}" style="background-color: #2ecc71; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-right: 15px; display: inline-block;">✅ Confirmer</a>
            <a href="{url_refuser}" style="background-color: #e74c3c; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">❌ Refuser</a>
        </div>
    </div>
    """
    
    if envoyer_email(EMAIL_ARTISTE_PATRON, sujet, html_contenu):
        return jsonify({"status": "success", "message": "Demande envoyée à l'artiste."}), 200
    return jsonify({"status": "error", "message": "Échec de l'envoi de l'email."}), 500

# ===========================================================================
# ⚡ ROUTES DE DÉCISION (Retourne juste du texte brut et notifie le client)
# ===========================================================================

@app.route('/confirmer/<id_reservation>', methods=['GET'])
def confirmer_reservation(id_reservation):
    email_client = request.args.get('client')
    
    if email_client:
        sujet_client = "🎉 Votre réservation a été acceptée !"
        html_client = "<h3>Bonjour,</h3><p>Bonne nouvelle ! L'artiste a validé votre demande de réservation.</p>"
        envoyer_email(email_client, sujet_client, html_client)
        
    return "Confirmé", 200

@app.route('/refuser/<id_reservation>', methods=['GET'])
def refuser_reservation(id_reservation):
    email_client = request.args.get('client')
    
    if email_client:
        sujet_client = "Mise à jour concernant votre réservation"
        html_client = "<h3>Bonjour,</h3><p>L'artiste n'est malheureusement pas disponible pour cette date.</p>"
        envoyer_email(email_client, sujet_client, html_client)
        
    return "Refusé", 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Fuladou Live API operationnelle"}), 200

if __name__ == '__main__':
    # Render utilise la variable d'environnement PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
