import requests
from bs4 import BeautifulSoup

# Télécharger une page web
url = "https://www.boursorama.com/bourse/devises/converter/"
headers = {"User-Agent": "Mozilla/5.0"}  # se faire passer pour un navigateur

reponse = requests.get(url, headers=headers)

print(f"✅ Statut : {reponse.status_code}")  # 200 = succès
print(f"📄 Taille de la page : {len(reponse.text)} caractères")

# Analyser le HTML
soup = BeautifulSoup(reponse.text, "html.parser")

# Afficher le titre de la page
print(f"📌 Titre : {soup.title.text}")
