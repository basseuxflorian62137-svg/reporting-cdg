import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Reporting CDG", page_icon="📊", layout="wide")

# Titre
st.title("📊 Dashboard Contrôle de Gestion")
st.markdown("---")

# Données
data = {
    "bu":        ["France", "Allemagne", "Espagne", "Italie"],
    "ca_reel":   [1200000, 980000, 400000, 380000],
    "ca_budget": [1100000, 1050000, 450000, 350000],
    "charges":   [900000,  820000,  360000, 340000]
}

df = pd.DataFrame(data)
df["ecart_valeur"] = df["ca_reel"] - df["ca_budget"]
df["ecart_pct"]    = round((df["ecart_valeur"] / df["ca_budget"]) * 100, 2)
df["marge"]        = df["ca_reel"] - df["charges"]
df["taux_marge"]   = round((df["marge"] / df["ca_reel"]) * 100, 2)

# KPIs en haut de page
st.subheader("📌 Indicateurs clés")
col1, col2, col3, col4 = st.columns(4)

col1.metric("CA Réel Total",    f"{df['ca_reel'].sum()/1000000:.1f}M€")
col2.metric("CA Budget Total",  f"{df['ca_budget'].sum()/1000000:.1f}M€")
col3.metric("Écart Total",      f"{df['ecart_valeur'].sum()/1000:.0f}k€")
col4.metric("Marge Totale",     f"{df['marge'].sum()/1000:.0f}k€")

st.markdown("---")

# Tableau de données
st.subheader("📋 Tableau de bord par BU")
st.dataframe(df, use_container_width=True)





