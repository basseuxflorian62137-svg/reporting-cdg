import streamlit as st

st.set_page_config(
    page_title="Reporting CDG",
    page_icon="📊",
    layout="wide"
)

# Titre et logo
col_titre, col_logo = st.columns([4, 1])
with col_titre:
    st.title("📊 Dashboard Contrôle de Gestion")
with col_logo:
    try:
        st.image("logo.png", width=150)
    except:
        pass

st.markdown("---")

st.markdown("""
### 👋 Bienvenue sur le Dashboard CDG

Utilise le menu à gauche pour naviguer entre les sections :

- 📌 **Vue Globale** — KPIs consolidés et synthèse
- 🔍 **Analyse par site** — Drill-down par site et marque
- 📈 **Graphiques** — Visualisations interactives
- 📋 **Données** — Tableau complet et export
- ⚙️ **Pipeline** — Chargement et analyse des données
""")