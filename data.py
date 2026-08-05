import pandas as pd
import os
import sys

# Ajouter le dossier pipeline au chemin
sys.path.append(os.path.join(os.path.dirname(__file__), "pipeline"))

from extraction     import creer_export_simule, charger_donnees
from transformation import transformer_donnees, agreger_par_site, agreger_par_marque

def get_data():
    """Charge les données depuis le CSV généré par le pipeline"""

    chemin_csv = os.path.join(os.path.dirname(__file__), 
                              "data/output/data_dashboard.csv")

    # Si le CSV existe — on le lit directement
    if os.path.exists(chemin_csv):
        df = pd.read_csv(chemin_csv)
        return df

    # Sinon — on génère les données depuis extraction.py
    else:
        chemin = creer_export_simule()
        df_brut = charger_donnees(chemin)
        df = transformer_donnees(df_brut)
        return df