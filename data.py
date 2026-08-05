import pandas as pd
import os
import sys

# Ajouter le dossier pipeline au chemin
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline"))

from extraction     import creer_export_simule, charger_donnees
from transformation import transformer_donnees

def get_data():
    """Charge les données depuis le CSV ou génère depuis extraction.py"""

    chemin_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "data/output/data_dashboard.csv")

    # Si le CSV existe — on le lit directement
    if os.path.exists(chemin_csv):
        df = pd.read_csv(chemin_csv)
        return df

    # Sinon — on génère depuis extraction.py
    else:
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "data/input/export_carbase.xlsx")

        # Créer le fichier simulé si nécessaire
        if not os.path.exists(chemin):
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            creer_export_simule()

        df_brut = charger_donnees(chemin)
        df      = transformer_donnees(df_brut)
        return df