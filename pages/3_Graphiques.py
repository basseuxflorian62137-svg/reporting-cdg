import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data import get_data

st.title("📈 Graphiques")
st.markdown("---")

df = get_data()

# Graphique 1 — CA Réel vs Budget
fig1 = go.Figure()

fig1.add_trace(go.Bar(
    x=df["bu"], y=df["ca_reel"],
    name="CA Réel", marker_color="#1F4E79",
    hovertemplate="<b>%{x}</b><br>CA Réel : %{y:,.0f}€<extra></extra>"
))

fig1.add_trace(go.Bar(
    x=df["bu"], y=df["ca_budget"],
    name="CA Budget", marker_color="#C00000", opacity=0.7,
    hovertemplate="<b>%{x}</b><br>CA Budget : %{y:,.0f}€<extra></extra>"
))

fig1.update_layout(
    title="CA Réel vs Budget par BU",
    barmode="group",
    template="plotly_white"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Graphique 2 — Taux de marge
fig2 = go.Figure(go.Bar(
    x=df["bu"],
    y=df["taux_marge"],
    marker_color=["#C6EFCE" if v > 15 else "#FFC7CE" for v in df["taux_marge"]],
    hovertemplate="<b>%{x}</b><br>Taux de marge : %{y:.1f}%<extra></extra>"
))

fig2.update_layout(
    title="Taux de marge par BU",
    template="plotly_white"
)

st.plotly_chart(fig2, use_container_width=True)