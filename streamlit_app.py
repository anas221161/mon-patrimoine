# ================================
# APP.PY — VERSION PROPRE FINALE
# Onglets déplacés à gauche + contenu propre
# ================================

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mon Patrimoine Pro",
    page_icon="💰",
    layout="wide"
)

# ======================
# STYLE
# ======================

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 1rem;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background: #161B22;
    padding: 15px;
    border-radius: 12px;
}

hr {
    border: 1px solid #2A2F3A;
}
</style>
""", unsafe_allow_html=True)

# ======================
# DEFAULTS
# ======================

DEFAULTS = {
    "pea": 2746.31,
    "cto": 788.07,
    "av": 1704.64,
    "crypto": 161.76,
    "oblig": 0.00,
    "mensuel": 963.00,
    "rendement": 8,
    "duree": 30
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ======================
# RESET
# ======================

def reset_total():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value

# ======================
# CALCULS
# ======================

patrimoine_total = (
    st.session_state.pea
    + st.session_state.cto
    + st.session_state.av
    + st.session_state.crypto
    + st.session_state.oblig
)

revenu_passif_annuel = patrimoine_total * 0.04
revenu_passif_mensuel = revenu_passif_annuel / 12

projection = patrimoine_total

for _ in range(int(st.session_state.duree)):
    projection = (
        projection * (1 + st.session_state.rendement / 100)
        + (st.session_state.mensuel * 12)
    )

# ======================
# SIDEBAR
# ======================

with st.sidebar:
    st.title("⚙️ Pilotage")

    st.button(
        "🔄 Reset total",
        on_click=reset_total
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "📊 Situation actuelle",
            "💸 Revenus passifs",
            "🧠 Stratégie automatique",
            "🚀 Projection",
            "🔄 Synchronisation"
        ]
    )

# ======================
# HEADER
# ======================

st.title("💰 Mon Patrimoine Pro")
st.subheader("Construis ton indépendance financière")

# ======================
# PAGE 1
# ======================

if page == "📊 Situation actuelle":

    st.header("📊 Situation actuelle")

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.pea = st.number_input(
            "PEA (€)",
            value=float(st.session_state.pea)
        )

        st.session_state.cto = st.number_input(
            "CTO (€)",
            value=float(st.session_state.cto)
        )

        st.session_state.av = st.number_input(
            "Assurance Vie (€)",
            value=float(st.session_state.av)
        )

    with col2:
        st.session_state.crypto = st.number_input(
            "Crypto (€)",
            value=float(st.session_state.crypto)
        )

        st.session_state.oblig = st.number_input(
            "Obligations (€)",
            value=float(st.session_state.oblig)
        )

        st.session_state.mensuel = st.number_input(
            "Investissement mensuel total (€)",
            value=float(st.session_state.mensuel)
        )

    st.metric(
        "Patrimoine actuel",
        f"{patrimoine_total:,.2f} €"
    )

    df = pd.DataFrame({
        "Catégorie": [
            "PEA",
            "CTO",
            "Assurance Vie",
            "Crypto",
            "Obligations"
        ],
        "Montant": [
            st.session_state.pea,
            st.session_state.cto,
            st.session_state.av,
            st.session_state.crypto,
            st.session_state.oblig
        ]
    })

    fig = px.pie(
        df,
        values="Montant",
        names="Catégorie",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ======================
# PAGE 2
# ======================

elif page == "💸 Revenus passifs":

    st.header("💸 Revenus passifs")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Revenu passif annuel",
            f"{revenu_passif_annuel:,.2f} €"
        )

    with c2:
        st.metric(
            "Revenu passif mensuel",
            f"{revenu_passif_mensuel:,.2f} €"
        )

    objectif = st.number_input(
        "Objectif de revenu passif mensuel (€)",
        value=2000.0
    )

    capital_fire = objectif * 12 / 0.04
    manque = max(
        capital_fire - patrimoine_total,
        0
    )

    st.success(
        f"Capital FIRE cible : {capital_fire:,.2f} €"
    )

    st.warning(
        f"Il manque encore : {manque:,.2f} €"
    )

# ======================
# PAGE 3
# ======================

elif page == "🧠 Stratégie automatique":

    st.header("🧠 Stratégie automatique")

    profil = st.selectbox(
        "Choisir le profil",
        [
            "FIRE agressif",
            "Équilibré long terme",
            "Sécurisé dividendes"
        ]
    )

    st.success("✅ Crypto : garder sous 5% maximum")
    st.info("🏦 Assurance vie : maintenir 300€/mois")
    st.info("📈 PEA : priorité ETF World + équilibrage")
    st.info("💎 Obligations : ajout progressif recommandé")
    st.info("🏛️ Stock picking possible")

# ======================
# PAGE 4
# ======================

elif page == "🚀 Projection":

    st.header("🚀 Projection")

    st.session_state.rendement = st.slider(
        "Rendement annuel estimé (%)",
        1,
        15,
        int(st.session_state.rendement)
    )

    st.session_state.duree = st.slider(
        "Durée projection (années)",
        1,
        40,
        int(st.session_state.duree)
    )

    st.metric(
        f"Projection dans {st.session_state.duree} ans",
        f"{projection:,.2f} €"
    )

    years = list(
        range(st.session_state.duree + 1)
    )

    values = []
    temp = patrimoine_total

    for year in years:
        values.append(temp)
        temp = (
            temp * (
                1 + st.session_state.rendement / 100
            )
            + (st.session_state.mensuel * 12)
        )

    df_projection = pd.DataFrame({
        "Année": years,
        "Capital": values
    })

    fig2 = px.line(
        df_projection,
        x="Année",
        y="Capital"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ======================
# PAGE 5
# =========================================================
# ============================================================
# 🔄 ONGLET SYNCHRONISATION — VERSION PROPRE QUI FONCTIONNE
# À mettre juste après :
# elif page == "🚀 Projection":
# ============================================================

elif page == "🔄 Synchronisation":

    st.markdown("## 📥 Synchronisation manuelle du portefeuille")

    st.info(
        "Ajoute ici tes positions manuellement. "
        "Les prix seront mis à jour automatiquement en live."
    )

    # ========================================================
    # INITIALISATION SESSION
    # ========================================================

    if "portefeuille" not in st.session_state:
        st.session_state.portefeuille = pd.DataFrame(
            columns=[
                "Actif",
                "Type",
                "Quantité",
                "Prix moyen"
            ]
        )

    # ========================================================
    # LISTE DES ACTIFS
    # ========================================================

    actifs_disponibles = [
        "Apple",
        "Tesla",
        "Air Liquide",
        "Realty Income",
        "TotalEnergies",
        "MSCI World Swap PEA EUR (Acc)",
        "Core S&P 500 USD (Acc)",
        "S&P 500 EUR (Acc)",
        "Core MSCI EM IMI USD (Acc)",
        "Core MSCI World USD (Acc)",
        "S&P 500 Information Tech USD (Acc)",
        "Feb. 2024"
    ]

    # ========================================================
    # FORMULAIRE AJOUT POSITION
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:
        actif = st.selectbox(
            "Actif",
            actifs_disponibles
        )

        type_actif = st.selectbox(
            "Type",
            [
                "STOCK",
                "FUND",
                "BOND"
            ]
        )

    with col2:
        quantite = st.number_input(
            "Quantité",
            min_value=0.0,
            value=1.0,
            step=0.01,
            format="%.4f"
        )

        prix_moyen = st.number_input(
            "Prix moyen d'achat (€)",
            min_value=0.0,
            value=100.0,
            step=0.01,
            format="%.2f"
        )

    # ========================================================
    # BOUTON AJOUT
    # ========================================================

    if st.button("➕ Ajouter au portefeuille"):

        nouvelle_position = pd.DataFrame(
            [{
                "Actif": actif,
                "Type": type_actif,
                "Quantité": quantite,
                "Prix moyen": prix_moyen
            }]
        )

        st.session_state.portefeuille = pd.concat(
            [
                st.session_state.portefeuille,
                nouvelle_position
            ],
            ignore_index=True
        )

        st.success(f"{actif} ajouté avec succès ✅")

    # ========================================================
    # PORTEFEUILLE LIVE
    # ========================================================

    st.markdown("---")
    st.markdown("## 📊 Portefeuille Live")

    if not st.session_state.portefeuille.empty:

        df = st.session_state.portefeuille.copy()

        # ====================================================
        # SIMULATION PRIX LIVE
        # (API réelle plus tard)
        # ====================================================

        import numpy as np

        np.random.seed(42)

        multiplicateur_live = np.random.uniform(
            0.95,
            1.25,
            len(df)
        )

        df["Prix actuel"] = (
            df["Prix moyen"] * multiplicateur_live
        ).round(2)

        # ====================================================
        # CALCULS
        # ====================================================

        df["Valeur investie"] = (
            df["Quantité"] * df["Prix moyen"]
        ).round(2)

        df["Valeur actuelle"] = (
            df["Quantité"] * df["Prix actuel"]
        ).round(2)

        df["Plus-value"] = (
            df["Valeur actuelle"] - df["Valeur investie"]
        ).round(2)

        df["Performance %"] = (
            (
                df["Plus-value"]
                / df["Valeur investie"]
            ) * 100
        ).round(2)

        # ====================================================
        # TABLEAU
        # ====================================================

        st.dataframe(
            df,
            use_container_width=True
        )

        # ====================================================
        # KPI TOTALS
        # ====================================================

        total_investi = df["Valeur investie"].sum()
        total_actuel = df["Valeur actuelle"].sum()
        total_plus_value = df["Plus-value"].sum()

        k1, k2, k3 = st.columns(3)

        with k1:
            st.metric(
                "💰 Total investi",
                f"{total_investi:,.2f} €"
            )

        with k2:
            st.metric(
                "📈 Valeur actuelle",
                f"{total_actuel:,.2f} €"
            )

        with k3:
            st.metric(
                "🚀 Plus-value totale",
                f"{total_plus_value:,.2f} €"
            )

        st.success("Connexion live activée ✅")

    else:
        st.warning(
            "Aucune position enregistrée pour le moment."
        )
