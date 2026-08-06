import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data import get_data

st.title("📌 Vue Globale")
st.markdown("---")

df = get_data()
st.write("Colonnes disponibles :", df.columns.tolist())  # ← debug temporaire
st.write("5 premières lignes :", df.head())              # ← debug temporaire

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("CA Réel Total",       f"{df['ca_reel'].sum()/1000000:.1f}M€")
col2.metric("CA Budget Total",     f"{df['ca_budget'].sum()/1000000:.1f}M€")
col3.metric("Écart Total",         f"{df['ecart_valeur'].sum()/1000:.0f}k€",
            delta=f"{round(df['ecart_valeur'].sum()/df['ca_budget'].sum()*100, 2)}%")
col4.metric("Taux de marge moyen", f"{df['taux_marge'].mean():.1f}%")

st.markdown("---")

# Tableau synthèse par site
st.subheader("📋 Synthèse par site")
df_site = df.groupby("site")[["ca_reel", "ca_budget", "marge"]].sum().reset_index()
df_site["ecart_valeur"] = df_site["ca_reel"] - df_site["ca_budget"]
df_site["ecart_pct"]    = round(df_site["ecart_valeur"] / df_site["ca_budget"] * 100, 2)
df_site["taux_marge"]   = round(df_site["marge"] / df_site["ca_reel"] * 100, 2)
st.dataframe(df_site, use_container_width=True)

st.markdown("---")

# Alertes
st.subheader("⚠️ Alertes")
alertes = df_site[df_site["ecart_pct"] < 0]
if len(alertes) > 0:
    for _, row in alertes.iterrows():
        st.error(f"🔴 {row['site']} — Écart : {row['ecart_pct']}%")
else:
    st.success("✅ Tous les sites sont dans les objectifs !")