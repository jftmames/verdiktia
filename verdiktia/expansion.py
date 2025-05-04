import os
from openai import OpenAI
from typing import List, Dict

class ExpansionEngine:
    """Genera un plan de entrada faseado a mercados según el modelo Uppsala."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate_plan(
        self,
        ranked_countries: List[Dict],
        profile: Dict,
        top_n: int = 3
    ) -> List[str]:
        """
        Toma los primeros top_n países del ranking y genera un plan
        de entrada fase 1 → fase 2 → fase 3 con acciones concretas.
        """
        top_countries = ranked_countries[:top_n]
        prompt = (
            "Eres un consultor experto en internacionalización y aplicarás "
            "el modelo Uppsala. La empresa tiene este perfil:\n"
            f"{profile}\n\n"
            "Y ha priorizado estos mercados:\n"
        )
        for idx, c in enumerate(top_countries, 1):
            prompt += f"{idx}. {c['nombre']} (score={c['score']:.1f})\n"
        prompt += (
            "\nDescribe un plan en 3 fases:\n"
            "Fase 1: entrada piloto en el mercado 1.\n"
            "Fase 2: expansión al mercado 2.\n"
            "Fase 3: consolidación en el mercado 3.\n"
            "Para cada fase, sugiere 2 acciones concretas."
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        text = resp.choices[0].message.content.strip()
        # separar por fases numeradas
        lines = [line.strip("-• \t") for line in text.splitlines() if line.strip()]
        return lines
