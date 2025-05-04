-# verdiktia/ui.py
-from __future__ import annotations
-import streamlit as st
-import yaml
-from pathlib import Path
-from typing import Dict, List, Tuple
+# verdiktia/ui.py
+from __future__ import annotations
+import streamlit as st
+import yaml
+from pathlib import Path
+from typing import Dict, List, Tuple

 def render_inputs() -> Dict[str, any]:
     st.header("Datos de tu empresa")
     return dict(
         producto = st.selectbox("Producto", ["Aceite de oliva","Vino","Fruta eco"]),
         certificaciones = st.multiselect("Certificaciones", ["BIO","IFS","BRC","D.O."]),
         preferencias_geo = st.multiselect("Preferencias geográficas", ["UE","LatAm","MENA","Asia"]),
         idiomas = st.multiselect("Idiomas en el equipo", ["Inglés","Francés","Alemán"]),
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
