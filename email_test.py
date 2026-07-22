import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configuration
EMAIL_EXPEDITEUR   = "basseux.florian62137@gmail.com"
MOT_DE_PASSE       = "seqj bgrn delb aqji"
EMAIL_DESTINATAIRE = "laboutiquedeflorian@gmail.com"
CHEMIN_FICHIER     = "C:/Users/florian/pandas_project/reporting_cdg.xlsx"

# Créer le message
message = MIMEMultipart()
message["From"]    = EMAIL_EXPEDITEUR
message["To"]      = EMAIL_DESTINATAIRE
message["Subject"] = "📊 Reporting CDG — Analyse mensuelle"

# Corps du message
corps = """
Bonjour,

Veuillez trouver en pièce jointe le reporting CDG du mois.

Points clés :
- CA Réel Total : 2.96M€
- Écart vs Budget : +10k€
- Taux de marge moyen : 15.5%

Cordialement,
Le système de reporting CDG
"""

message.attach(MIMEText(corps, "plain"))

# Attacher le fichier Excel
with open(CHEMIN_FICHIER, "rb") as fichier:
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(fichier.read())
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(CHEMIN_FICHIER)}"
    )
    message.attach(attachment)

# Envoi
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
        serveur.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)
        serveur.sendmail(EMAIL_EXPEDITEUR, EMAIL_DESTINATAIRE, message.as_string())
    print("✅ E-mail avec pièce jointe envoyé avec succès !")

except Exception as e:
    print(f"❌ Erreur : {e}")




