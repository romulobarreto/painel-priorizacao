"""Estilos customizados para o painel."""

import streamlit as st


def apply_custom_styles() -> None:
    """Aplica CSS customizado para temas dark e light."""
    st.markdown(
        """
        <style>
        /* ===== SIDEBAR: Remove padding superior ===== */
        section[data-testid="stSidebar"] {
            padding-top: 0rem !important;
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem !important;
        }

        /* ===== CONTAINER DO LOGO + TEXTO ===== */
        .sidebar-header {
            position: relative;
            text-align: center;
            margin-top: 0;
            margin-bottom: 20px;
        }

        .sidebar-header img {
            display: block;
            margin: 0 auto;
            width: 70%;
            max-width: 180px;
        }

        .sidebar-header p {
            margin-top: 5px;
            margin-bottom: 0;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.8px;
            color: var(--text-color);
        }

        /* ===== LABELS DOS FILTROS (modo light e dark) ===== */
        label[data-testid="stWidgetLabel"] {
            color: inherit !important;
            font-weight: 500 !important;
        }

        /* ===== FILTROS: Background adaptativo ===== */
        .stMultiSelect div[data-baseweb="select"],
        .stSelectbox div[data-baseweb="select"] {
            background-color: var(--secondary-background-color) !important;
        }

        /* ===== TEXTO DENTRO DOS FILTROS ===== */
        .stMultiSelect span,
        .stSelectbox span {
            color: var(--text-color) !important;
        }

        /* ===== LEGENDA DO MAPA: Barra de fundo ===== */
        .map-legend {
            display: flex;
            gap: 25px;
            justify-content: center;
            background-color: var(--secondary-background-color);
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 1px solid var(--border-color);
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 15px;
            font-weight: 600;
            color: var(--text-color);
        }

        /* ===== DIVISORES ===== */
        hr {
            margin-top: 1rem;
            margin-bottom: 1rem;
            border-color: var(--border-color);
        }

        /* ===== VARIÁVEIS DE COR (fallback) ===== */
        :root {
            --border-color: #343d4b;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )