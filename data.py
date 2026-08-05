import pandas as pd

def get_data():
    data = {
        "bu":        ["France", "Allemagne", "Espagne", "Italie"],
        "ca_reel":   [1200000, 980000, 400000, 380000],
        "ca_budget": [1100000, 1050000, 450000, 350000],
        "charges":   [900000, 820000, 360000, 340000],
        "trimestre": ["T1", "T2", "T1", "T2"]
    }

    df = pd.DataFrame(data)
    df["ecart_valeur"] = df["ca_reel"] - df["ca_budget"]
    df["ecart_pct"]    = round((df["ecart_valeur"] / df["ca_budget"]) * 100, 2)
    df["marge"]        = df["ca_reel"] - df["charges"]
    df["taux_marge"]   = round((df["marge"] / df["ca_reel"]) * 100, 2)

    return df