import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import get_data

st.title("📋 Données brutes")
st.markdown("---")

df = get_data()

# Filtres
col1, col2 = st.columns(2)
with col1:
    bus = st.multiselect(
        "Filtrer par BU :",
        options=df["bu"].tolist(),
        default=df["bu"].tolist()
    )
with col2:
    trimestres = st.multiselect(
        "Filtrer par trimestre :",
        options=df["trimestre"].unique().tolist(),
        default=df["trimestre"].unique().tolist()
    )

# Appliquer les filtres
df_filtre = df[(df["bu"].isin(bus)) & (df["trimestre"].isin(trimestres))]

# Afficher le tableau
st.dataframe(df_filtre, use_container_width=True)

# Statistiques
st.markdown("---")
st.subheader("📊 Statistiques")
col1, col2, col3 = st.columns(3)
col1.metric("Nombre de BUs",  len(df_filtre))
col2.metric("CA Réel Total",  f"{df_filtre['ca_reel'].sum()/1000:.0f}k€")
col3.metric("Marge Totale",   f"{df_filtre['marge'].sum()/1000:.0f}k€")