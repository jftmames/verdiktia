from __future__ import annotations
import streamlit as st
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

def render_inputs() -> Dict[str, any]:
    st.header("Datos de tu empresa")
    return dict(
        producto          = st.selectbox("Producto", ["Aceite de oliva", "Vino", "Fruta eco"]),
        certificaciones   = st.multiselect("Certificaciones", ["BIO", "IFS", "BRC", "D.O."]),
        preferencias_geo  = st.multiselect("Preferencias geográficas", ["UE", "LatAm", "MENA", "Asia"]),
        idiomas           = st.multiselect("Idiomas en el equipo", ["Inglés", "Francés", "Alemán"]),
    )

def render_weights() -> Dict[str, int]:
    st.subheader("Ajusta la importancia de cada factor")
    default = yaml.safe_load(Path("config.yaml").read_text())["weights"]
    weights: Dict[str, int] = {}
    for key, val in default.items():
        weights[key] = st.slider(
            label=key.replace('_', ' ').capitalize(),
            min_value=0,
            max_value=50,
            value=val,
            help=f"Peso de '{key}' en el cálculo"
        )
    return weights

def render_results(ranked: List[Tuple[str, int]]) -> None:
    st.subheader("Países recomendados")
    for nombre, score in ranked[:2]:
        st.write(f"**{nombre}** — Puntuación: {score}/500")
        st.caption(f"Nivel de confianza: {int(score/500*100)} %")

# verdiktia/ui.py (añadir al final)

from typing import Dict, List

def render_canvas(subquestions: Dict[str, List[str]]) -> None:
    st.subheader("Diagnóstico Inicial (Canvas)")
    for root, subs in subquestions.items():
        with st.expander(root):
            for i, sq in enumerate(subs, 1):
                st.markdown(f"**{i}.** {sq}")
            st.text_input(f"Responde aquí sobre «{root}»", key=f"resp_{root}")
# en verdiktia/ui.py (al final del módulo)

from graphviz import Digraph
from typing import Dict, List

def render_reasoning_graph(subquestions: Dict[str, List[str]]) -> None:
    """
    Dibuja un grafo dirigido donde cada pregunta raíz conecta
    con sus sub-preguntas.
    """
    dot = Digraph(
        name="ReasoningGraph",
        format="svg",
        graph_attr={"rankdir": "LR", "splines": "ortho"}
    )
    # crea nodos y aristas
    for root, subs in subquestions.items():
        dot.node(root, label=root, shape="box", style="filled", fillcolor="lightblue")
        for sq in subs:
            dot.node(sq, label=sq, shape="ellipse")
            dot.edge(root, sq)

    # renderiza en la UI
    import streamlit as st
    st.subheader("Grafo de razonamiento")
    st.graphviz_chart(dot.source)
# al final de verdiktia/ui.py

from typing import Dict, List

def render_adaptations(adaptations: Dict[str, List[str]]) -> None:
    """Muestra las recomendaciones de adaptación."""
    import streamlit as st

    st.subheader("Recomendaciones de Adaptación")
    for root, recs in adaptations.items():
        with st.expander(f"Ajustes para «{root}»"):
            for i, r in enumerate(recs, 1):
                st.markdown(f"{i}. {r}")
