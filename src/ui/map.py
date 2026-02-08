# src/ui/map.py
"""Componente de mapa interativo."""

from typing import Any, Dict, List, Optional, Tuple

import folium
import math
import pandas as pd
import streamlit as st
from folium.plugins import Draw, MarkerCluster
from streamlit_folium import st_folium


def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância Haversine entre dois pontos em metros."""
    R = 6371000  # radius Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def point_in_polygon(lat: float, lon: float, polygon: List[Tuple[float, float]]) -> bool:
    """
    Testa se um ponto (lat, lon) está dentro de um polígono (lista de (lat, lon)).
    Algoritmo ray-casting (não precisa de shapely).
    """
    inside = False
    n = len(polygon)
    if n == 0:
        return False
    j = n - 1
    for i in range(n):
        yi, xi = polygon[i]  # lat, lon
        yj, xj = polygon[j]
        intersect = ((xi > lon) != (xj > lon)) and (
            lat < (yj - yi) * (lon - xi) / (xj - xi + 1e-15) + yi
        )
        if intersect:
            inside = not inside
        j = i
    return inside


def _normalize_last_drawn(ret: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Retorna a última feição desenhada no formato geojson se existir.
    Trata variações do retorno do st_folium.
    """
    if not ret:
        return None
    for key in ("last_drawn_feature", "last_active_drawing", "last_draw"):
        if key in ret and ret[key]:
            return ret[key]
    if "all_drawings" in ret and ret["all_drawings"]:
        return ret["all_drawings"][-1]
    # fallback: se houver 'features' em geojson
    if "features" in ret and ret["features"]:
        return ret["features"][-1]
    return None


def _extract_geom_coords(geom: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Normaliza a geometria de várias formas possíveis retornadas pelo Draw/st_folium.
    Retorna dict com keys:
    - 'type': 'polygon' | 'bbox' | 'circle' | 'point'
    - 'coords': list of (lon, lat) or (lat, lon) depending on consumer
    - 'center': (lat, lon) for circle/point
    - 'radius': radius in meters (for circle) if available
    """
    if not geom:
        return None

    g = geom
    # se veio como Feature com geometry
    if "geometry" in g:
        g = g["geometry"]

    gtype = g.get("type")
    coords = g.get("coordinates")

    # Polygon: coords = [[[lon, lat], ...]]
    if gtype and gtype.lower() == "polygon" and coords:
        ring = coords[0]
        # convert to list of (lat, lon)
        poly = [(pt[1], pt[0]) for pt in ring]
        return {"type": "polygon", "poly": poly}

    # Point (pode vir com radius nas properties -> circle)
    if gtype and gtype.lower() == "point" and coords:
        lon, lat = coords[0], coords[1] if isinstance(coords[0], list) else (coords[0], coords[1])
        return {"type": "point", "center": (float(lat), float(lon))}

    # Alguns Draws retornam Feature com properties.radius e geometry.coordinates como [lon, lat]
    # ou retornam como Feature com properties: {'radius': x} e geometry: {'type': 'Point', 'coordinates':[lon,lat]}
    prop = geom.get("properties", {}) or {}
    if prop:
        # Circle com center + radius
        if "radius" in prop:
            radius = float(prop["radius"])
            # try coordinates in geom or prop
            if coords:
                # if polygon-like coords for circle, fallback to center = first coordinate
                if isinstance(coords, list) and len(coords) >= 2 and isinstance(coords[0], (int, float)):
                    lon = coords[0]
                    lat = coords[1]
                    return {"type": "circle", "center": (float(lat), float(lon)), "radius": radius}
                # polygon-like (some draw versions approximate circle as polygon)
                if isinstance(coords, list) and isinstance(coords[0], list):
                    # take centroid approximate
                    pts = coords[0]
                    lons = [pt[0] for pt in pts]
                    lats = [pt[1] for pt in pts]
                    center_lat = sum(lats) / len(lats)
                    center_lon = sum(lons) / len(lons)
                    return {"type": "circle", "center": (float(center_lat), float(center_lon)), "radius": radius}
    # If coords looks like bbox (e.g., polygon rectangle), try to treat as polygon above
    if gtype and gtype.lower() == "featurecollection":
        # pega primeira feature
        features = geom.get("features") or []
        if features:
            return _extract_geom_coords(features[-1].get("geometry", features[-1]))
    return None


def render_map(df: pd.DataFrame) -> None:
    """
    Renderiza o mapa de calor com as UCs priorizadas e grava seleção em st.session_state['map_selection'].

    A seleção pode ser:
    - {'type': 'bbox'|'polygon', 'bounds': (min_lat, min_lon, max_lat, max_lon), 'selected_uc_list': [...]}
    - {'type': 'click', 'lat': ..., 'lon': ..., 'radius_m': ..., 'selected_uc_list': [...]}
    - {'type': 'circle', 'center': (lat, lon), 'radius': meters, 'selected_uc_list': [...]}
    """
    st.write("### 📍 Localização das UCs Priorizadas")

    # Legenda HTML
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

    # Botão para limpar seleção do mapa com callback (on_click provoca rerun automaticamente)
    def _clear_map():
        st.session_state.pop("map_selection", None)
        st.session_state["ignore_map"] = False

    st.button("Limpar seleção do mapa", on_click=_clear_map)

    # Data sanity
    if "LATITUDE" not in df.columns or "LONGITUDE" not in df.columns:
        st.warning("As colunas 'LATITUDE' e 'LONGITUDE' não foram encontradas.")
        return

    df_map = df.dropna(subset=["LATITUDE", "LONGITUDE"]).copy()
    if df_map.empty:
        st.warning("Nenhuma UC com coordenadas válidas para exibir no mapa.")
        return

    # garante tipos float
    df_map["LATITUDE"] = df_map["LATITUDE"].astype(float)
    df_map["LONGITUDE"] = df_map["LONGITUDE"].astype(float)

    center_lat = float(df_map["LATITUDE"].mean())
    center_lon = float(df_map["LONGITUDE"].mean())

    # Cria mapa e adiciona plugin Draw
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    draw = Draw(
        export=False,
        draw_options={
            "polyline": False,
            "rectangle": True,
            "circle": True,
            "marker": False,
            "polygon": True,
        },
        edit_options={"edit": True},
    )
    draw.add_to(m)

    marker_cluster = MarkerCluster().add_to(m)
    color_map = {"P1": "red", "P2": "orange", "P3": "blue"}

    # Limitação de pontos para performance
    max_points = 5000
    if len(df_map) > max_points:
        st.info(f"Exibindo {max_points} de {len(df_map)} UCs (ordenadas por prioridade).")
        df_map = df_map.sort_values("PRIORIDADE").head(max_points)

    for _, row in df_map.iterrows():
        folium.CircleMarker(
            location=[row["LATITUDE"], row["LONGITUDE"]],
            radius=6,
            color=color_map.get(row.get("PRIORIDADE"), "gray"),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>UC:</b> {row.get('UC')}<br>"
                f"<b>Prioridade:</b> {row.get('PRIORIDADE')}<br>"
                f"<b>Motivo:</b> {row.get('MOTIVO_PRIORIDADE')}",
                max_width=300,
            ),
        ).add_to(marker_cluster)

    # Renderiza o mapa e captura retorno (cliques + desenhos)
    ret = st_folium(m, width="100%", height=600)

    # Processa clique do usuário no mapa (retorna coords)
    last_clicked = ret.get("last_clicked") if isinstance(ret, dict) else None
    if last_clicked:
        lat = last_clicked.get("lat") or last_clicked.get("latitude") or last_clicked.get("y")
        lon = last_clicked.get("lng") or last_clicked.get("longitude") or last_clicked.get("x")
        try:
            lat = float(lat)
            lon = float(lon)
            # raio por clique (sidebar) - o usuário pode ajustar
            radius_m = st.sidebar.number_input(
                "Raio de seleção por clique (m)", min_value=50, max_value=2000, value=200, step=50
            )
            df_map["__dist_m"] = df_map.apply(
                lambda r: haversine_meters(lat, lon, float(r["LATITUDE"]), float(r["LONGITUDE"])), axis=1
            )
            sel = df_map[df_map["__dist_m"] <= radius_m]
            if sel.empty:
                nearest = df_map.loc[df_map["__dist_m"].idxmin()]
                sel_list = [nearest.get("UC")]
                st.info(f"Nenhuma UC dentro de {radius_m}m — selecionando UC mais próxima: {nearest.get('UC')}")
            else:
                sel_list = sel["UC"].tolist()
                st.info(f"Selecionadas {len(sel_list)} UCs dentro de {radius_m}m do clique.")
            st.session_state["map_selection"] = {
                "type": "click",
                "lat": lat,
                "lon": lon,
                "radius_m": radius_m,
                "selected_uc_list": sel_list,
            }
        except Exception:
            # ignora parsing errors
            pass

    # Processa desenho (retângulo/polígono/circle)
    drawn = _normalize_last_drawn(ret)
    if drawn:
        # tenta extrair geom normalizado
        geom_info = _extract_geom_coords(drawn)
        if geom_info:
            gtype = geom_info.get("type")
            if gtype == "polygon":
                poly = geom_info.get("poly", [])
                # bounding box para filtro rápido
                lats = [p[0] for p in poly]
                lons = [p[1] for p in poly]
                min_lat, max_lat = min(lats), max(lats)
                min_lon, max_lon = min(lons), max(lons)
                candidate = df_map[
                    (df_map["LATITUDE"] >= min_lat)
                    & (df_map["LATITUDE"] <= max_lat)
                    & (df_map["LONGITUDE"] >= min_lon)
                    & (df_map["LONGITUDE"] <= max_lon)
                ]
                # filtra verdadeiramente por polígono com point_in_polygon
                sel = []
                for _, r in candidate.iterrows():
                    if point_in_polygon(float(r["LATITUDE"]), float(r["LONGITUDE"]), poly):
                        sel.append(r["UC"])
                st.session_state["map_selection"] = {
                    "type": "bbox",
                    "bounds": (min_lat, min_lon, max_lat, max_lon),
                    "selected_uc_list": sel,
                }
                st.info(f"Selecionadas {len(sel)} UCs dentro da área desenhada.")
            elif gtype == "circle":
                center = geom_info.get("center")
                radius = geom_info.get("radius", 200.0)
                if center:
                    latc, lonc = center
                    df_map["__dist_m"] = df_map.apply(
                        lambda r: haversine_meters(latc, lonc, float(r["LATITUDE"]), float(r["LONGITUDE"])), axis=1
                    )
                    sel = df_map[df_map["__dist_m"] <= float(radius)]
                    sel_list = sel["UC"].tolist()
                    st.session_state["map_selection"] = {
                        "type": "circle",
                        "center": (latc, lonc),
                        "radius": float(radius),
                        "selected_uc_list": sel_list,
                    }
                    st.info(f"Selecionadas {len(sel_list)} UCs dentro do círculo desenhado.")
            elif gtype == "point":
                # fallback: caso draw tenha criado apenas um point (sem radius), tratamos como click
                center = geom_info.get("center")
                if center:
                    latc, lonc = center
                    radius_m = st.sidebar.number_input("Raio de seleção por clique (m)", min_value=50, max_value=2000, value=200, step=50)
                    df_map["__dist_m"] = df_map.apply(
                        lambda r: haversine_meters(latc, lonc, float(r["LATITUDE"]), float(r["LONGITUDE"])), axis=1
                    )
                    sel = df_map[df_map["__dist_m"] <= radius_m]
                    sel_list = sel["UC"].tolist() if not sel.empty else []
                    st.session_state["map_selection"] = {
                        "type": "click",
                        "lat": latc,
                        "lon": lonc,
                        "radius_m": radius_m,
                        "selected_uc_list": sel_list,
                    }
                    st.info(f"Selecionadas {len(sel_list)} UCs pelo point draw.")
        # sem erro, a mera existência de drawn atualiza session_state (sem experimental_rerun)

    # Mostra info sobre a seleção atual na sidebar (ou vazio)
    sel = st.session_state.get("map_selection")
    if sel:
        sel_type = sel.get("type")
        if sel_type == "click":
            st.sidebar.write(f"Selecionadas (click): {len(sel.get('selected_uc_list', []))} UCs")
        elif sel_type == "circle":
            st.sidebar.write(f"Selecionadas (círculo): {len(sel.get('selected_uc_list', []))} UCs")
        else:
            st.sidebar.write(f"Selecionadas (área): {len(sel.get('selected_uc_list', []))} UCs")
    else:
        st.sidebar.write("Nenhuma seleção do mapa ativa.")