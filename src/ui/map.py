"""Componente de mapa interativo."""

import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


def render_map(df: pd.DataFrame) -> None:
    """
    Renderiza o mapa de calor com as UCs priorizadas.

    Args:
        df: DataFrame filtrado com as UCs a serem plotadas.
    """
    st.write('### 📍 Localização das UCs Priorizadas')

    # Legenda HTML com barra de fundo
    st.markdown(
        """
        <div class="map-legend">
            <div class="legend-item">
                <span style="color: #FF4B4B; font-size: 20px;">●</span>
                <span>P1 (Alerta)</span>
            </div>
            <div class="legend-item">
                <span style="color: #FFA500; font-size: 20px;">●</span>
                <span>P2 (Regra)</span>
            </div>
            <div class="legend-item">
                <span style="color: #1E90FF; font-size: 20px;">●</span>
                <span>P3 (Sinal)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Remove linhas sem coordenadas
    df_map = df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()

    if len(df_map) == 0:
        st.warning('Nenhuma UC com coordenadas válidas para exibir no mapa.')
        return

    # Calcula centro do mapa
    center_lat = df_map['LATITUDE'].mean()
    center_lon = df_map['LONGITUDE'].mean()

    # Cria o mapa
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(m)

    # Mapeamento de cores
    color_map = {'P1': 'red', 'P2': 'orange', 'P3': 'blue'}

    # Limita a 5000 pontos para performance
    max_points = 5000
    if len(df_map) > max_points:
        st.info(
            f'Exibindo {max_points} de {len(df_map)} UCs '
            f'(ordenadas por prioridade).'
        )
        # Prioriza P1 > P2 > P3
        df_map = df_map.sort_values('PRIORIDADE').head(max_points)

    # Plota os marcadores
    for _, row in df_map.iterrows():
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=6,
            color=color_map.get(row['PRIORIDADE'], 'gray'),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>UC:</b> {row['UC']}<br>"
                f"<b>Prioridade:</b> {row['PRIORIDADE']}<br>"
                f"<b>Motivo:</b> {row['MOTIVO_PRIORIDADE']}",
                max_width=300,
            ),
        ).add_to(marker_cluster)

    # Renderiza o mapa
    st_folium(m, width='100%', height=500)