import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import get_data

st.title("📌 Vue Globale")
st.markdown("---")

df = get_data()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("CA Réel Total",       f"{df['ca_reel'].sum()/1000000:.1f}M€")
col2.metric("CA Budget Total",     f"{df['ca_budget'].sum()/1000000:.1f}M€")
col3.metric("Écart Total",         f"{df['ecart_valeur'].sum()/1000:.0f}k€",
            delta=f"{round(df['ecart_valeur'].sum()/df['ca_budget'].sum()*100, 2)}%")
col4.metric("Taux de marge moyen", f"{df['taux_marge'].mean():.1f}%")

st.markdown("---")

# Tableau synthèse
st.subheader("📋 Synthèse par BU")
st.dataframe(df.style.map(
    lambda x: "background-color: #C6EFCE" if isinstance(x, float) and x > 0
    else ("background-color: #FFC7CE" if isinstance(x, float) and x < 0 else ""),
    subset=["ecart_pct"]
), use_container_width=True)

# Alertes
st.markdown("---")
st.subheader("⚠️ Alertes")
bu_alertes = df[df["ecart_pct"] < 0]
if len(bu_alertes) > 0:
    for _, row in bu_alertes.iterrows():
        st.error(f"🔴 {row['bu']} — Écart : {row['ecart_pct']}%")
else:
    st.success("✅ Toutes les BUs sont dans les objectifs !")