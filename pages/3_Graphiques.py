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

# Agrégation par site
df_site = df.groupby("site")[["ca_reel", "ca_budget", "marge"]].sum().reset_index()
df_site["taux_marge"] = round(df_site["marge"] / df_site["ca_reel"] * 100, 2)

# Graphique 1 — CA Réel vs Budget par site
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=df_site["site"], y=df_site["ca_reel"],
    name="CA Réel", marker_color="#1F4E79",
    hovertemplate="<b>%{x}</b><br>CA Réel : %{y:,.0f}€<extra></extra>"
))
fig1.add_trace(go.Bar(
    x=df_site["site"], y=df_site["ca_budget"],
    name="CA Budget", marker_color="#C00000", opacity=0.7,
    hovertemplate="<b>%{x}</b><br>CA Budget : %{y:,.0f}€<extra></extra>"
))
fig1.update_layout(
    title="CA Réel vs Budget par site",
    barmode="group",
    template="plotly_white"
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Graphique 2 — Taux de marge par site
fig2 = go.Figure(go.Bar(
    x=df_site["site"],
    y=df_site["taux_marge"],
    marker_color=["#C6EFCE" if v > 15 else "#FFC7CE" for v in df_site["taux_marge"]],
    hovertemplate="<b>%{x}</b><br>Taux de marge : %{y:.1f}%<extra></extra>"
))
fig2.update_layout(
    title="Taux de marge par site",
    template="plotly_white"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Graphique 3 — CA par marque
st.subheader("🚗 CA par marque")
df_marque = df.groupby("marque")[["ca_reel", "ca_budget"]].sum().reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=df_marque["marque"], y=df_marque["ca_reel"],
    name="CA Réel", marker_color="#1F4E79"
))
fig3.add_trace(go.Bar(
    x=df_marque["marque"], y=df_marque["ca_budget"],
    name="CA Budget", marker_color="#C00000", opacity=0.7
))
fig3.update_layout(
    title="CA par marque",
    barmode="group",
    template="plotly_white"
)
st.plotly_chart(fig3, use_container_width=True)