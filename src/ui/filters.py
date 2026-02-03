"""Componente de filtros interativos."""

import pandas as pd
import streamlit as st


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza os filtros e retorna o DataFrame filtrado.

    Args:
        df: DataFrame original com todos os dados.

    Returns:
        DataFrame filtrado de acordo com as seleções do usuário.
    """
    st.write('### 🔍 Filtros de Análise')

    # Primeira linha de filtros
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        f_prio = st.multiselect(
            'Prioridade',
            options=sorted(df['PRIORIDADE'].dropna().unique()),
            default=list(df['PRIORIDADE'].dropna().unique()),
        )

    with c2:
        f_motivo = st.multiselect(
            'Motivo Prioridade',
            options=sorted(df['MOTIVO_PRIORIDADE'].dropna().unique()),
        )

    with c3:
        f_status = st.multiselect(
            'Status', options=sorted(df['STATUS_COMERCIAL'].dropna().unique())
        )

    with c4:
        f_seccional = st.multiselect(
            'Seccional', options=sorted(df['SECCIONAL'].dropna().unique())
        )

    with c5:
        f_alimentador = st.multiselect(
            'Alimentador',
            options=sorted(df['SE_AL_NORM'].dropna().unique()),
        )

    # Segunda linha de filtros
    c5, c6, c7, c8 = st.columns(4)

    with c5:
        f_muni = st.multiselect(
            'Município', options=sorted(df['MUNICIPIO'].dropna().unique())
        )

    with c6:
        f_condo = st.selectbox('Condomínio', options=['Todos', 'SIM', 'NAO'])

    with c7:
        f_perim = st.multiselect(
            'Perímetro', options=sorted(df['PERIMETRO'].dropna().unique())
        )

    with c8:
        f_classe = st.multiselect(
            'Classe Consumo',
            options=sorted(df['CLASSE_CONSUMO'].dropna().unique()),
        )

    # Aplicação dos filtros
    df_filtered = df.copy()

    if f_prio:
        df_filtered = df_filtered[df_filtered['PRIORIDADE'].isin(f_prio)]

    if f_motivo:
        df_filtered = df_filtered[
            df_filtered['MOTIVO_PRIORIDADE'].isin(f_motivo)
        ]

    if f_motivo:
        df_filtered = df_filtered[
            df_filtered['STATUS_COMERCIAL'].isin(f_status)
        ]

    if f_seccional:
        df_filtered = df_filtered[df_filtered['SECCIONAL'].isin(f_seccional)]

    if f_alimentador:
        df_filtered = df_filtered[
            df_filtered['SE_AL_NORM'].isin(f_alimentador)
        ]

    if f_muni:
        df_filtered = df_filtered[df_filtered['MUNICIPIO'].isin(f_muni)]

    if f_condo != 'Todos':
        df_filtered = df_filtered[df_filtered['CONDOMINIO'] == f_condo]

    if f_perim:
        df_filtered = df_filtered[df_filtered['PERIMETRO'].isin(f_perim)]

    if f_classe:
        df_filtered = df_filtered[df_filtered['CLASSE_CONSUMO'].isin(f_classe)]

    return df_filtered
