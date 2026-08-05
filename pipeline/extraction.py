import pandas as pd
import os
from datetime import datetime

def creer_export_simule():
    """Simule un export Carbase en créant un fichier Excel de test"""

    data = {
        "date":          ["01/01/2024", "01/02/2024", "01/03/2024",
                          "01/04/2024", "01/05/2024", "01/06/2024"],
        "site":          ["Paris", "Lyon", "Paris", "Marseille", "Lyon", "Paris"],
        "marque":        ["Peugeot", "Renault", "Citroën", "Peugeot", "Renault", "Citroën"],
        "type_vente":    ["VN", "VO", "VN", "VO", "VN", "VO"],
        "ca_reel":       [450000, 280000, 320000, 190000, 410000, 260000],
        "ca_budget":     [400000, 300000, 350000, 200000, 380000, 280000],
        "charges":       [350000, 220000, 260000, 160000, 310000, 210000],
        "nb_vehicules":  [45, 28, 32, 19, 41, 26]
    }

    df = pd.DataFrame(data)

    # Sauvegarder dans data/input
    chemin = "C:/Users/florian/pandas_project/data/input/export_carbase.xlsx"
    df.to_excel(chemin, index=False)
    print(f"✅ Export Carbase simulé créé — {len(df)} lignes")
    return chemin

def charger_donnees(chemin):
    """Charge les données depuis l'export Carbase"""
    try:
        df = pd.read_excel(chemin)
        print(f"✅ Données chargées — {len(df)} lignes, {len(df.columns)} colonnes")
        return df
    except Exception as e:
        print(f"❌ Erreur de chargement : {e}")
        return None

def get_taux_eur_usd():
    """Récupère le taux EUR/USD depuis le web"""
    import requests
    from bs4 import BeautifulSoup

    try:
        url = "https://www.x-rates.com/table/?from=EUR&amount=1"
        headers = {"User-Agent": "Mozilla/5.0"}
        reponse = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(reponse.text, "html.parser")
        tableau = soup.find("table", {"class": "tablesorter"})
        lignes = tableau.find_all("tr")

        for ligne in lignes:
            colonnes = ligne.find_all("td")
            if colonnes and "US Dollar" in colonnes[0].text:
                taux = float(colonnes[1].text.strip())
                print(f"✅ Taux EUR/USD récupéré : {taux}")
                return taux

    except Exception as e:
        print(f"⚠️ Impossible de récupérer le taux : {e} — taux par défaut utilisé")
        return 1.08  # taux par défaut

if __name__ == "__main__":
    chemin = creer_export_simule()
    df = charger_donnees(chemin)
    print(df)