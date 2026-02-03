"""Módulo para carregamento e validação de dados do CSV do ETL."""

import pandas as pd
import streamlit as st


def load_data(uploaded_file) -> pd.DataFrame | None:
    """
    Carrega o CSV gerado pelo pipeline de ETL.

    Trata separador brasileiro (;), decimais com vírgula e normaliza colunas.

    Args:
        uploaded_file: Arquivo CSV carregado via st.file_uploader.

    Returns:
        DataFrame com os dados carregados ou None em caso de erro.
    """
    try:
        df = pd.read_csv(
            uploaded_file,
            sep=';',
            decimal=',',
            engine='python',
            on_bad_lines='skip',
            encoding='utf-8',
        )

        # Normaliza nomes de colunas (remove espaços e aspas)
        df.columns = [
            c.strip().replace("'", '').replace('"', '') for c in df.columns
        ]

        # Validação básica: verifica se colunas essenciais existem
        required_cols = ['UC', 'PRIORIDADE', 'LATITUDE', 'LONGITUDE']
        missing = [col for col in required_cols if col not in df.columns]

        if missing:
            st.error(f'Colunas obrigatórias ausentes: {missing}')
            return None

        return df

    except Exception as e:
        st.error(f'Erro ao carregar o arquivo: {e}')
        return None
