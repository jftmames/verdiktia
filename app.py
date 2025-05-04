import streamlit as st
from verdiktia import ui, data, logic
from verdiktia.inquiry import InquiryEngine
from verdiktia.adaptation import AdaptationEngine

def main():
    # Configuración de la página
    st.set_page_config(page_title="VERDIKTIA", layout="centered")
    st.title("VERDIKTIA – Selección de Mercado Internacional")

    # 1) Inputs y pesos
    profile = ui.render_inputs()
    weights = ui.render_weights()

    # 2) Motor de indagación
    engine = InquiryEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
    canvas_questions = [
        "¿Mis recursos financieros son suficientes para exportar?",
        "¿Tengo una propuesta de valor clara para el mercado internacional?",
        "¿Conozco mis canales de distribución en destino?",
    ]
    subqs = {q: engine.generate_subquestions(q) for q in canvas_questions}

    # 3) Renderizado del Canvas y grafo de razonamiento
    ui.render_canvas(subqs)
    ui.render_reasoning_graph(subqs)

    # 4) Adaptaciones
    canvas_answers = {
        q: st.session_state.get(f"resp_{q}", "")
        for q in canvas_questions
    }
    adapt_engine = AdaptationEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
    if st.button("Generar recomendaciones de adaptación"):
        adaptations = adapt_engine.generate_adaptations(canvas_answers, profile)
        ui.render_adaptations(adaptations)

    # 5) Ranking de mercados
    if st.button("Generar recomendación de mercados"):
        countries = data.get_countries()
        ranked = logic.rank_countries(profile, countries, weights)
        ui.render_results(ranked)

if __name__ == "__main__":
    main()
