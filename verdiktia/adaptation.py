# verdiktia/adaptation.py

import os
from openai import OpenAI
from typing import Dict, List

class AdaptationEngine:
    """Genera recomendaciones de adaptación de producto/servicio."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate_adaptations(
        self,
        canvas_answers: Dict[str, str],
        profile: Dict,
    ) -> Dict[str, List[str]]:
        """
        Para cada pregunta raíz, toma la respuesta del usuario
        y su perfil, y devuelve una lista de recomendaciones.
        """
        adaptations: Dict[str, List[str]] = {}
        for root_question, answer in canvas_answers.items():
            prompt = (
                "Eres un experto en internacionalización. "
                "Dado el perfil de empresa:\n"
                f"{profile}\n\n"
                f"Y esta respuesta a «{root_question}»:\n"
                f"{answer}\n\n"
                "Sugiere 3 ajustes concretos en producto/servicio "
                "o estrategia de mercado para mejorar el fit local."
            )
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role":"user","content":prompt}],
                temperature=0.7,
                max_tokens=300
            )
            text = resp.choices[0].message.content.strip()
            # parsea en viñetas o líneas
            lines = [line.strip("-• \t") for line in text.splitlines() if line.strip()]
            adaptations[root_question] = lines
        return adaptations
