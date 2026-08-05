import csv

# Lecture du fichier
with open("C:/Users/florian/pandas_project/budget.csv", "r", encoding="utf-8") as fichier:
    reader = csv.DictReader(fichier)  # lit chaque ligne comme un dictionnaire
    
    for ligne in reader:
        bu = ligne["bus"]
        ca_reel = int(ligne["ca_reel"])
        ca_budget = int(ligne["ca_budget"])
        
        print(bu, "| CA Réel :", ca_reel, "| CA Budget :", ca_budget)