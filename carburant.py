import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_prix_carburants():
    url = "https://www.prix-carburants.gouv.fr/"
    headers = {"User-Agent": "Mozilla/5.0"}

    reponse = requests.get(url, headers=headers)
    soup = BeautifulSoup(reponse.text, "html.parser")

    # Extraire les prix moyens nationaux
    prix = {}

    # Trouver les éléments de prix
    elements = soup.find_all("div", {"class": "prix"})
    for element in elements:
        carburant = element.find("span", {"class": "nom"})
        valeur = element.find("span", {"class": "valeur"})
        if carburant and valeur:
            prix[carburant.text.strip()] = valeur.text.strip()

    return prix

prix = get_prix_carburants()
for carburant, valeur in prix.items():
    print(f"{carburant} : {valeur}")