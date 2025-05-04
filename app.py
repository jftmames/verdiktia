import streamlit as st
from verdiktia import ui, data, logic
from verdiktia.inquiry import InquiryEngine

def main():
    # Configuración de la página
    st.set_page_config(page_title="VERDIKTIA", layout="centered")
    st.title("VERDIKTIA – Selección de Mercado Internacional")

    # 1) Recogida de inputs del usuario
    profile = ui.render_inputs()
    weights = ui.render_weights()

    # 2) Motor de indagación (Inquiry Engine)
    engine = InquiryEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
    canvas_questions = [
        "¿Mis recursos financieros son suficientes para exportar?",
        "¿Tengo una propuesta de valor clara para el mercado internacional?",
        "¿Conozco mis canales de distribución en destino?",
    ]
    subqs = {q: engine.generate_subquestions(q) for q in canvas_questions}

    # 3) Renderizado del Canvas y del grafo de razonamiento
    ui.render_canvas(subqs)
    ui.render_reasoning_graph(subqs)

    # 4) Ranking de mercados al pulsar el botón
    if st.button("Generar recomendación"):
        countries = data.get_countries()
        ranked    = logic.rank_countries(profile, countries, weights)
        ui.render_results(ranked)

if __name__ == "__main__":
    main()
