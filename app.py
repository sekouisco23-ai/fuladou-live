
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests as req
import os

app = Flask(__name__)
CORS(app)

# Configuration depuis variables d'environnement
BREVO_API_KEY  = os.environ.get("BREVO_API_KEY")
EMAIL_ARTISTE  = os.environ.get("EMAIL_ARTISTE")
BASE_URL       = os.environ.get("BASE_URL")
LOVABLE_URL    = os.environ.get("LOVABLE_URL")

@app.after_request
def add_headers(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def envoyer_email(destinataire_email, destinataire_nom, sujet, contenu_html):
    payload = {
        "sender":      {"name": "Fuladou Live", "email": EMAIL_ARTISTE},
        "to":          [{"email": destinataire_email, "name": destinataire_nom}],
        "subject":     sujet,
        "htmlContent": contenu_html
    }
    headers = {
        "accept":       "application/json",
        "content-type": "application/json",
        "api-key":      BREVO_API_KEY
    }
    return req.post("https://api.brevo.com/v3/smtp/email",
                    json=payload, headers=headers)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Fuladou Live API operationnelle"})

@app.route("/notifier-artiste", methods=["POST"])
def notifier_artiste():
    data           = request.get_json()
    reservation_id = data.get("id")
    lien_confirmer = f"{BASE_URL}/confirmer/{reservation_id}"
    lien_refuser   = f"{BASE_URL}/refuser/{reservation_id}"

    contenu_html = (
        "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;"
        "border:2px solid #D4A017;border-radius:12px;overflow:hidden;'>"
        "<div style='background:#3B1F6A;padding:24px;text-align:center;'>"
        "<h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1>"
        "<p style='color:white;'>Nouvelle demande de reservation</p></div>"
        "<div style='padding:28px;background:#F8F5FF;'>"
        f"<p>Bonjour <strong>King Dou</strong>,</p>"
        "<p>Vous avez recu une nouvelle demande :</p>"
        "<table style='width:100%;border-collapse:collapse;margin:20px 0;'>"
        "<tr style='background:#3B1F6A;'><td colspan='2' style='padding:10px;"
        "color:#D4A017;font-weight:bold;'>Details</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Client</td>"
        f"<td style='padding:10px;font-weight:bold;'>{data.get('nom_client')}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Telephone</td>"
        f"<td style='padding:10px;font-weight:bold;'>{data.get('telephone_client')}</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Email</td>"
        f"<td style='padding:10px;font-weight:bold;'>{data.get('email_client', 'Non renseigne')}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Date</td>"
        f"<td style='padding:10px;font-weight:bold;'>{data.get('date_evenement')}</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Lieu</td>"
        f"<td style='padding:10px;font-weight:bold;'>{data.get('lieu')}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Type</td>"
        f"<td style='padding:10px;font-weight:bold;'>{data.get('type_evenement')}</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Reference</td>"
        f"<td style='padding:10px;font-weight:bold;'>#{reservation_id}</td></tr>"
        "</table>"
        "<div style='text-align:center;margin:28px 0;'>"
        f"<a href='{lien_confirmer}' style='background:#D4A017;color:#3B1F6A;"
        "padding:14px 32px;border-radius:8px;text-decoration:none;"
        "font-weight:bold;font-size:16px;margin-right:16px;'>Confirmer</a>"
        f"<a href='{lien_refuser}' style='background:white;color:#DC2626;"
        "padding:14px 32px;border-radius:8px;text-decoration:none;"
        "font-weight:bold;font-size:16px;border:2px solid #DC2626;'>Refuser</a>"
        "</div>"
        "<p style='color:#888;font-size:13px;'>"
        "Confirmation apres reception de l avance.</p>"
        "</div>"
        "<div style='background:#3B1F6A;padding:16px;text-align:center;'>"
        "<p style='color:#D4A017;margin:0;'>Fuladou Live - Kolda, Senegal</p>"
        "</div></div>"
    )

    response = envoyer_email(
        EMAIL_ARTISTE, "King Dou",
        f"Nouvelle reservation #{reservation_id} - {data.get('type_evenement')}",
        contenu_html
    )

    if response.status_code == 201:
        return jsonify({"success": True, "message": "Email envoye a King Dou"})
    return jsonify({"success": False, "error": response.text}), 400

@app.route("/confirmer/<reservation_id>", methods=["GET"])
def confirmer_reservation(reservation_id):
    email_client = request.args.get("email", "")
    nom_client   = request.args.get("nom", "Client")
    date_ev      = request.args.get("date", "")
    lieu_ev      = request.args.get("lieu", "")
    type_ev      = request.args.get("type", "")

    contenu_html = (
        "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;"
        "border:2px solid #D4A017;border-radius:12px;overflow:hidden;'>"
        "<div style='background:#3B1F6A;padding:24px;text-align:center;'>"
        "<h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1>"
        "<p style='color:white;'>Reservation confirmee</p></div>"
        "<div style='padding:28px;background:#F8F5FF;text-align:center;'>"
        "<div style='font-size:60px;'>✅</div>"
        f"<h2 style='color:#3B1F6A;'>Bonjour {nom_client},</h2>"
        "<p>Votre reservation a ete <strong>confirmee</strong> par King Dou.</p>"
        "<table style='width:100%;border-collapse:collapse;margin:20px 0;'>"
        f"<tr><td style='padding:10px;color:#666;'>Date</td>"
        f"<td style='padding:10px;font-weight:bold;'>{date_ev}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Lieu</td>"
        f"<td style='padding:10px;font-weight:bold;'>{lieu_ev}</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Type</td>"
        f"<td style='padding:10px;font-weight:bold;'>{type_ev}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Reference</td>"
        f"<td style='padding:10px;font-weight:bold;'>#{reservation_id}</td></tr>"
        "</table>"
        "<p style='color:#888;'>King Dou vous contactera pour les details du paiement.</p>"
        "</div>"
        "<div style='background:#3B1F6A;padding:16px;text-align:center;'>"
        "<p style='color:#D4A017;margin:0;'>Fuladou Live - Kolda, Senegal</p>"
        "</div></div>"
    )

    if email_client:
        envoyer_email(
            email_client, nom_client,
            f"Reservation #{reservation_id} confirmee - Fuladou Live",
            contenu_html
        )

    return (
        "<html><body style='font-family:Arial;background:#F8F5FF;"
        "display:flex;justify-content:center;align-items:center;height:100vh;margin:0;'>"
        "<div style='background:white;padding:40px;border-radius:16px;"
        "border:2px solid #D4A017;text-align:center;max-width:400px;'>"
        "<div style='font-size:60px;'>✅</div>"
        f"<h2 style='color:#3B1F6A;'>Reservation #{reservation_id} confirmee !</h2>"
        "<p style='color:#555;'>Le client a ete notifie par email.</p>"
        "<p style='color:#D4A017;font-weight:bold;'>Fuladou Live</p>"
        "</div></body></html>"
    )

@app.route("/refuser/<reservation_id>", methods=["GET"])
def refuser_reservation(reservation_id):
    email_client = request.args.get("email", "")
    nom_client   = request.args.get("nom", "Client")
    date_ev      = request.args.get("date", "")

    contenu_html = (
        "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;"
        "border:2px solid #DC2626;border-radius:12px;overflow:hidden;'>"
        "<div style='background:#3B1F6A;padding:24px;text-align:center;'>"
        "<h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1>"
        "<p style='color:white;'>Reservation refusee</p></div>"
        "<div style='padding:28px;background:#F8F5FF;text-align:center;'>"
        "<div style='font-size:60px;'>❌</div>"
        f"<h2 style='color:#DC2626;'>Bonjour {nom_client},</h2>"
        "<p>Nous sommes desoles, King Dou est "
        f"<strong>INDISPONIBLE</strong> pour le {date_ev}.</p>"
        f"<p>Reference : <strong>#{reservation_id}</strong></p>"
        "<p style='color:#888;'>Vous pouvez faire une nouvelle reservation "
        f"pour une autre date sur notre plateforme.</p>"
        f"<a href='{LOVABLE_URL}' style='display:inline-block;background:#3B1F6A;"
        "color:#D4A017;padding:12px 24px;border-radius:8px;"
        "text-decoration:none;font-weight:bold;margin-top:16px;'>"
        "Faire une nouvelle reservation</a>"
        "</div>"
        "<div style='background:#3B1F6A;padding:16px;text-align:center;'>"
        "<p style='color:#D4A017;margin:0;'>Fuladou Live - Kolda, Senegal</p>"
        "</div></div>"
    )

    if email_client:
        envoyer_email(
            email_client, nom_client,
            f"Reservation #{reservation_id} - INDISPONIBLE - Fuladou Live",
            contenu_html
        )

    return (
        "<html><body style='font-family:Arial;background:#F8F5FF;"
        "display:flex;justify-content:center;align-items:center;height:100vh;margin:0;'>"
        "<div style='background:white;padding:40px;border-radius:16px;"
        "border:2px solid #DC2626;text-align:center;max-width:400px;'>"
        "<div style='font-size:60px;'>❌</div>"
        f"<h2 style='color:#DC2626;'>Reservation #{reservation_id} refusee</h2>"
        "<p style='color:#555;'>Le client a ete notifie par email.</p>"
        "<p style='color:#D4A017;font-weight:bold;'>Fuladou Live</p>"
        "</div></body></html>"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
