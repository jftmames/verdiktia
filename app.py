import streamlit as st
from verdiktia import ui, data, logic
from verdiktia.inquiry    import InquiryEngine
from verdiktia.adaptation import AdaptationEngine
from verdiktia.expansion  import ExpansionEngine

def main():
    # Configuración de la página
    st.set_page_config(page_title="VERDIKTIA", layout="centered")
    st.title("VERDIKTIA – Selección de Mercado Internacional")

    # 1) INPUTS y PESOS
    profile = ui.render_inputs()
    weights = ui.render_weights()

    # 2) MOTOR DE INDAGACIÓN
    engine = InquiryEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
    canvas_questions = [
        "¿Mis recursos financieros son suficientes para exportar?",
        "¿Tengo una propuesta de valor clara para el mercado internacional?",
        "¿Conozco mis canales de distribución en destino?",
    ]
    subqs = {q: engine.generate_subquestions(q) for q in canvas_questions}

    # 3) RENDERIZADO DEL CANVAS y GRAFO XAI
    ui.render_canvas(subqs)
    ui.render_reasoning_graph(subqs)

    # 4) ADAPTACIONES
    canvas_answers = {
        q: st.session_state.get(f"resp_{q}", "")
        for q in canvas_questions
    }
    adapt_engine = AdaptationEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
    if st.button("Generar recomendaciones de adaptación"):
        adaptations = adapt_engine.generate_adaptations(canvas_answers, profile)
        ui.render_adaptations(adaptations)

    # 5) RANKING y PLAN DE ESCALADO
    if st.button("Generar recomendación de mercados"):
        # 5.1) Ranking
        countries = data.get_countries()
        ranked    = logic.rank_countries(profile, countries, weights)
        ui.render_results(ranked)

        # 5.2) Plan de escalado (Uppsala)
        exp_engine = ExpansionEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
        plan       = exp_engine.generate_plan(ranked, profile, top_n=3)
        ui.render_expansion_plan(plan)

if __name__ == "__main__":
    main()
