# verdiktia/ui.py

from __future__ import annotations

import streamlit as st
import yaml
from pathlib import Path
from typing import Any, Dict, List, Tuple
import re
from graphviz import Digraph


def render_inputs() -> Dict[str, Any]:
    st.header("Datos de tu empresa")
    return dict(
        producto         = st.selectbox("Producto", ["Aceite de oliva", "Vino", "Fruta eco"]),
        certificaciones  = st.multiselect("Certificaciones", ["BIO", "IFS", "BRC", "D.O."]),
        preferencias_geo = st.multiselect("Preferencias geográficas", ["UE", "LatAm", "MENA", "Asia"]),
        idiomas          = st.multiselect("Idiomas en el equipo", ["Inglés", "Francés", "Alemán"]),
    )


def render_weights() -> Dict[str, int]:
    st.subheader("Ajusta la importancia de cada factor")
    cfg = yaml.safe_load(Path("config.yaml").read_text())
    default = cfg.get("weights", {})
    weights: Dict[str, int] = {}
    for key, val in default.items():
        weights[key] = st.slider(
            label=key.replace('_', ' ').capitalize(),
            min_value=0,
            max_value=50,
            value=int(val),
            help=f"Peso de '{key}' en el cálculo"
        )
    return weights


def render_results(ranked: List[Tuple[str, float]]) -> None:
    st.subheader("Países recomendados")
    for nombre, score in ranked[:2]:
        st.write(f"**{nombre}** — Puntuación: {score:.1f}/500")
        st.caption(f"Nivel de confianza: {int(score/500*100)} %")


def render_canvas(subquestions: Dict[str, List[str]]) -> None:
    st.subheader("Diagnóstico Inicial (Canvas)")
    for root, subs in subquestions.items():
        with st.expander(root):
            for i, sq in enumerate(subs, start=1):
                st.markdown(f"**{i}.** {sq}")
            st.text_input(f"Responde aquí sobre «{root}»", key=f"resp_{root}")


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
    for root, subs in subquestions.items():
        dot.node(root,   label=root, shape="box", style="filled", fillcolor="lightblue")
        for sq in subs:
            dot.node(sq, label=sq, shape="ellipse")
            dot.edge(root, sq)

    st.subheader("Grafo de razonamiento")
    st.graphviz_chart(dot.source)


def render_adaptations(adaptations: Dict[str, List[str]]) -> None:
    """Muestra las recomendaciones de adaptación."""
    st.subheader("Recomendaciones de Adaptación")
    for root, recs in adaptations.items():
        with st.expander(f"Ajustes para «{root}»"):
            for i, r in enumerate(recs, start=1):
                st.markdown(f"{i}. {r}")


def render_expansion_plan(plan: str) -> None:
    """
    Muestra el plan faseado de entrada a mercados como markdown,
    filtrando líneas vacías o que solo contengan viñetas.
    """
    st.subheader("Plan de Implementación y Escalado")
    lines = plan.splitlines()
    clean: List[str] = []
    for ln in lines:
        stripped = ln.strip()
        if not stripped or re.fullmatch(r"[•\-\*]+", stripped):
            continue
        clean.append(ln)
    st.markdown("\n".join(clean))
