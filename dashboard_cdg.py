import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
st.set_page_config(page_title="Reporting CDG", page_icon="📊", layout="wide")

# Titre + Logo
col_titre, col_logo = st.columns([4, 1])

with col_titre:
    st.title("📊 Dashboard Contrôle de Gestion")

with col_logo:
    st.image("C:/Users/florian/pandas_project/logo.png", width=150)

st.markdown("---")

# Données
data = {
    "bu":        ["France", "Allemagne", "Espagne", "Italie"],
    "ca_reel":   [1200000, 980000, 400000, 380000],
    "ca_budget": [1100000, 1050000, 450000, 350000],
    "charges":   [900000, 820000, 360000, 340000]
}

df = pd.DataFrame(data)
df["ecart_valeur"] = df["ca_reel"] - df["ca_budget"]
df["ecart_pct"]    = round((df["ecart_valeur"] / df["ca_budget"]) * 100, 2)
df["marge"]        = df["ca_reel"] - df["charges"]
df["taux_marge"]   = round((df["marge"] / df["ca_reel"]) * 100, 2)

# Section 1 — KPIs globaux
st.subheader("📌 Indicateurs clés")
col1, col2, col3, col4 = st.columns(4)

col1.metric("CA Réel Total",       f"{df['ca_reel'].sum()/1000000:.1f}M€")
col2.metric("CA Budget Total",     f"{df['ca_budget'].sum()/1000000:.1f}M€")
col3.metric("Écart Total",         f"{df['ecart_valeur'].sum()/1000:.0f}k€")
col4.metric("Taux de marge moyen", f"{df['taux_marge'].mean():.1f}%")

st.markdown("---")

# Section 2 — Filtre et analyse par BU
st.subheader("🔍 Analyse par BU")

bu_selectionnee = st.selectbox("Sélectionne une BU :", options=df["bu"].tolist())
df_filtre = df[df["bu"] == bu_selectionnee]
ligne = df_filtre.iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("CA Réel",       f"{ligne['ca_reel']/1000:.0f}k€")
col2.metric("Écart valeur",  f"{ligne['ecart_valeur']/1000:.0f}k€",
            delta=f"{ligne['ecart_pct']}%")
col3.metric("Taux de marge", f"{ligne['taux_marge']}%")

st.markdown("---")

# Section 3 — Tableau complet
st.subheader("📋 Tableau complet")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# Section 4 — Graphique
st.subheader("📈 CA Réel vs Budget par BU")

fig, ax = plt.subplots(figsize=(10, 5))

x = range(len(df["bu"]))
ax.bar([i - 0.2 for i in x], df["ca_reel"],   0.4,
       label="CA Réel",   color="#1F4E79")
ax.bar([i + 0.2 for i in x], df["ca_budget"], 0.4,
       label="CA Budget", color="#C00000", alpha=0.7)

ax.set_xticks(x)
ax.set_xticklabels(df["bu"])
ax.set_ylabel("CA (€)")
ax.legend()
ax.grid(True, axis="y", alpha=0.3)
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"{x/1000:.0f}k€")
)

st.pyplot(fig)





