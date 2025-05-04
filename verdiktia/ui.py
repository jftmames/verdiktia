from __future__ import annotations
import streamlit as st
from typing import Dict, List, Tuple

def render_inputs() -> Dict:
    st.header("Datos de tu empresa")
    return dict(
        producto = st.selectbox("Producto", ["Aceite de oliva","Vino","Fruta eco"]),
        certificaciones = st.multiselect("Certificaciones", ["BIO","IFS","BRC","D.O."]),
        preferencias_geo = st.multiselect("Preferencias geográficas", ["UE","LatAm","MENA","Asia"]),
        idiomas = st.multiselect("Idiomas en el equipo", ["Inglés","Francés","Alemán"]),
    )

def render_results(ranked: List[Tuple[str,int]]) -> None:
    st.subheader("Países recomendados")
    for nombre, score in ranked[:2]:
        st.write(f"**{nombre}** — Puntuación: {score}/500")
        st.caption(f"Nivel de confianza: {int(score/500*100)} %")
