import streamlit as st
from verdiktia import ui, data, logic

st.set_page_config(page_title="VERDIKTIA", layout="centered")
st.title("VERDIKTIA – Selección de Mercado Internacional")

profile = ui.render_inputs()

if st.button("Generar recomendación"):
    ranked = logic.rank_countries(profile, data.get_countries())
    ui.render_results(ranked)
