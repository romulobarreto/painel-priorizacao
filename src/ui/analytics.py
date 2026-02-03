"""Módulo para renderização de gráficos estatísticos."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_analytics(df: pd.DataFrame) -> None:
    """
    Renderiza a aba de análise estatística com gráficos interativos.

    Args:
        df: DataFrame filtrado vindo do app principal.
    """
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")
        return

    st.write("### 📈 Visão Geral e Distribuição")

    # --- LINHA 1: Status Comercial e Prioridade por Seccional ---
    c1, c2 = st.columns(2)

    with c1:
        # 1. Total por STATUS_COMERCIAL
        status_df = df['STATUS_COMERCIAL'].value_counts().reset_index()
        status_df.columns = ['Status', 'Quantidade']
        
        fig_status = px.bar(
            status_df,
            x='Status',
            y='Quantidade',
            title='Total por Status Comercial',
            text='Quantidade',
            color_discrete_sequence=['#00d4ff']
        )
        fig_status.update_traces(textposition='outside')
        st.plotly_chart(fig_status, use_container_width=True)

    with c2:
        # 2. Prioridades por Seccional (Barras Empilhadas)
        prio_seccional = df.groupby(['SECCIONAL', 'PRIORIDADE']).size().reset_index(name='Qtd')
        
        fig_seccional = px.bar(
            prio_seccional,
            x='SECCIONAL',
            y='Qtd',
            color='PRIORIDADE',
            title='Prioridades por Seccional',
            text='Qtd',
            barmode='group',
            color_discrete_map={'P1': '#FF4B4B', 'P2': '#FFA500', 'P3': '#1E90FF'}
        )
        fig_seccional.update_traces(textposition='outside')
        st.plotly_chart(fig_seccional, use_container_width=True)

    # --- LINHA 2: Prioridade por Município (Top 15) ---
    st.write("---")
    # 3. Prioridades por Município
    prio_muni = df.groupby(['MUNICIPIO', 'PRIORIDADE']).size().reset_index(name='Qtd')
    # Pegar os top 15 municípios com mais UCs para não poluir o gráfico
    top_munis = df['MUNICIPIO'].value_counts().nlargest(15).index
    prio_muni_filtered = prio_muni[prio_muni['MUNICIPIO'].isin(top_munis)]

    fig_muni = px.bar(
        prio_muni_filtered,
        x='MUNICIPIO',
        y='Qtd',
        color='PRIORIDADE',
        title='Top 15 Municípios por Prioridade',
        text='Qtd',
        barmode='group',
        color_discrete_map={'P1': '#FF4B4B', 'P2': '#FFA500', 'P3': '#1E90FF'}
    )
    fig_muni.update_traces(textposition='outside')
    st.plotly_chart(fig_muni, use_container_width=True)

    # --- LINHA 3: Condomínio e Perímetro ---
    st.write("---")
    c3, c4 = st.columns(2)

    with c3:
        # 4. Total por Condomínio
        condo_df = df['CONDOMINIO'].value_counts().reset_index()
        condo_df.columns = ['Condomínio', 'Quantidade']
        
        fig_condo = px.bar(
            condo_df,
            x='Condomínio',
            y='Quantidade',
            title='Total por Condomínio (SIM/NÃO)',
            text='Quantidade',
            color='Condomínio',
            color_discrete_map={'SIM': '#00d4ff', 'NAO': '#343d4b'}
        )
        fig_condo.update_traces(textposition='outside')
        st.plotly_chart(fig_condo, use_container_width=True)

    with c4:
        # 5. Total por Perímetro
        perim_df = df['PERIMETRO'].value_counts().reset_index()
        perim_df.columns = ['Perímetro', 'Quantidade']
        
        fig_perim = px.bar(
            perim_df,
            x='Perímetro',
            y='Quantidade',
            title='Total por Perímetro (R/U)',
            text='Quantidade',
            color_discrete_sequence=['#00ffcc']
        )
        fig_perim.update_traces(textposition='outside')
        st.plotly_chart(fig_perim, use_container_width=True)