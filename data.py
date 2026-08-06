# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline"))
from transformation import transformer_donnees

def get_data():
    data = {
        "date":         ["01/01/2024", "01/02/2024", "01/03/2024",
                         "01/04/2024", "01/05/2024", "01/06/2024"],
        "site":         ["Paris", "Lyon", "Paris", "Marseille", "Lyon", "Paris"],
        "marque":       ["Peugeot", "Renault", "Citroen", "Peugeot", "Renault", "Citroen"],
        "type_vente":   ["VN", "VO", "VN", "VO", "VN", "VO"],
        "ca_reel":      [450000, 280000, 320000, 190000, 410000, 260000],
        "ca_budget":    [400000, 300000, 350000, 200000, 380000, 280000],
        "charges":      [350000, 220000, 260000, 160000, 310000, 210000],
        "nb_vehicules": [45, 28, 32, 19, 41, 26]
    }
    df_brut = pd.DataFrame(data)
    df      = transformer_donnees(df_brut)
    return df