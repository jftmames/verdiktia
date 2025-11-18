import streamlit as st
from verdiktia import ui, data, logic
from verdiktia.inquiry     import InquiryEngine
from verdiktia.adaptation  import AdaptationEngine
from verdiktia.expansion   import ExpansionEngine

def main():
    # Configuración de la página
    st.set_page_config(page_title="VERDIKTIA - Admisiones", layout="centered")
    # CAMBIO: Título principal adaptado
    st.title("VERDIKTIA – Estrategia de Captación de Alumnos")

    # 1) INPUTS y PESOS
    # Nota: ui.render_inputs ya fue modificado para pedir datos académicos
    profile = ui.render_inputs()
    weights = ui.render_weights()

    # 2) MOTOR DE INDAGACIÓN
    engine = InquiryEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
    
    # CAMBIO: Preguntas estratégicas (Canvas) para el sector universitario
    canvas_questions = [
        "¿Tenemos capacidad administrativa para gestionar visados de estudiantes extracomunitarios?",
        "¿Es nuestra oferta académica competitiva en precio y prestigio?",
        "¿Disponemos de servicios de acogida (alojamiento, idioma) para estudiantes internacionales?",
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
    
    # CAMBIO: Etiqueta del botón
    if st.button("Generar recomendaciones de adaptación académica"):
        adaptations = adapt_engine.generate_adaptations(canvas_answers, profile)
        ui.render_adaptations(adaptations)

    # 5) RANKING y PLAN DE RECLUTAMIENTO
    # CAMBIO: Etiqueta del botón
    if st.button("Generar estrategia de reclutamiento"):
        # 5.1) Ranking (usa la nueva lógica de demografía/PIB)
        countries = data.get_countries()
        ranked    = logic.rank_countries(profile, countries, weights)
        ui.render_results(ranked)

        # 5.2) Plan de reclutamiento (ExpansionEngine)
        # Nota: El prompt dentro de ExpansionEngine debería ajustarse para dar acciones de marketing educativo
        exp_engine = ExpansionEngine(api_key=st.secrets.get("OPENAI_API_KEY"))
        plan       = exp_engine.generate_plan(ranked, profile, top_n=3)
        ui.render_expansion_plan(plan)

if __name__ == "__main__":
    main()
