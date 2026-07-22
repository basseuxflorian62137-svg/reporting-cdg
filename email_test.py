import schedule
import time
import subprocess
from datetime import datetime

def lancer_reporting():
    print(f"⏰ Lancement automatique — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    subprocess.run(["python", "C:/Users/florian/pandas_project/envoi_reporting.py"])

# Planification
schedule.every().day.at("08:00").do(lancer_reporting)       # Tous les jours à 8h


print("✅ Reporting généré et envoyé avec succès !")

# Boucle infinie qui vérifie les tâches planifiées


except Exception as e:
    print(f"❌ Erreur lors de l'exécution : {message d'erreur}"

while True:
    schedule.run_pending()
    time.sleep(24)  # vérifie toutes les 60 secondes


