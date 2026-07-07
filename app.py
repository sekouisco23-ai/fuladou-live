import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests as req
from urllib.parse import quote

app = Flask(__name__)
CORS(app)

# ===========================================================================
# CONFIGURATION
# ===========================================================================
BASE_URL      = "https://fuladou-live.onrender.com"
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
EMAIL_ARTISTE = os.environ.get("EMAIL_ARTISTE", "kingdou2004@gmail.com")
LOVABLE_URL   = os.environ.get("LOVABLE_URL", "https://fuladou-live-booking.lovable.app")

# ===========================================================================
# FONCTION UNIVERSELLE D'ENVOI EMAIL VIA BREVO
# ===========================================================================
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
    response = req.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers=headers
    )
    return response.status_code == 201

# ===========================================================================
# ROUTE 1 : Notifie l'artiste avec boutons
# ===========================================================================
@app.route('/notifier-artiste', methods=['POST'])
def notifier_artiste():
    data           = request.get_json()
    id_reservation = data.get('id', 'RES000')
    nom_client     = data.get('nom_client', 'Client')
    email_client   = data.get('email_client', '')
    telephone      = data.get('telephone_client', '')
    date_ev        = data.get('date_evenement', '')
    lieu_ev        = data.get('lieu', '')
    type_ev        = data.get('type_evenement', '')
    message_client = data.get('message', '')

    # Liens avec toutes les infos dans l'URL
    params = (
        f"?nom={quote(nom_client)}"
        f"&email={quote(email_client)}"
        f"&tel={quote(telephone)}"
        f"&date={quote(date_ev)}"
        f"&lieu={quote(lieu_ev)}"
        f"&type={quote(type_ev)}"
        f"&message={quote(message_client)}"
    )
    url_confirmer = f"{BASE_URL}/confirmer/{id_reservation}{params}"
    url_refuser   = f"{BASE_URL}/refuser/{id_reservation}{params}"

    # Ligne message optionnelle dans le tableau
    ligne_message = ""
    if message_client:
        ligne_message = f"""
        <tr>
            <td style="padding:10px;color:#666;">💬 Message</td>
            <td style="padding:10px;font-weight:bold;">{message_client}</td>
        </tr>"""

    contenu_html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;
    border:2px solid #D4A017;border-radius:12px;overflow:hidden;">

        <div style="background:#3B1F6A;padding:24px;text-align:center;">
            <h1 style="color:#D4A017;margin:0;">🎵 Fuladou Live</h1>
            <p style="color:white;margin:6px 0 0;">Nouvelle demande de réservation</p>
        </div>

        <div style="padding:28px;background:#F8F5FF;">
            <p>Bonjour <strong>King Dou</strong>,</p>
            <p>Vous avez reçu une nouvelle demande de réservation :</p>

            <table style="width:100%;border-collapse:collapse;margin:20px 0;">
                <tr style="background:#3B1F6A;">
                    <td colspan="2" style="padding:10px;color:#D4A017;font-weight:bold;">
                        Détails de la demande
                    </td>
                </tr>
                <tr>
                    <td style="padding:10px;color:#666;">👤 Client</td>
                    <td style="padding:10px;font-weight:bold;">{nom_client}</td>
                </tr>
                <tr style="background:#F0EBF8;">
                    <td style="padding:10px;color:#666;">📧 Email</td>
                    <td style="padding:10px;font-weight:bold;">{email_client}</td>
                </tr>
                <tr>
                    <td style="padding:10px;color:#666;">📱 Téléphone</td>
                    <td style="padding:10px;font-weight:bold;">{telephone}</td>
                </tr>
                <tr style="background:#F0EBF8;">
                    <td style="padding:10px;color:#666;">📅 Date</td>
                    <td style="padding:10px;font-weight:bold;">{date_ev}</td>
                </tr>
                <tr>
                    <td style="padding:10px;color:#666;">📍 Lieu</td>
                    <td style="padding:10px;font-weight:bold;">{lieu_ev}</td>
                </tr>
                <tr style="background:#F0EBF8;">
                    <td style="padding:10px;color:#666;">🎉 Type</td>
                    <td style="padding:10px;font-weight:bold;">{type_ev}</td>
                </tr>
                {ligne_message}
                <tr style="background:#F0EBF8;">
                    <td style="padding:10px;color:#666;">🔖 Référence</td>
                    <td style="padding:10px;font-weight:bold;">#{id_reservation}</td>
                </tr>
            </table>

            <p><strong>Acceptez-vous cette réservation ?</strong></p>
            <p style="color:#888;font-size:13px;">
                ⚠️ La confirmation est définitive après réception de l'avance.
            </p>

            <div style="text-align:center;margin:28px 0;">
                <a href="{url_confirmer}"
                   style="background:#D4A017;color:#3B1F6A;padding:14px 32px;
                   text-decoration:none;border-radius:8px;font-weight:bold;
                   font-size:16px;margin-right:16px;display:inline-block;">
                   ✅ Confirmer
                </a>
                <a href="{url_refuser}"
                   style="background:white;color:#DC2626;padding:14px 32px;
                   text-decoration:none;border-radius:8px;font-weight:bold;
                   font-size:16px;border:2px solid #DC2626;display:inline-block;">
                   ❌ Refuser
                </a>
            </div>
        </div>

        <div style="background:#3B1F6A;padding:16px;text-align:center;">
            <p style="color:#D4A017;margin:0;">Fuladou Live · Kolda, Sénégal · 2025</p>
        </div>
    </div>
    """

    succes = envoyer_email(
        EMAIL_ARTISTE, "King Dou",
        f"🔔 Nouvelle réservation #{id_reservation} - {type_ev}",
        contenu_html
    )

    if succes:
        return jsonify({"status": "success", "message": "Email envoyé à l'artiste."}), 200
    return jsonify({"status": "error", "message": "Échec de l'envoi."}), 500


# ===========================================================================
# ROUTE 2 : King Dou clique Confirmer
# ===========================================================================
@app.route('/confirmer/<id_reservation>', methods=['GET'])
def confirmer_reservation(id_reservation):
    nom_client     = request.args.get('nom', 'Client')
    email_client   = request.args.get('email', '')
    telephone      = request.args.get('tel', '')
    date_ev        = request.args.get('date', '')
    lieu_ev        = request.args.get('lieu', '')
    type_ev        = request.args.get('type', '')
    message_client = request.args.get('message', '')

    # Ligne message optionnelle
    ligne_message = ""
    if message_client:
        ligne_message = f"""
        <tr style="background:#F0EBF8;">
            <td style="padding:10px;color:#666;">💬 Votre message</td>
            <td style="padding:10px;font-weight:bold;">{message_client}</td>
        </tr>"""

    if email_client:
        contenu_html = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;
        border:2px solid #D4A017;border-radius:12px;overflow:hidden;">

            <div style="background:#3B1F6A;padding:24px;text-align:center;">
                <h1 style="color:#D4A017;margin:0;">🎵 Fuladou Live</h1>
                <p style="color:white;">Réservation confirmée</p>
            </div>

            <div style="padding:28px;background:#F8F5FF;text-align:center;">
                <div style="font-size:60px;margin:16px 0;">✅</div>
                <h2 style="color:#3B1F6A;">Bonjour {nom_client},</h2>
                <p>Bonne nouvelle ! Votre réservation a été
                <strong>confirmée</strong> par King Dou.</p>

                <table style="width:100%;border-collapse:collapse;
                margin:20px 0;text-align:left;">
                    <tr>
                        <td style="padding:10px;color:#666;">📅 Date</td>
                        <td style="padding:10px;font-weight:bold;">{date_ev}</td>
                    </tr>
                    <tr style="background:#F0EBF8;">
                        <td style="padding:10px;color:#666;">📍 Lieu</td>
                        <td style="padding:10px;font-weight:bold;">{lieu_ev}</td>
                    </tr>
                    <tr>
                        <td style="padding:10px;color:#666;">🎉 Type</td>
                        <td style="padding:10px;font-weight:bold;">{type_ev}</td>
                    </tr>
                    <tr style="background:#F0EBF8;">
                        <td style="padding:10px;color:#666;">🔖 Référence</td>
                        <td style="padding:10px;font-weight:bold;">#{id_reservation}</td>
                    </tr>
                    {ligne_message}
                </table>

                <p style="color:#888;">
                    King Dou vous contactera au <strong>{telephone}</strong>
                    pour finaliser les détails et le paiement.
                </p>
            </div>

            <div style="background:#3B1F6A;padding:16px;text-align:center;">
                <p style="color:#D4A017;margin:0;">
                    Fuladou Live · Kolda, Sénégal · 2025
                </p>
            </div>
        </div>
        """
        envoyer_email(
            email_client, nom_client,
            f"🎉 Réservation #{id_reservation} confirmée - Fuladou Live",
            contenu_html
        )

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmé - Fuladou Live</title>
        <style>
            body {{font-family:Arial,sans-serif;background:#F8F5FF;
                  display:flex;justify-content:center;align-items:center;
                  min-height:100vh;margin:0;}}
            .card {{background:white;border-radius:16px;padding:40px;
                   max-width:450px;width:90%;text-align:center;
                   border:2px solid #D4A017;
                   box-shadow:0 4px 20px rgba(0,0,0,0.1);}}
            .header {{background:#3B1F6A;padding:20px;
                     border-radius:12px;margin-bottom:24px;}}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h1 style="color:#D4A017;margin:0;">🎵 Fuladou Live</h1>
            </div>
            <div style="font-size:70px;margin:16px 0;">✅</div>
            <h2 style="color:#3B1F6A;">Réservation confirmée !</h2>
            <p style="color:#555;">
                La réservation de <strong>{nom_client}</strong>
                a été confirmée avec succès.
            </p>
            <p style="color:#555;">
                Un email de confirmation a été envoyé au client.
            </p>
            <p style="background:#F8F5FF;padding:12px;border-radius:8px;
               color:#3B1F6A;font-weight:bold;">
               Référence : #{id_reservation}
            </p>
            <p style="color:#D4A017;font-weight:bold;margin-top:24px;">
                Fuladou Live · Kolda, Sénégal
            </p>
        </div>
    </body>
    </html>
    """, 200


# ===========================================================================
# ROUTE 3 : King Dou clique Refuser
# ===========================================================================
@app.route('/refuser/<id_reservation>', methods=['GET'])
def refuser_reservation(id_reservation):
    nom_client     = request.args.get('nom', 'Client')
    email_client   = request.args.get('email', '')
    date_ev        = request.args.get('date', '')
    lieu_ev        = request.args.get('lieu', '')
    type_ev        = request.args.get('type', '')
    message_client = request.args.get('message', '')

    # Ligne message optionnelle
    ligne_message = ""
    if message_client:
        ligne_message = f"""
        <tr style="background:#F0EBF8;">
            <td style="padding:10px;color:#666;">💬 Votre message</td>
            <td style="padding:10px;font-weight:bold;">{message_client}</td>
        </tr>"""

    if email_client:
        contenu_html = f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;
        border:2px solid #DC2626;border-radius:12px;overflow:hidden;">

            <div style="background:#3B1F6A;padding:24px;text-align:center;">
                <h1 style="color:#D4A017;margin:0;">🎵 Fuladou Live</h1>
                <p style="color:white;">Mise à jour de votre réservation</p>
            </div>

            <div style="padding:28px;background:#F8F5FF;text-align:center;">
                <div style="font-size:60px;margin:16px 0;">❌</div>
                <h2 style="color:#DC2626;">Bonjour {nom_client},</h2>
                <p>Nous sommes désolés, King Dou est
                <strong>INDISPONIBLE</strong> pour le {date_ev}.</p>

                <table style="width:100%;border-collapse:collapse;
                margin:20px 0;text-align:left;">
                    <tr>
                        <td style="padding:10px;color:#666;">📅 Date</td>
                        <td style="padding:10px;font-weight:bold;">{date_ev}</td>
                    </tr>
                    <tr style="background:#F0EBF8;">
                        <td style="padding:10px;color:#666;">📍 Lieu</td>
                        <td style="padding:10px;font-weight:bold;">{lieu_ev}</td>
                    </tr>
                    <tr>
                        <td style="padding:10px;color:#666;">🎉 Type</td>
                        <td style="padding:10px;font-weight:bold;">{type_ev}</td>
                    </tr>
                    <tr style="background:#F0EBF8;">
                        <td style="padding:10px;color:#666;">🔖 Référence</td>
                        <td style="padding:10px;font-weight:bold;">#{id_reservation}</td>
                    </tr>
                    {ligne_message}
                </table>

                <p style="color:#888;">
                    Vous pouvez faire une nouvelle réservation pour une autre date.
                </p>
                <a href="{LOVABLE_URL}"
                   style="display:inline-block;background:#3B1F6A;color:#D4A017;
                   padding:12px 24px;border-radius:8px;text-decoration:none;
                   font-weight:bold;margin-top:16px;">
                   Faire une nouvelle réservation
                </a>
            </div>

            <div style="background:#3B1F6A;padding:16px;text-align:center;">
                <p style="color:#D4A017;margin:0;">
                    Fuladou Live · Kolda, Sénégal · 2025
                </p>
            </div>
        </div>
        """
        envoyer_email(
            email_client, nom_client,
            f"Réservation #{id_reservation} - INDISPONIBLE - Fuladou Live",
            contenu_html
        )

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Refusé - Fuladou Live</title>
        <style>
            body {{font-family:Arial,sans-serif;background:#F8F5FF;
                  display:flex;justify-content:center;align-items:center;
                  min-height:100vh;margin:0;}}
            .card {{background:white;border-radius:16px;padding:40px;
                   max-width:450px;width:90%;text-align:center;
                   border:2px solid #DC2626;
                   box-shadow:0 4px 20px rgba(0,0,0,0.1);}}
            .header {{background:#3B1F6A;padding:20px;
                     border-radius:12px;margin-bottom:24px;}}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h1 style="color:#D4A017;margin:0;">🎵 Fuladou Live</h1>
            </div>
            <div style="font-size:70px;margin:16px 0;">❌</div>
            <h2 style="color:#DC2626;">INDISPONIBLE</h2>
            <p style="color:#555;">
                La demande de <strong>{nom_client}</strong>
                a été refusée.
            </p>
            <p style="color:#555;">
                Un email a été envoyé au client pour l'informer.
            </p>
            <p style="background:#FEE2E2;padding:12px;border-radius:8px;
               color:#DC2626;font-weight:bold;">
               Référence : #{id_reservation}
            </p>
            <p style="color:#D4A017;font-weight:bold;margin-top:24px;">
                Fuladou Live · Kolda, Sénégal
            </p>
        </div>
    </body>
    </html>
    """, 200


# ===========================================================================
# ROUTE SANTE
# ===========================================================================
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Fuladou Live API operationnelle"}), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
