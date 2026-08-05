import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_taux_change():
    url = "https://www.x-rates.com/table/?from=EUR&amount=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    reponse = requests.get(url, headers=headers)
    soup = BeautifulSoup(reponse.text, "html.parser")

    # Trouver le tableau des taux
    tableau = soup.find("table", {"class": "tablesorter"})
    lignes = tableau.find_all("tr")[1:]  # ignorer l'en-tête

    taux = []
    for ligne in lignes:
        colonnes = ligne.find_all("td")
        if len(colonnes) >= 2:
            devise = colonnes[0].text.strip()
            taux_valeur = float(colonnes[1].text.strip())
            taux.append({"devise": devise, "taux_eur": taux_valeur})

    df = pd.DataFrame(taux)
    df["date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    return df

# Récupérer et afficher les taux
df_taux = get_taux_change()
print(df_taux.head(10))