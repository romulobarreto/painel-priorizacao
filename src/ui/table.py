"""Componente de tabela de detalhamento."""

import pandas as pd
import streamlit as st


def render_table(df: pd.DataFrame) -> None:
    """
    Renderiza a tabela de detalhamento das UCs.

    Args:
        df: DataFrame filtrado com as UCs.
    """
    st.write('### 📋 Detalhamento das UCs')

    # Colunas a serem exibidas
    cols_tabela = [
        'UC',
        'STATUS_COMERCIAL',
        'CLASSE_CONSUMO',
        'SE_AL_NORM',
        'MEDIDOR',
        'ANO',
        'FABRICANTE',
        'FASE',
        'MICRO_GERADOR',
        'ENDERECO',
        'CONDOMINIO',
        'PERIMETRO',
        'BAIRRO',
        'MUNICIPIO',
        'SECCIONAL',
        'CONSUMO_MEDIO',
        'PRIORIDADE',
        'MOTIVO_PRIORIDADE',
        'LATITUDE',
        'LONGITUDE'
    ]

    # Filtra apenas colunas que existem
    cols_existentes = [c for c in cols_tabela if c in df.columns]

    # Exibe a tabela
    st.dataframe(
        df[cols_existentes],
        use_container_width=True,
        height=400,
    )

    # Botão de download
    csv = df[cols_existentes].to_csv(index=False, sep=';', decimal=',')
    st.download_button(
        label='📥 Baixar Tabela Filtrada (CSV)',
        data=csv,
        file_name='ucs_priorizadas_filtradas.csv',
        mime='text/csv',
    )
