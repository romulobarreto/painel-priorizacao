"""Componente de métricas do painel."""

import pandas as pd
import streamlit as st


def render_metrics(df: pd.DataFrame) -> None:
    """
    Renderiza as métricas principais no cabeçalho.

    Args:
        df: DataFrame com os dados filtrados.
    """
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric('Total de UCs', f'{len(df):,}')

    with m2:
        st.metric('Municípios', df['MUNICIPIO'].nunique())

    with m3:
        p1_count = len(df[df['PRIORIDADE'] == 'P1'])
        st.metric('Prioridade P1', p1_count, delta_color='inverse')

    with m4:
        p2_count = len(df[df['PRIORIDADE'] == 'P2'])
        st.metric('Prioridade P2', p2_count)

    with m5:
        p3_count = len(df[df['PRIORIDADE'] == 'P3'])
        st.metric('Prioridade P3', p3_count)
