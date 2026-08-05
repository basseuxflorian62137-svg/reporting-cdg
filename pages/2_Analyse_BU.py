import streamlit as st
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import get_data

st.title("🔍 Analyse par site")
st.markdown("---")

df = get_data()

# Filtre site
site_selectionne = st.selectbox(
    "Sélectionne un site :",
    options=df["site"].unique().tolist()
)

df_filtre = df[df["site"] == site_selectionne]

# KPIs du site
col1, col2, col3, col4 = st.columns(4)
col1.metric("CA Réel",       f"{df_filtre['ca_reel'].sum()/1000:.0f}k€")
col2.metric("CA Budget",     f"{df_filtre['ca_budget'].sum()/1000:.0f}k€")
col3.metric("Écart",         f"{df_filtre['ecart_valeur'].sum()/1000:.0f}k€",
            delta=f"{round(df_filtre['ecart_valeur'].sum()/df_filtre['ca_budget'].sum()*100, 2)}%")
col4.metric("Taux de marge", f"{df_filtre['taux_marge'].mean():.1f}%")

st.markdown("---")

# Graphique par marque
st.subheader(f"📊 Détail par marque — {site_selectionne}")

df_marque = df_filtre.groupby("marque")[["ca_reel", "ca_budget"]].sum().reset_index()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_marque["marque"], y=df_marque["ca_reel"],
    name="CA Réel", marker_color="#1F4E79",
    hovertemplate="<b>%{x}</b><br>CA Réel : %{y:,.0f}€<extra></extra>"
))
fig.add_trace(go.Bar(
    x=df_marque["marque"], y=df_marque["ca_budget"],
    name="CA Budget", marker_color="#C00000", opacity=0.7,
    hovertemplate="<b>%{x}</b><br>CA Budget : %{y:,.0f}€<extra></extra>"
))

fig.update_layout(
    title=f"CA Réel vs Budget par marque — {site_selectionne}",
    barmode="group",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)