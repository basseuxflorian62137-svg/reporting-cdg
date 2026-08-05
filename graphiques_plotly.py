import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

data = {
    "mois":      ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun",
                  "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"],
    "ca_reel":   [980000, 1020000, 1100000, 950000, 1080000, 1150000,
                  1200000, 1050000, 1180000, 1220000, 1300000, 1400000],
    "ca_budget": [1000000, 1000000, 1050000, 1000000, 1050000, 1100000,
                  1100000, 1100000, 1150000, 1200000, 1250000, 1300000],
    "charges":   [750000, 780000, 820000, 730000, 800000, 850000,
                  880000, 790000, 860000, 900000, 950000, 1020000]
}

df = pd.DataFrame(data)
df["taux_marge"] = round((df["ca_reel"] - df["charges"]) / df["ca_reel"] * 100, 2)

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"colspan": 2}, None],
           [{}, {}]],
    subplot_titles=(
        "CA Réel vs Budget sur 12 mois",
        "Charges par mois",
        "Taux de marge mensuel"
    )
)

# Graphique 1 — Courbes CA Réel et Budget
fig.add_trace(go.Scatter(
    x=df["mois"],
    y=df["ca_reel"],
    name="CA Réel",
    mode="lines+markers",
    line=dict(color="#1F4E79", width=2),
    marker=dict(size=8),
    hovertemplate="<b>%{x}</b><br>CA Réel : %{y:,.0f}€<extra></extra>"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df["mois"],
    y=df["ca_budget"],
    name="CA Budget",
    mode="lines+markers",
    line=dict(color="#C00000", width=2, dash="dash"),
    marker=dict(size=8),
    hovertemplate="<b>%{x}</b><br>CA Budget : %{y:,.0f}€<extra></extra>"
), row=1, col=1)

# Graphique 2 — Histogramme charges
fig.add_trace(go.Bar(
    x=df["mois"],
    y=df["charges"],
    name="Charges",
    marker_color="#ED7D31",
    hovertemplate="<b>%{x}</b><br>Charges : %{y:,.0f}€<extra></extra>"
), row=2, col=1)

# Graphique 3 — Courbe taux de marge ✅
fig.add_trace(go.Scatter(
    x=df["mois"],
    y=df["taux_marge"],
    name="Taux de marge",
    mode="lines+markers",
    line=dict(color="#70AD47", width=2),
    marker=dict(size=8),
    hovertemplate="<b>%{x}</b><br>Taux de marge : %{y:.2f}%<extra></extra>"
), row=2, col=2)

fig.update_layout(
    title="📊 Tableau de bord CDG — Vue annuelle",
    template="plotly_white",
    height=700,
    showlegend=True
)

fig.write_html("C:/Users/florian/pandas_project/exercice_plotly.html")
print("✅ Dashboard Plotly généré !")