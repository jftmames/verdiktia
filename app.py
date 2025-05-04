# app.py
import streamlit as st
from verdiktia import ui, data, logic
from verdiktia.inquiry    import InquiryEngine
from verdiktia.adaptation import AdaptationEngine
from verdiktia.expansion  import ExpansionEngine

def main():
    st.set_page_config(page_title="VERDIKTIA", layout="centered")

    # ... pasos 1–4: inputs, subquestions, adaptaciones, etc.

    # 5) Ranking de mercados
    if st.button("Generar recomendación de mercados"):
        countries = data.get_countries()
        ranked    = logic.rank_countries(profile, countries, weights)
        ui.render_results(ranked)

        # 6) Plan de escalado
        exp_engine = ExpansionEngine(api_key=st.secrets["OPENAI_API_KEY"])
        plan       = exp_engine.generate_plan(ranked, profile, top_n=3)
        ui.render_expansion_plan(plan)

if __name__ == "__main__":
    main()
