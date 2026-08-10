import streamlit as st
import pandas as pd
import os
import base64
 
# ─────────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Suivi des livraisons",
    layout="wide",
    initial_sidebar_state="collapsed"  # ✅ masque la sidebar
)


# ─────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────
CHEMIN_EXCEL = "Synthese VN 2026.xlsx"  # chemin relatif
CHEMIN_LOGO  = "logoValauto"
 
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
    "VW": "Volkswagen",
    "SK": "Skoda",
    "HY": "Hyundai",
    "VU": "VUL",
    "SE": "SEAT",
}
 
MOIS_FR = {
    1: "Janvier",  2: "Février",   3: "Mars",
    4: "Avril",    5: "Mai",       6: "Juin",
    7: "Juillet",  8: "Août",      9: "Septembre",
    10: "Octobre", 11: "Novembre", 12: "Décembre",
}
 
# ─────────────────────────────────────────────
# CSS global
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    hr { display: none !important; }
    .entete-page {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5cm;
    }
    .note-tableau {
        font-size: 8pt;
        font-style: italic;
        color: #555;
        margin-top: -4px;
        margin-bottom: 0;
    }
    .espaceur { margin-top: 1.5cm; }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# En-tête : titre + logo
# ─────────────────────────────────────────────
logo_html = ""
for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
    chemin_logo_complet = CHEMIN_LOGO + ext
    if os.path.exists(chemin_logo_complet):
        with open(chemin_logo_complet, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        mime = "image/png" if ext.lower() == ".png" else "image/jpeg"
        logo_html = f'<img src="data:{mime};base64,{logo_b64}" style="height:225px; margin-right:-4cm;">'
        break
 
st.markdown(f"""
<div class="entete-page">
    <h2 style="font-family: Arial, sans-serif; font-size: 48pt;
               color: #094780; font-weight: bold; margin: 0; padding: 0;
               margin-left: 1.5cm;">
        Suivi des livraisons
    </h2>
    {logo_html}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="border-top: 1px solid #cccccc; margin-top: -2cm; margin-bottom: 2,5cm;"></div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

 
# ─────────────────────────────────────────────
# Chargement des données
# ─────────────────────────────────────────────
@st.cache_data
def charger_donnees():
    df = pd.read_excel("Synthese VN 2026.xlsx", sheet_name="Marges VN")
    df["Date de Livraison"] = pd.to_datetime(df["Date de Livraison"], errors="coerce")
    df["Mois_num"] = df["Date de Livraison"].dt.month
    df["Mois_nom"] = df["Mois_num"].map(MOIS_FR)
    df["Site_nom"] = df["Site"].map(NOMS_SITES).fillna(df["Site"].astype(str))

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
# Ordre des mois
# ─────────────────────────────────────────────
mois_presents = sorted(df["Mois_num"].dropna().unique().astype(int))
mois_colonnes = [MOIS_FR[m] for m in mois_presents]
 
# ─────────────────────────────────────────────
# Fonction : afficher tableau HTML
# ─────────────────────────────────────────────
def afficher_tableau_html(df_pivot, format_fn=None, ligne_total=False):
 
    STYLE_HEADER = (
        "background-color: #094780; color: #FFFFFF; font-weight: bold; "
        "font-size: 14pt; text-align: center; padding: 6px 10px; "
        "border: 1px solid #ccc; white-space: nowrap;"
    )
    STYLE_CELL = (
        "text-align: center; font-size: 14pt; color: black; "
        "padding: 4px 10px; border: 1px solid #eee;"
    )
    STYLE_INDEX = (
        "text-align: left; font-size: 14pt; color: black; "
        "padding: 4px 10px; border: 1px solid #eee; white-space: nowrap;"
    )
    STYLE_TOTAL_CELL = (
        "text-align: center; font-size: 14pt; color: black; font-weight: bold; "
        "background-color: #E8E8E8; padding: 4px 10px; border: 1px solid #ccc;"
    )
    STYLE_TOTAL_INDEX = (
        "text-align: left; font-size: 14pt; color: black; font-weight: bold; "
        "background-color: #E8E8E8; padding: 4px 10px; border: 1px solid #ccc; white-space: nowrap;"
    )
 
    html = '<table style="border-collapse: collapse; font-family: Arial, sans-serif; margin-left: 3cm;">'
 
    # En-tête colonnes
    html += "<thead><tr>"
    html += f'<th style="{STYLE_HEADER}"></th>'
    for col in df_pivot.columns:
        html += f'<th style="{STYLE_HEADER}">{col}</th>'
    html += "</tr></thead>"
 
    # Corps
    html += "<tbody>"
    n_rows = len(df_pivot)
    for i, (idx, row) in enumerate(df_pivot.iterrows()):
        is_total = ligne_total and (i == n_rows - 1)
        s_idx  = STYLE_TOTAL_INDEX if is_total else STYLE_INDEX
        s_cell = STYLE_TOTAL_CELL  if is_total else STYLE_CELL
 
        html += f"<tr><td style='{s_idx}'>{idx}</td>"
        for val in row:
            if pd.isna(val):
                val_str = "–"
            elif format_fn:
                try:
                    val_str = format_fn(val)
                except:
                    val_str = "–"
            else:
                val_str = str(val)
            html += f"<td style='{s_cell}'>{val_str}</td>"
        html += "</tr>"
 
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# Fonctions : lignes Total / Moyenne
# ─────────────────────────────────────────────
def ajouter_total_nb(pivot):
    total = pivot.sum(numeric_only=True)
    total.name = "Total"
    return pd.concat([pivot, total.to_frame().T])
 
def ajouter_total_marge(pivot):
    moyenne = pivot.mean(numeric_only=True)
    moyenne.name = "Moyenne"
    return pd.concat([pivot, moyenne.to_frame().T])
 
# ─────────────────────────────────────────────
# Données filtrées
# ─────────────────────────────────────────────
df_livres = df.dropna(subset=["Date de Livraison"]).copy()
df_marge  = df[df["Etat"].isin(["C", "NP"])].dropna(subset=["Date de Livraison"]).copy()


 
# ─────────────────────────────────────────────
# TABLEAU 1 — Nb véhicules livrés par SITE
# ─────────────────────────────────────────────
pivot_site_nb = (
    df_livres
    .groupby(["Site_nom", "Mois_nom", "Mois_num"])["Châssis"]
    .nunique()
    .reset_index()
    .rename(columns={"Châssis": "nb"})
)
pivot_site_nb = pivot_site_nb.pivot_table(
    index="Site_nom", columns="Mois_nom", values="nb",
    aggfunc="sum", fill_value=0
)
pivot_site_nb = pivot_site_nb.reindex(
    columns=[m for m in mois_colonnes if m in pivot_site_nb.columns], fill_value=0
)
pivot_site_nb["Total"] = pivot_site_nb.sum(axis=1)
pivot_site_nb.index.name = "Site"
pivot_site_nb = ajouter_total_nb(pivot_site_nb)
 
afficher_tableau_html(
    pivot_site_nb,
    format_fn=lambda x: f"{int(x):,}".replace(",", " ") if pd.notna(x) and x != 0 else "–",
    ligne_total=True
)
 
# ─────────────────────────────────────────────
# TABLEAU 2 — Marge moyenne par SITE
# ─────────────────────────────────────────────
st.markdown('<div class="espaceur"></div>', unsafe_allow_html=True)
 
pivot_site_marge = (
    df_marge
    .groupby(["Site_nom", "Mois_nom", "Mois_num"])["Marge nette recalculée"]
    .mean()
    .reset_index()
    .rename(columns={"Marge nette recalculée": "marge_moy"})
)
pivot_site_marge = pivot_site_marge.pivot_table(
    index="Site_nom", columns="Mois_nom", values="marge_moy",
    aggfunc="mean", fill_value=None
)
pivot_site_marge = pivot_site_marge.reindex(
    columns=[m for m in mois_colonnes if m in pivot_site_marge.columns]
)


 
afficher_tableau_html(
    pivot_site_marge,
    format_fn=lambda x: f"{x:,.0f} €".replace(",", " ") if pd.notna(x) else "–",
    ligne_total=False  # ✅
)
st.markdown(
    '<p class="note-tableau" style="margin-left: 1.5cm;">* Seules les marges VN conformes (C &amp; NP) sont prises en compte '
    'dans le calcul des marges moyennes</p>',
    unsafe_allow_html=True
)
 
# ─────────────────────────────────────────────
# TABLEAU 3 — Nb véhicules livrés par MARQUE
# ─────────────────────────────────────────────
st.markdown('<div class="espaceur"></div>', unsafe_allow_html=True)
 
pivot_marque_nb = (
    df_livres
    .groupby(["Marque_nom", "Mois_nom", "Mois_num"])["Châssis"]
    .nunique()
    .reset_index()
    .rename(columns={"Châssis": "nb"})
)
pivot_marque_nb = pivot_marque_nb.pivot_table(
    index="Marque_nom", columns="Mois_nom", values="nb",
    aggfunc="sum", fill_value=0
)
pivot_marque_nb = pivot_marque_nb.reindex(
    columns=[m for m in mois_colonnes if m in pivot_marque_nb.columns], fill_value=0
)
pivot_marque_nb["Total"] = pivot_marque_nb.sum(axis=1)
pivot_marque_nb.index.name = "Marque"
pivot_marque_nb = ajouter_total_nb(pivot_marque_nb)
 
afficher_tableau_html(
    pivot_marque_nb,
    format_fn=lambda x: f"{int(x):,}".replace(",", " ") if pd.notna(x) and x != 0 else "–",
    ligne_total=True
)
 
# ─────────────────────────────────────────────
# TABLEAU 4 — Marge moyenne par MARQUE
# ─────────────────────────────────────────────
st.markdown('<div class="espaceur"></div>', unsafe_allow_html=True)
 
pivot_marque_marge = (
    df_marge
    .groupby(["Marque_nom", "Mois_nom", "Mois_num"])["Marge nette recalculée"]
    .mean()
    .reset_index()
    .rename(columns={"Marge nette recalculée": "marge_moy"})
)
pivot_marque_marge = pivot_marque_marge.pivot_table(
    index="Marque_nom", columns="Mois_nom", values="marge_moy",
    aggfunc="mean", fill_value=None
)
pivot_marque_marge = pivot_marque_marge.reindex(
    columns=[m for m in mois_colonnes if m in pivot_marque_marge.columns]
)

 
afficher_tableau_html(
    pivot_marque_marge,
    format_fn=lambda x: f"{x:,.0f} €".replace(",", " ") if pd.notna(x) else "–",
    ligne_total=False  # ✅
)
st.markdown(
    '<p class="note-tableau" style="margin-left: 1.5cm;">* Seules les marges VN conformes (C &amp; NP) sont prises en compte '
    'dans le calcul des marges moyennes</p>',
    unsafe_allow_html=True
)