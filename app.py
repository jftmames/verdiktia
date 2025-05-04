# app.py
import streamlit as st
from verdiktia import ui, data, logic
from verdiktia.inquiry import InquiryEngine

st.set_page_config(page_title="VERDIKTIA", layout="centered")
st.title("VERDIKTIA – Selección de Mercado Internacional")

# 1) Inputs y pesos
profile = ui.render_inputs()
weights = ui.render_weights()

# 2) Inquiry Engine
openai_key = st.secrets.get("OPENAI_API_KEY")
engine = InquiryEngine(api_key=openai_key)

# 3) Loop de Canvas
canvas_questions = [
    "¿Mis recursos financieros son suficientes para exportar?",
    "¿Tengo una propuesta de valor clara para el mercado internacional?",
    "¿Conozco mis canales de distribución en destino?",
]
subqs = {q: engine.generate_subquestions(q) for q in canvas_questions}
ui.render_canvas(subqs)  # nueva función en ui.py

# 4) Ranking
if st.button("Generar recomendación"):
    countries = data.get_countries()
    ranked    = logic.rank_countries(profile, countries, weights)
    ui.render_results(ranked)
