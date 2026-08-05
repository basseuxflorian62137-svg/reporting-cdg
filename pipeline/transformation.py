import pandas as pd
import numpy as np

def transformer_donnees(df):
    """Nettoie et enrichit les données brutes"""

    print("🔄 Transformation des données...")

    # 1 — Nettoyer les données
    df = df.dropna(how="all")
    df = df.drop_duplicates()
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["mois"] = df["date"].dt.strftime("%B %Y")
    df["trimestre"] = "T" + df["date"].dt.quarter.astype(str)

    # 2 — Calculs financiers
    df["ecart_valeur"] = df["ca_reel"] - df["ca_budget"]
    df["ecart_pct"]    = round((df["ecart_valeur"] / df["ca_budget"]) * 100, 2)
    df["marge"]        = df["ca_reel"] - df["charges"]
    df["taux_marge"]   = round((df["marge"] / df["ca_reel"]) * 100, 2)
    df["ca_moyen_vh"]  = round(df["ca_reel"] / df["nb_vehicules"], 0)

    # 3 — Statut
    df["statut"] = np.where(df["ecart_pct"] > 5,  "🟢 Excellent",
                   np.where(df["ecart_pct"] >= 0,  "🟡 Dans les normes",
                                                    "🔴 Alerte"))

    print(f"✅ Transformation terminée — {len(df)} lignes enrichies")
    return df

def agreger_par_site(df):
    """Agrège les données par site"""
    resume = df.groupby("site").agg(
        ca_reel    = ("ca_reel",    "sum"),
        ca_budget  = ("ca_budget",  "sum"),
        charges    = ("charges",    "sum"),
        nb_vehicules = ("nb_vehicules", "sum")
    ).reset_index()

    resume["ecart_valeur"] = resume["ca_reel"] - resume["ca_budget"]
    resume["ecart_pct"]    = round((resume["ecart_valeur"] / resume["ca_budget"]) * 100, 2)
    resume["marge"]        = resume["ca_reel"] - resume["charges"]
    resume["taux_marge"]   = round((resume["marge"] / resume["ca_reel"]) * 100, 2)

    print(f"✅ Agrégation par site — {len(resume)} sites")
    return resume

def agreger_par_marque(df):
    """Agrège les données par marque"""
    resume = df.groupby("marque").agg(
        ca_reel      = ("ca_reel",      "sum"),
        ca_budget    = ("ca_budget",    "sum"),
        nb_vehicules = ("nb_vehicules", "sum")
    ).reset_index()

    resume["ecart_pct"]   = round((resume["ca_reel"] - resume["ca_budget"]) / resume["ca_budget"] * 100, 2)
    resume["ca_moyen_vh"] = round(resume["ca_reel"] / resume["nb_vehicules"], 0)

    print(f"✅ Agrégation par marque — {len(resume)} marques")
    return resume

if __name__ == "__main__":
    df = pd.read_excel("C:/Users/florian/pandas_project/data/input/export_carbase.xlsx")
    df_transforme   = transformer_donnees(df)
    df_par_site     = agreger_par_site(df_transforme)
    df_par_marque   = agreger_par_marque(df_transforme)
    print("\n--- Par site ---")
    print(df_par_site)
    print("\n--- Par marque ---")
    print(df_par_marque)