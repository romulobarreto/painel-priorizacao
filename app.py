"""Painel de Priorização de Perdas - Aplicação Principal."""

import streamlit as st

from src.data.loader import load_data
from src.styles.custom import apply_custom_styles
from src.ui.analytics import render_analytics
from src.ui.filters import render_filters
from src.ui.map import render_map
from src.ui.metrics import render_metrics
from src.ui.table import render_table

# Configuração da página
st.set_page_config(
    page_title='Painel de Priorização | Equatorial',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Aplica estilos customizados
apply_custom_styles()

# --- SIDEBAR ---
with st.sidebar:
    # Container para centralizar o logo
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    
    # Logo (ajuste o width conforme necessário: 150, 180, 200, etc.)
    st.image(
        'src/assets/Logo_Grupo_Equatorial_Energia.png',
        width=600,  # Aumente esse valor para deixar maior
        use_container_width=False
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Texto colado logo abaixo
    st.markdown(
        """
        <p style='text-align: center; margin-top: -10px; 
        font-weight: 600; font-size: 11px; letter-spacing: 1px;'>
        GRUPO EQUATORIAL
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.title('📁 Configurações')

    uploaded_file = st.file_uploader(
        'Carregue o CSV do ETL',
        type='csv',
        help='Arquivo gerado pelo pipeline de alertas-regras-sinais',
    )


# --- FLUXO PRINCIPAL ---
if uploaded_file:
    df = load_data(uploaded_file)

    if df is not None:
        # --- ADICIONE ISSO AQUI ---
        # Inicializa o estado da seleção do mapa se não existir
        if 'map_selection' not in st.session_state:
            st.session_state['map_selection'] = None
        # --------------------------

        st.title('📊 Painel de Priorização de Perdas')
        st.markdown(
            'Visualize no mapa as UCs encontradas pelo sistema de '
            'alertas-regras-sinais da Regional Sul.'
        )

        # Filtros globais (afetam ambas as abas)
        df_filtered = render_filters(df)

        # Métricas dinâmicas (refletem os filtros)
        render_metrics(df_filtered)

        # Criação das Abas
        tab_mapa, tab_estatistica = st.tabs(
            ['📍 Mapa de Localização', '📈 Análise Estatística']
        )

        with tab_mapa:
            render_map(df_filtered)
            st.divider()
            render_table(df_filtered)

        with tab_estatistica:
            render_analytics(df_filtered)

else:
    st.info('👈 Arraste o arquivo CSV para a barra lateral para começar.')