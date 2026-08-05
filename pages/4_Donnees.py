import streamlit as st
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import get_data

st.title("📋 Données brutes")
st.markdown("---")

df = get_data()

# Filtres
col1, col2, col3 = st.columns(3)
with col1:
    sites = st.multiselect(
        "Filtrer par site :",
        options=df["site"].unique().tolist(),
        default=df["site"].unique().tolist()
    )
with col2:
    marques = st.multiselect(
        "Filtrer par marque :",
        options=df["marque"].unique().tolist(),
        default=df["marque"].unique().tolist()
    )
with col3:
    types = st.multiselect(
        "Filtrer par type de vente :",
        options=df["type_vente"].unique().tolist(),
        default=df["type_vente"].unique().tolist()
    )

# Appliquer les filtres
df_filtre = df[
    (df["site"].isin(sites)) &
    (df["marque"].isin(marques)) &
    (df["type_vente"].isin(types))
]

st.dataframe(df_filtre, use_container_width=True)

# Statistiques
st.markdown("---")
st.subheader("📊 Statistiques")
col1, col2, col3 = st.columns(3)
col1.metric("Nombre de lignes",  len(df_filtre))
col2.metric("CA Réel Total",     f"{df_filtre['ca_reel'].sum()/1000:.0f}k€")
col3.metric("Marge Totale",      f"{df_filtre['marge'].sum()/1000:.0f}k€")

# Export
st.download_button(
    label="📥 Télécharger les données filtrées",
    data=df_filtre.to_csv(index=False).encode("utf-8"),
    file_name=f"export_cdg_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)