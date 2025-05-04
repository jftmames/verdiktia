# verdiktia/expansion.py

import os
from openai import OpenAI
from typing import List, Tuple, Dict

class ExpansionEngine:
    """Genera un plan de entrada faseado a mercados según el modelo Uppsala."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate_plan(
        self,
        ranked: List[Tuple[str, float]],
        profile: Dict,
        top_n: int = 3
    ) -> str:
        """
        Toma los primeros top_n países del ranking (lista de (nombre, score))
        y genera un plan en 3 fases con 2 acciones cada una.
        Devuelve el texto completo de la respuesta.
        """
        # Construir prompt
        prompt = (
            "Eres un consultor experto en internacionalización y aplicarás "
            "el modelo Uppsala. La empresa tiene este perfil:\n"
            f"{profile}\n\n"
            "Y ha priorizado estos mercados:\n"
        )
        for idx, (country, score) in enumerate(ranked[:top_n], start=1):
            prompt += f"{idx}. {country} (score={score:.1f})\n"

        prompt += (
            "\nDescribe un plan en 3 fases:\n"
            "Fase 1: entrada piloto en el mercado 1 (2 acciones).\n"
            "Fase 2: expansión al mercado 2 (2 acciones).\n"
            "Fase 3: consolidación en el mercado 3 (2 acciones).\n"
            "Responde como lista numerada por fases y acciones."
        )

        # Llamada a la API con el nuevo cliente
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return resp.choices[0].message.content.strip()
