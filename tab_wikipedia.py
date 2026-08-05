import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_immatriculations():
    # Données immatriculations automobiles en Europe
    url = "https://fr.wikipedia.org/wiki/Industrie_automobile_en_France"
    headers = {"User-Agent": "Mozilla/5.0"}

    reponse = requests.get(url, headers=headers)
    soup = BeautifulSoup(reponse.text, "html.parser")

    # Trouver le premier tableau
    tableau = soup.find("table", {"class": "wikitable"})

    if tableau:
        # Utiliser pandas pour lire directement le tableau HTML
        df = pd.read_html(str(tableau))[0]
        return df
    return None

df = get_immatriculations()
if df is not None:
    print(df.head())