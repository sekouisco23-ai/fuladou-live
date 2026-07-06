%%writefile app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests as req
import os
from urllib.parse import quote

app = Flask(__name__)
CORS(app)

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
EMAIL_ARTISTE = os.environ.get("EMAIL_ARTISTE")
BASE_URL      = "https://fuladou-live.onrender.com"
LOVABLE_URL   = os.environ.get("LOVABLE_URL")

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
    data = request.get_json()

    reservation_id = data.get("id")
    nom_client     = data.get("nom_client", "")
    email_client   = data.get("email_client", "")
    telephone      = data.get("telephone_client", "")
    date_ev        = data.get("date_evenement", "")
    lieu_ev        = data.get("lieu", "")
    type_ev        = data.get("type_evenement", "")

    # Construire les liens avec toutes les infos dans l'URL
    params = (
        f"?nom={quote(nom_client)}"
        f"&email={quote(email_client)}"
        f"&tel={quote(telephone)}"
        f"&date={quote(date_ev)}"
        f"&lieu={quote(lieu_ev)}"
        f"&type={quote(type_ev)}"
    )
    lien_confirmer = f"{BASE_URL}/confirmer/{reservation_id}{params}"
    lien_refuser   = f"{BASE_URL}/refuser/{reservation_id}{params}"

    contenu_html = (
        "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;"
        "border:2px solid #D4A017;border-radius:12px;overflow:hidden;'>"
        "<div style='background:#3B1F6A;padding:24px;text-align:center;'>"
        "<h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1>"
        "<p style='color:white;'>Nouvelle demande de reservation</p></div>"
        "<div style='padding:28px;background:#F8F5FF;'>"
        "<p>Bonjour <strong>King Dou</strong>,</p>"
        "<p>Vous avez recu une nouvelle demande :</p>"
        "<table style='width:100%;border-collapse:collapse;margin:20px 0;'>"
        "<tr style='background:#3B1F6A;'>"
        "<td colspan='2' style='padding:10px;color:#D4A017;font-weight:bold;'>Details</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Client</td>"
        f"<td style='padding:10px;font-weight:bold;'>{nom_client}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Email</td>"
        f"<td style='padding:10px;font-weight:bold;'>{email_client}</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Telephone</td>"
        f"<td style='padding:10px;font-weight:bold;'>{telephone}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Date</td>"
        f"<td style='padding:10px;font-weight:bold;'>{date_ev}</td></tr>"
        f"<tr><td style='padding:10px;color:#666;'>Lieu</td>"
        f"<td style='padding:10px;font-weight:bold;'>{lieu_ev}</td></tr>"
        f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Type</td>"
        f"<td style='padding:10px;font-weight:bold;'>{type_ev}</td></tr>"
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
        "<p style='color:#888;font-size:13px;'>Confirmation apres reception de l avance.</p>"
        "</div>"
        "<div style='background:#3B1F6A;padding:16px;text-align:center;'>"
        "<p style='color:#D4A017;margin:0;'>Fuladou Live - Kolda, Senegal</p>"
        "</div></div>"
    )

    response = envoyer_email(
        EMAIL_ARTISTE, "King Dou",
        f"Nouvelle reservation #{reservation_id} - {type_ev}",
        contenu_html
    )

    if response.status_code == 201:
        return jsonify({"success": True, "message": "Email envoye a King Dou"})
    return jsonify({"success": False, "error": response.text}), 400

@app.route("/confirmer/<reservation_id>", methods=["GET"])
def confirmer_reservation(reservation_id):
    nom_client   = request.args.get("nom", "Client")
    email_client = request.args.get("email", "")
    date_ev      = request.args.get("date", "")
    lieu_ev      = request.args.get("lieu", "")
    type_ev      = request.args.get("type", "")

    # Email au client
    if email_client:
        contenu_html = (
            "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;"
            "border:2px solid #D4A017;border-radius:12px;overflow:hidden;'>"
            "<div style='background:#3B1F6A;padding:24px;text-align:center;'>"
            "<h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1>"
            "<p style='color:white;'>Reservation confirmee</p></div>"
            "<div style='padding:28px;background:#F8F5FF;text-align:center;'>"
            "<div style='font-size:60px;margin:16px 0;'>✅</div>"
            f"<h2 style='color:#3B1F6A;'>Bonjour {nom_client},</h2>"
            "<p>Votre reservation a ete <strong>confirmee</strong> par King Dou.</p>"
            "<table style='width:100%;border-collapse:collapse;margin:20px 0;text-align:left;'>"
            f"<tr><td style='padding:10px;color:#666;'>Date</td>"
            f"<td style='padding:10px;font-weight:bold;'>{date_ev}</td></tr>"
            f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Lieu</td>"
            f"<td style='padding:10px;font-weight:bold;'>{lieu_ev}</td></tr>"
            f"<tr><td style='padding:10px;color:#666;'>Type</td>"
            f"<td style='padding:10px;font-weight:bold;'>{type_ev}</td></tr>"
            f"<tr style='background:#F8F5FF;'><td style='padding:10px;color:#666;'>Reference</td>"
            f"<td style='padding:10px;font-weight:bold;'>#{reservation_id}</td></tr>"
            "</table>"
            "<p style='color:#888;'>King Dou vous contactera pour finaliser les details.</p>"
            "</div>"
            "<div style='background:#3B1F6A;padding:16px;text-align:center;'>"
            "<p style='color:#D4A017;margin:0;'>Fuladou Live - Kolda, Senegal</p>"
            "</div></div>"
        )
        envoyer_email(
            email_client, nom_client,
            f"Reservation #{reservation_id} confirmee - Fuladou Live",
            contenu_html
        )

    # Page HTML pour King Dou
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Confirmation - Fuladou Live</title>"
        "<style>body{font-family:Arial,sans-serif;background:#F8F5FF;"
        "display:flex;justify-content:center;align-items:center;"
        "min-height:100vh;margin:0;}"
        ".card{background:white;border-radius:16px;padding:40px;"
        "max-width:450px;width:90%;text-align:center;"
        "border:2px solid #D4A017;box-shadow:0 4px 20px rgba(0,0,0,0.1);}"
        ".header{background:#3B1F6A;color:#D4A017;padding:20px;"
        "border-radius:12px;margin-bottom:24px;}"
        ".icon{font-size:70px;margin:16px 0;}"
        "h2{color:#3B1F6A;}"
        "p{color:#555;line-height:1.6;}"
        ".ref{background:#F8F5FF;padding:12px;border-radius:8px;"
        "color:#3B1F6A;font-weight:bold;margin:16px 0;display:inline-block;}"
        "</style></head><body>"
        "<div class='card'>"
        "<div class='header'><h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1></div>"
        "<div class='icon'>✅</div>"
        f"<h2>Reservation confirmee !</h2>"
        f"<p>La reservation de <strong>{nom_client}</strong> a ete confirmee.</p>"
        f"<p>Un email de confirmation a ete envoye au client.</p>"
        f"<div class='ref'>Reference : #{reservation_id}</div>"
        "<p style='color:#D4A017;font-weight:bold;margin-top:24px;'>Fuladou Live</p>"
        "</div></body></html>"
    )

@app.route("/refuser/<reservation_id>", methods=["GET"])
def refuser_reservation(reservation_id):
    nom_client   = request.args.get("nom", "Client")
    email_client = request.args.get("email", "")
    date_ev      = request.args.get("date", "")
    lieu_ev      = request.args.get("lieu", "")
    type_ev      = request.args.get("type", "")

    # Email au client
    if email_client:
        contenu_html = (
            "<div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;"
            "border:2px solid #DC2626;border-radius:12px;overflow:hidden;'>"
            "<div style='background:#3B1F6A;padding:24px;text-align:center;'>"
            "<h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1>"
            "<p style='color:white;'>Reservation refusee</p></div>"
            "<div style='padding:28px;background:#F8F5FF;text-align:center;'>"
            "<div style='font-size:60px;margin:16px 0;'>❌</div>"
            f"<h2 style='color:#DC2626;'>Bonjour {nom_client},</h2>"
            "<p>Nous sommes desoles, King Dou est "
            f"<strong>INDISPONIBLE</strong> pour le {date_ev}.</p>"
            f"<p>Reference : <strong>#{reservation_id}</strong></p>"
            "<p style='color:#888;'>Vous pouvez faire une nouvelle reservation "
            "pour une autre date.</p>"
            f"<a href='{LOVABLE_URL}' style='display:inline-block;background:#3B1F6A;"
            "color:#D4A017;padding:12px 24px;border-radius:8px;"
            "text-decoration:none;font-weight:bold;margin-top:16px;'>"
            "Faire une nouvelle reservation</a>"
            "</div>"
            "<div style='background:#3B1F6A;padding:16px;text-align:center;'>"
            "<p style='color:#D4A017;margin:0;'>Fuladou Live - Kolda, Senegal</p>"
            "</div></div>"
        )
        envoyer_email(
            email_client, nom_client,
            f"Reservation #{reservation_id} - INDISPONIBLE - Fuladou Live",
            contenu_html
        )

    # Page HTML pour King Dou
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Refus - Fuladou Live</title>"
        "<style>body{font-family:Arial,sans-serif;background:#F8F5FF;"
        "display:flex;justify-content:center;align-items:center;"
        "min-height:100vh;margin:0;}"
        ".card{background:white;border-radius:16px;padding:40px;"
        "max-width:450px;width:90%;text-align:center;"
        "border:2px solid #DC2626;box-shadow:0 4px 20px rgba(0,0,0,0.1);}"
        ".header{background:#3B1F6A;color:#D4A017;padding:20px;"
        "border-radius:12px;margin-bottom:24px;}"
        ".icon{font-size:70px;margin:16px 0;}"
        "h2{color:#DC2626;}"
        "p{color:#555;line-height:1.6;}"
        ".ref{background:#FEE2E2;padding:12px;border-radius:8px;"
        "color:#DC2626;font-weight:bold;margin:16px 0;display:inline-block;}"
        "</style></head><body>"
        "<div class='card'>"
        "<div class='header'><h1 style='color:#D4A017;margin:0;'>Fuladou Live</h1></div>"
        "<div class='icon'>❌</div>"
        f"<h2>INDISPONIBLE</h2>"
        f"<p>La demande de <strong>{nom_client}</strong> a ete refusee.</p>"
        f"<p>Un email a ete envoye au client pour l informer.</p>"
        f"<div class='ref'>Reference : #{reservation_id}</div>"
        "<p style='color:#D4A017;font-weight:bold;margin-top:24px;'>Fuladou Live</p>"
        "</div></body></html>"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
