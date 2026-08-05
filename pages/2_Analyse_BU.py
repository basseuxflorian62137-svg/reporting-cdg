import streamlit as st
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import get_data

st.title("🔍 Analyse par BU")
st.markdown("---")

df = get_data()

# Filtre BU
bu_selectionnee = st.selectbox("Sélectionne une BU :", options=df["bu"].tolist())
ligne = df[df["bu"] == bu_selectionnee].iloc[0]

# KPIs de la BU
col1, col2, col3, col4 = st.columns(4)
col1.metric("CA Réel",       f"{ligne['ca_reel']/1000:.0f}k€")
col2.metric("CA Budget",     f"{ligne['ca_budget']/1000:.0f}k€")
col3.metric("Écart",         f"{ligne['ecart_valeur']/1000:.0f}k€",
            delta=f"{ligne['ecart_pct']}%")
col4.metric("Taux de marge", f"{ligne['taux_marge']}%")

st.markdown("---")

# Graphique comparaison
fig = go.Figure()

fig.add_trace(go.Bar(
    x=["CA Réel", "CA Budget"],
    y=[ligne["ca_reel"], ligne["ca_budget"]],
    marker_color=["#1F4E79", "#C00000"],
    hovertemplate="%{x} : %{y:,.0f}€<extra></extra>"
))

fig.update_layout(
    title=f"CA Réel vs Budget — {bu_selectionnee}",
    template="plotly_white",
    height=400
)

st.plotly_chart(fig, use_container_width=True)