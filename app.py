# app.py
import streamlit as st
from verdiktia import ui, data, logic

st.set_page_config(page_title="VERDIKTIA", layout="centered")
st.title("VERDIKTIA – Selección de Mercado Internacional")

profile = ui.render_inputs()
weights = ui.render_weights()

if st.button("Generar recomendación"):
    countries = data.get_countries()
    ranked    = logic.rank_countries(profile, countries, weights)
    ui.render_results(ranked)
