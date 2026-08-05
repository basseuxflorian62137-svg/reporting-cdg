import sys
import os
import io
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import pandas as pd

from extraction     import creer_export_simule, charger_donnees, get_taux_eur_usd
from transformation import transformer_donnees, agreger_par_site, agreger_par_marque
from reporting      import generer_reporting
from notification   import envoyer_notification

# ✅ Forcer l'encodage UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def sauvegarder_pour_dashboard(df_transforme, df_site, df_marque, taux_eur_usd):
    """Sauvegarde les données pour le dashboard Streamlit"""

    chemin_csv  = "C:/Users/florian/pandas_project/data/output/data_dashboard.csv"
    chemin_meta = "C:/Users/florian/pandas_project/data/output/metadata.json"

    # Sauvegarder les données détaillées
    df_transforme.to_csv(chemin_csv, index=False)

    # Sauvegarder les métadonnées
    metadata = {
        "derniere_maj":    datetime.now().strftime("%d/%m/%Y %H:%M"),
        "nb_lignes":       len(df_transforme),
        "nb_sites":        df_transforme["site"].nunique(),
        "nb_marques":      df_transforme["marque"].nunique(),
        "ca_reel_total":   int(df_transforme["ca_reel"].sum()),
        "ca_budget_total": int(df_transforme["ca_budget"].sum()),
        "ecart_total":     int(df_transforme["ecart_valeur"].sum()),
        "taux_eur_usd":    taux_eur_usd
    }

    with open(chemin_meta, "w") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    print("✅ Données dashboard sauvegardées")

def lancer_pipeline():
    print("=" * 50)
    print(f"🚀 PIPELINE CDG — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)

    try:
        # Étape 1 — Extraction
        print("\n📥 ÉTAPE 1 — Extraction des données")
        chemin  = creer_export_simule()
        df_brut = charger_donnees(chemin)

        # Étape 2 — Transformation
        print("\n🔄 ÉTAPE 2 — Transformation")
        df_transforme = transformer_donnees(df_brut)
        df_site       = agreger_par_site(df_transforme)
        df_marque     = agreger_par_marque(df_transforme)

        # Étape 3 — Enrichissement taux de change
        print("\n💱 ÉTAPE 3 — Enrichissement taux de change")
        taux_eur_usd = get_taux_eur_usd()
        df_transforme["ca_reel_usd"] = round(df_transforme["ca_reel"] * taux_eur_usd, 0)
        print(f"✅ Colonne ca_reel_usd ajoutée — taux utilisé : {taux_eur_usd}")

        # Étape 4 — Reporting Excel
        print("\n📊 ÉTAPE 4 — Génération du reporting")
        chemin_rapport = generer_reporting(df_transforme, df_site, df_marque)

        # Étape 5 — Sauvegarde pour dashboard
        print("\n💾 ÉTAPE 5 — Sauvegarde pour dashboard")
        sauvegarder_pour_dashboard(df_transforme, df_site, df_marque, taux_eur_usd)

        # Étape 6 — Notification e-mail
        print("\n📧 ÉTAPE 6 — Notification e-mail")
        envoyer_notification(df_transforme, df_site, chemin_rapport)

        # Récapitulatif
        print("\n" + "=" * 50)
        print("✅ PIPELINE TERMINÉ AVEC SUCCÈS !")
        print(f"📊 {len(df_transforme)} lignes traitées")
        print(f"🏢 {df_transforme['site'].nunique()} sites analysés")
        print(f"🚗 {df_transforme['marque'].nunique()} marques analysées")
        print(f"💱 Taux EUR/USD : {taux_eur_usd}")
        print(f"💾 Reporting : {chemin_rapport}")
        print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ ERREUR PIPELINE : {e}")
        raise

if __name__ == "__main__":
    lancer_pipeline()