import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def envoyer_notification(df_transforme, df_site, chemin_rapport):

    EMAIL_EXPEDITEUR   = "ton.email@gmail.com"
    MOT_DE_PASSE       = "abcd efgh ijkl mnop"
    EMAIL_DESTINATAIRE = "destinataire@email.com"

    message = MIMEMultipart()
    message["From"]    = EMAIL_EXPEDITEUR
    message["To"]      = EMAIL_DESTINATAIRE
    message["Subject"] = f"📊 Pipeline CDG — {datetime.now().strftime('%B %Y')}"

    corps = f"""
Bonjour,

Le pipeline CDG vient de se terminer avec succès.

📊 Résumé :
- Lignes traitées : {len(df_transforme)}
- Sites analysés : {df_transforme['site'].nunique()}
- CA Réel Total : {df_transforme['ca_reel'].sum()/1000:.0f}k€
- CA Budget Total : {df_transforme['ca_budget'].sum()/1000:.0f}k€
- Écart Total : {df_transforme['ecart_valeur'].sum()/1000:.0f}k€

Le reporting détaillé est en pièce jointe.

Cordialement,
Le système de reporting CDG
"""

    message.attach(MIMEText(corps, "plain"))

    # Pièce jointe
    with open(chemin_rapport, "rb") as fichier:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(fichier.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(chemin_rapport)}"
        )
        message.attach(attachment)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
            serveur.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)
            serveur.sendmail(EMAIL_EXPEDITEUR, EMAIL_DESTINATAIRE, message.as_string())
        print(f"✅ E-mail envoyé à : {EMAIL_DESTINATAIRE}")
    except Exception as e:
        print(f"❌ Erreur envoi e-mail : {e}")