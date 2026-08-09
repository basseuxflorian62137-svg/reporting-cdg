# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os

# ─────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Suivi des livraisons",
    layout="wide"
)

# ─────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────
CHEMIN_EXCEL = r"C:\Users\florian\pandas_project\Synthèse VN 2026.xlsx"
CHEMIN_LOGO  = r"C:\Users\florian\pandas_project\logoValauto"

NOMS_SITES = {
    10: "Valauto RONCQ",
    20: "Valauto PROFESSIONNELS",
    30: "Valauto LAMBERSART",
    60: "Val de Lys",
    70: "Valauto LOMME",
    15: "Valauto HAINAUT",
    25: "Valauto MAUBEUGE",
    35: "Valauto CAMBRAI",
    45: "Valauto ARRAS",
}

NOMS_MARQUES = {
    "VW":  "Volkswagen",
    "SK":  "Skoda",
    "HY":  "Hyundai",
    "VU":  "VUL",
    "SE":  "SEAT",
}

MOIS_FR = {
    1: "Janvier", 2: "Février",  3: "Mars",
    4: "Avril",   5: "Mai",      6: "Juin",
    7: "Juillet", 8: "Août",     9: "Septembre",
    10: "Octobre",11: "Novembre",12: "Décembre",
}

COULEUR_HEADER = "#094780"

# ─────────────────────────────────────────────
# CSS global
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Titre principal */
    .titre-livraisons {
        font-family: Arial, sans-serif;
        font-size: 28px;
        color: #094780;
        font-weight: bold;
        margin-bottom: 8px;
    }

    /* Séparateur sous-titre de section */
    .section-titre {
        font-family: Arial, sans-serif;
        font-size: 14px;
        font-weight: bold;
        color: #094780;
        margin-top: 24px;
        margin-bottom: 4px;
        border-left: 4px solid #094780;
        padding-left: 8px;
    }

    /* Note italique sous tableau */
    .note-tableau {
        font-size: 8pt;
        font-style: italic;
        color: #555;
        margin-top: 2px;
    }

    /* Supprimer le padding Streamlit autour des dataframes */
    .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# En-tête : titre + logo
# ─────────────────────────────────────────────
col_titre, col_logo = st.columns([5, 1])

with col_titre:
    st.markdown('<p class="titre-livraisons">Suivi des livraisons</p>', unsafe_allow_html=True)

with col_logo:
    # Cherche le logo (png, jpg, jpeg)
    logo_trouve = False
    for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
        chemin_logo_complet = CHEMIN_LOGO + ext
        if os.path.exists(chemin_logo_complet):
            st.image(chemin_logo_complet, width=160)
            logo_trouve = True
            break
    if not logo_trouve:
        # Essaie sans extension (si le chemin inclut déjà l'extension)
        if os.path.exists(CHEMIN_LOGO):
            st.image(CHEMIN_LOGO, width=160)

st.markdown("---")

# ─────────────────────────────────────────────
# Chargement et préparation des données
# ─────────────────────────────────────────────
@st.cache_data
def charger_donnees():
    df = pd.read_excel(CHEMIN_EXCEL, sheet_name="Marges VN")

    # Conversion de la date de livraison
    df["Date de Livraison"] = pd.to_datetime(df["Date de Livraison"], errors="coerce")

    # Extraction du mois
    df["Mois_num"] = df["Date de Livraison"].dt.month
    df["Mois_nom"] = df["Mois_num"].map(MOIS_FR)

    # Remplacement des codes sites
    df["Site_nom"] = df["Site"].map(NOMS_SITES).fillna(df["Site"].astype(str))

    # Remplacement des codes marques
    # Détecter la colonne marque
    col_marque = None
    for c in df.columns:
        if "marque" in c.lower():
            col_marque = c
            break

    if col_marque:
        df["Marque_nom"] = df[col_marque].map(NOMS_MARQUES).fillna(df[col_marque])
    else:
        df["Marque_nom"] = "Inconnue"

    return df, col_marque

try:
    df, col_marque = charger_donnees()
except Exception as e:
    st.error(f"❌ Impossible de charger le fichier : {e}")
    st.stop()

# ─────────────────────────────────────────────
# Fonction : mise en forme des tableaux
# ─────────────────────────────────────────────
def styler_tableau(df_pivot, format_fn=None):
    """Applique le style corporate au tableau pivot."""

    def style_header(s):
        return [
            f"background-color: {COULEUR_HEADER}; color: white; "
            "font-weight: bold; font-size: 8pt; text-align: center;"
        ] * len(s)

    def style_index(s):
        return [
            f"background-color: {COULEUR_HEADER}; color: white; "
            "font-weight: bold; font-size: 8pt;"
        ] * len(s)

    def centrer_valeurs(s):
        return ["text-align: center; font-size: 9pt;"] * len(s)

    styler = (
        df_pivot.style
        .apply(style_header, axis=1, subset=pd.IndexSlice[:, :])  # colonnes
        .apply(centrer_valeurs, axis=1)
        .apply_index(lambda s: [
            f"background-color: {COULEUR_HEADER}; color: white; "
            "font-weight: bold; font-size: 8pt;"
        ] * len(s), axis=0)
        .apply_index(lambda s: [
            f"background-color: {COULEUR_HEADER}; color: white; "
            "font-weight: bold; font-size: 8pt; text-align: center;"
        ] * len(s), axis=1)
    )

    if format_fn:
        styler = styler.format(format_fn)

    return styler

# ─────────────────────────────────────────────
# Ordre des mois (colonnes triées chronologiquement)
# ─────────────────────────────────────────────
mois_presents = sorted(df["Mois_num"].dropna().unique().astype(int))
mois_colonnes = [MOIS_FR[m] for m in mois_presents]

# ─────────────────────────────────────────────
# TABLEAU 1 — Nb véhicules livrés par SITE et par mois
# ─────────────────────────────────────────────
st.markdown('<p class="section-titre">Nombre de véhicules livrés par site et par mois</p>',
            unsafe_allow_html=True)

df_livres = df.dropna(subset=["Date de Livraison"]).copy()

pivot_site_nb = (
    df_livres
    .groupby(["Site_nom", "Mois_nom", "Mois_num"])["Châssis"]
    .nunique()
    .reset_index()
    .rename(columns={"Châssis": "nb"})
)

pivot_site_nb = pivot_site_nb.pivot_table(
    index="Site_nom",
    columns="Mois_nom",
    values="nb",
    aggfunc="sum",
    fill_value=0
)

# Réordonner les colonnes par mois chronologique
pivot_site_nb = pivot_site_nb.reindex(
    columns=[m for m in mois_colonnes if m in pivot_site_nb.columns],
    fill_value=0
)

# Ajouter colonne Total
pivot_site_nb["Total"] = pivot_site_nb.sum(axis=1)
pivot_site_nb.index.name = "Site"

st.dataframe(
    styler_tableau(pivot_site_nb, format_fn=lambda x: f"{int(x):,}".replace(",", " ") if x != 0 else "–"),
    use_container_width=True
)

# ─────────────────────────────────────────────
# TABLEAU 2 — Marge moyenne par SITE et par mois
# ─────────────────────────────────────────────
st.markdown('<p class="section-titre">Marge nette moyenne par site et par mois (€)</p>',
            unsafe_allow_html=True)

df_marge = df[df["Etat"].isin(["C", "NP"])].dropna(subset=["Date de Livraison"]).copy()

pivot_site_marge = (
    df_marge
    .groupby(["Site_nom", "Mois_nom", "Mois_num"])["Marge nette recalculée"]
    .mean()
    .reset_index()
    .rename(columns={"Marge nette recalculée": "marge_moy"})
)

pivot_site_marge = pivot_site_marge.pivot_table(
    index="Site_nom",
    columns="Mois_nom",
    values="marge_moy",
    aggfunc="mean",
    fill_value=None
)

pivot_site_marge = pivot_site_marge.reindex(
    columns=[m for m in mois_colonnes if m in pivot_site_marge.columns]
)

pivot_site_marge.index.name = "Site"

st.dataframe(
    styler_tableau(
        pivot_site_marge,
        format_fn=lambda x: f"{x:,.0f} €".replace(",", " ") if pd.notna(x) else "–"
    ),
    use_container_width=True
)

st.markdown(
    '<p class="note-tableau">* Seules les marges VN conformes (C &amp; NP) sont prises en compte '
    'dans le calcul des marges moyennes</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# ─────────────────────────────────────────────
# TABLEAU 3 — Nb véhicules livrés par MARQUE et par mois
# ─────────────────────────────────────────────
st.markdown('<p class="section-titre">Nombre de véhicules livrés par marque et par mois</p>',
            unsafe_allow_html=True)

pivot_marque_nb = (
    df_livres
    .groupby(["Marque_nom", "Mois_nom", "Mois_num"])["Châssis"]
    .nunique()
    .reset_index()
    .rename(columns={"Châssis": "nb"})
)

pivot_marque_nb = pivot_marque_nb.pivot_table(
    index="Marque_nom",
    columns="Mois_nom",
    values="nb",
    aggfunc="sum",
    fill_value=0
)

pivot_marque_nb = pivot_marque_nb.reindex(
    columns=[m for m in mois_colonnes if m in pivot_marque_nb.columns],
    fill_value=0
)

pivot_marque_nb["Total"] = pivot_marque_nb.sum(axis=1)
pivot_marque_nb.index.name = "Marque"

st.dataframe(
    styler_tableau(pivot_marque_nb, format_fn=lambda x: f"{int(x):,}".replace(",", " ") if x != 0 else "–"),
    use_container_width=True
)

# ─────────────────────────────────────────────
# TABLEAU 4 — Marge moyenne par MARQUE et par mois
# ─────────────────────────────────────────────
st.markdown('<p class="section-titre">Marge nette moyenne par marque et par mois (€)</p>',
            unsafe_allow_html=True)

pivot_marque_marge = (
    df_marge
    .groupby(["Marque_nom", "Mois_nom", "Mois_num"])["Marge nette recalculée"]
    .mean()
    .reset_index()
    .rename(columns={"Marge nette recalculée": "marge_moy"})
)

pivot_marque_marge = pivot_marque_marge.pivot_table(
    index="Marque_nom",
    columns="Mois_nom",
    values="marge_moy",
    aggfunc="mean",
    fill_value=None
)

pivot_marque_marge = pivot_marque_marge.reindex(
    columns=[m for m in mois_colonnes if m in pivot_marque_marge.columns]
)

pivot_marque_marge.index.name = "Marque"

st.dataframe(
    styler_tableau(
        pivot_marque_marge,
        format_fn=lambda x: f"{x:,.0f} €".replace(",", " ") if pd.notna(x) else "–"
    ),
    use_container_width=True
)

st.markdown(
    '<p class="note-tableau">* Seules les marges VN conformes (C &amp; NP) sont prises en compte '
    'dans le calcul des marges moyennes</p>',
    unsafe_allow_html=True
)