"""Módulo para renderização de gráficos estatísticos."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_analytics(df: pd.DataFrame) -> None:
    """
    Renderiza a aba de análise estatística com gráficos interativos.
    """
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")
        return

    st.write("### 📈 Visão Geral e Distribuição")

    # --- LINHA 1: Status Comercial e Prioridade por Seccional ---
    c1, c2 = st.columns(2)

    with c1:
        status_df = df['STATUS_COMERCIAL'].value_counts().reset_index()
        status_df.columns = ['Status', 'Quantidade']
        
        fig_status = px.bar(
            status_df, x='Status', y='Quantidade',
            title='Total por Status Comercial',
            text='Quantidade',
            color_discrete_sequence=['#00d4ff']
        )
        # Ajuste: Dá 15% de folga no topo do eixo Y
        max_val = status_df['Quantidade'].max()
        fig_status.update_yaxes(range=[0, max_val * 1.15])
        fig_status.update_traces(textposition='outside', texttemplate='%{text}')
        st.plotly_chart(fig_status, use_container_width=True)

    with c2:
        prio_seccional = df.groupby(['SECCIONAL', 'PRIORIDADE']).size().reset_index(name='Qtd')
        
        fig_seccional = px.bar(
            prio_seccional, x='SECCIONAL', y='Qtd', color='PRIORIDADE',
            title='Prioridades por Seccional',
            text='Qtd', barmode='group',
            color_discrete_map={'P1': '#FF4B4B', 'P2': '#FFA500', 'P3': '#1E90FF'}
        )
        # Ajuste: Folga no topo baseada no maior grupo
        max_val_prio = prio_seccional['Qtd'].max()
        fig_seccional.update_yaxes(range=[0, max_val_prio * 1.15])
        fig_seccional.update_traces(textposition='outside')
        st.plotly_chart(fig_seccional, use_container_width=True)

    # --- LINHA MOTIVOS: Motivos de Prioridade ---
    st.write("---")
    st.write("### 🎯 Detalhamento dos Motivos")
    df_prio = df[df['PRIORIDADE'].notna()].copy()
    
    if not df_prio.empty:
        motivo_df = df_prio.groupby(['MOTIVO_PRIORIDADE', 'PRIORIDADE']).size().reset_index(name='Quantidade')
        motivo_df = motivo_df.sort_values('Quantidade', ascending=True)

        fig_motivo = px.bar(
            motivo_df, y='MOTIVO_PRIORIDADE', x='Quantidade', color='PRIORIDADE',
            orientation='h', title='Quantidade Total por Motivo de Prioridade',
            text='Quantidade',
            color_discrete_map={'P1': '#FF4B4B', 'P2': '#FFA500', 'P3': '#1E90FF'}
        )
        # No gráfico horizontal, a folga é no eixo X
        max_val_motivo = motivo_df['Quantidade'].max()
        fig_motivo.update_xaxes(range=[0, max_val_motivo * 1.20]) # 20% de folga no X
        fig_motivo.update_traces(textposition='outside')
        fig_motivo.update_layout(margin=dict(l=200)) 
        st.plotly_chart(fig_motivo, use_container_width=True)

    # --- LINHA 2: Prioridade por Município (Top 15) ---
    st.write("---")
    prio_muni = df.groupby(['MUNICIPIO', 'PRIORIDADE']).size().reset_index(name='Qtd')
    top_munis = df['MUNICIPIO'].value_counts().nlargest(15).index
    prio_muni_filtered = prio_muni[prio_muni['MUNICIPIO'].isin(top_munis)]

    fig_muni = px.bar(
        prio_muni_filtered, x='MUNICIPIO', y='Qtd', color='PRIORIDADE',
        title='Top 15 Municípios por Prioridade',
        text='Qtd', barmode='group',
        color_discrete_map={'P1': '#FF4B4B', 'P2': '#FFA500', 'P3': '#1E90FF'}
    )
    # Ajuste: Folga no topo
    max_val_muni = prio_muni_filtered['Qtd'].max()
    fig_muni.update_yaxes(range=[0, max_val_muni * 1.15])
    fig_muni.update_traces(textposition='outside')
    st.plotly_chart(fig_muni, use_container_width=True)

    # --- LINHA 3: Condomínio e Perímetro ---
    st.write("---")
    c3, c4 = st.columns(2)

    with c3:
        condo_df = df['CONDOMINIO'].value_counts().reset_index()
        condo_df.columns = ['Condomínio', 'Quantidade']
        fig_condo = px.bar(
            condo_df, x='Condomínio', y='Quantidade',
            title='Total por Condomínio (SIM/NÃO)',
            text='Quantidade', color='Condomínio',
            color_discrete_map={'SIM': '#00d4ff', 'NAO': '#343d4b'}
        )
        max_val_condo = condo_df['Quantidade'].max()
        fig_condo.update_yaxes(range=[0, max_val_condo * 1.15])
        fig_condo.update_traces(textposition='outside')
        st.plotly_chart(fig_condo, use_container_width=True)

    with c4:
        perim_df = df['PERIMETRO'].value_counts().reset_index()
        perim_df.columns = ['Perímetro', 'Quantidade']
        fig_perim = px.bar(
            perim_df, x='Perímetro', y='Quantidade',
            title='Total por Perímetro (R/U)',
            text='Quantidade',
            color_discrete_sequence=['#00ffcc']
        )
        max_val_perim = perim_df['Quantidade'].max()
        fig_perim.update_yaxes(range=[0, max_val_perim * 1.15])
        fig_perim.update_traces(textposition='outside')
        st.plotly_chart(fig_perim, use_container_width=True)