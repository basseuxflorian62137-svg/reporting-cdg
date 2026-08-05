import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys
from datetime import datetime

st.title("⚙️ Pipeline de données")
st.markdown("---")

# Chemins
CHEMIN_META = "C:/Users/florian/pandas_project/data/output/metadata.json"

# Ajouter le dossier pipeline au chemin
sys.path.append("C:/Users/florian/pandas_project/pipeline")
from transformation import transformer_donnees, agreger_par_site, agreger_par_marque

# Section 1 — Statut du pipeline
st.subheader("📌 Statut du pipeline")

if os.path.exists(CHEMIN_META):
    with open(CHEMIN_META, "r") as f:
        meta = json.load(f)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dernière MAJ",    meta["derniere_maj"])
    col2.metric("Lignes traitées", meta["nb_lignes"])
    col3.metric("Sites analysés",  meta["nb_sites"])
    col4.metric("Taux EUR/USD",    meta["taux_eur_usd"])

    st.success(f"✅ Pipeline exécuté le {meta['derniere_maj']}")
else:
    st.warning("⚠️ Aucune donnée disponible — charge un fichier pour commencer")

st.markdown("---")

# Section 2 — Upload fichier Carbase
st.subheader("📥 Charger un export Carbase")

fichier = st.file_uploader(
    "Dépose ton export Carbase ici",
    type=["xlsx", "csv"]
)

if fichier is not None:
    # Charger le fichier
    if fichier.name.endswith(".csv"):
        df_brut = pd.read_csv(fichier)
    else:
        df_brut = pd.read_excel(fichier)

    st.success(f"✅ Fichier chargé — {len(df_brut)} lignes, {len(df_brut.columns)} colonnes")

    st.markdown("---")

    # Aperçu des données brutes
    with st.expander("👁️ Aperçu des données brutes"):
        st.dataframe(df_brut, use_container_width=True)

    # Lancer l'analyse automatiquement
    st.subheader("🔄 Analyse automatique")

    try:
        # Transformation
        df_transforme = transformer_donnees(df_brut)
        df_site       = agreger_par_site(df_transforme)
        df_marque     = agreger_par_marque(df_transforme)

        st.success("✅ Analyse terminée !")

        # KPIs
        st.markdown("---")
        st.subheader("📊 Indicateurs clés")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CA Réel Total",
                    f"{df_transforme['ca_reel'].sum()/1000:.0f}k€")
        col2.metric("CA Budget Total",
                    f"{df_transforme['ca_budget'].sum()/1000:.0f}k€")
        col3.metric("Écart Total",
                    f"{df_transforme['ecart_valeur'].sum()/1000:.0f}k€",
                    delta=f"{round(df_transforme['ecart_valeur'].sum()/df_transforme['ca_budget'].sum()*100,2)}%")
        col4.metric("Taux de marge moyen",
                    f"{df_transforme['taux_marge'].mean():.1f}%")

        st.markdown("---")

        # Graphiques
        st.subheader("📈 Visualisations")

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("CA Réel vs Budget par site", "Taux de marge par site")
        )

        fig.add_trace(go.Bar(
            x=df_site["site"], y=df_site["ca_reel"],
            name="CA Réel", marker_color="#1F4E79",
            hovertemplate="<b>%{x}</b><br>CA Réel : %{y:,.0f}€<extra></extra>"
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=df_site["site"], y=df_site["ca_budget"],
            name="CA Budget", marker_color="#C00000", opacity=0.7,
            hovertemplate="<b>%{x}</b><br>CA Budget : %{y:,.0f}€<extra></extra>"
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=df_site["site"],
            y=df_site["taux_marge"],
            name="Taux de marge",
            marker_color=["#C6EFCE" if v > 15 else "#FFC7CE" for v in df_site["taux_marge"]],
            hovertemplate="<b>%{x}</b><br>Taux de marge : %{y:.1f}%<extra></extra>"
        ), row=1, col=2)

        fig.update_layout(
            template="plotly_white",
            height=400,
            barmode="group"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Alertes
        st.subheader("⚠️ Alertes")
        bu_alertes = df_transforme[df_transforme["ecart_pct"] < 0]
        if len(bu_alertes) > 0:
            for _, row in bu_alertes.iterrows():
                st.error(f"🔴 {row['site']} — {row['marque']} : Écart {row['ecart_pct']}%")
        else:
            st.success("✅ Tous les sites sont dans les objectifs !")

        st.markdown("---")

        # Tableau détaillé avec filtres
        st.subheader("📋 Données détaillées")

        col1, col2 = st.columns(2)
        with col1:
            sites = st.multiselect(
                "Filtrer par site :",
                options=df_transforme["site"].unique().tolist(),
                default=df_transforme["site"].unique().tolist()
            )
        with col2:
            marques = st.multiselect(
                "Filtrer par marque :",
                options=df_transforme["marque"].unique().tolist(),
                default=df_transforme["marque"].unique().tolist()
            )

        df_filtre = df_transforme[
            (df_transforme["site"].isin(sites)) &
            (df_transforme["marque"].isin(marques))
        ]

        st.dataframe(df_filtre, use_container_width=True)

        # Export CSV
        st.download_button(
            label="📥 Télécharger les données analysées",
            data=df_filtre.to_csv(index=False).encode("utf-8"),
            file_name=f"analyse_cdg_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse : {e}")
        st.info("💡 Vérifie que ton fichier contient bien les colonnes : site, marque, type_vente, ca_reel, ca_budget, charges, nb_vehicules")