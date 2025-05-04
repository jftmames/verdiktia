import os
import openai
from typing import List

class InquiryEngine:
    """Genera sub-preguntas jerárquicas usando la API de OpenAI."""
    
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def generate_subquestions(self, root_question: str, n: int = 3) -> List[str]:
        """
        Dada una pregunta raíz, devuelve n sub-preguntas numeradas.
        """
        prompt = (
            f"Descompón esta pregunta de Canvas en {n} sub-preguntas concretas:\n"
            f"» {root_question}\n\n"
            "Responde como lista numerada."
        )
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        text = resp.choices[0].message.content.strip()
        # Extrae cada línea numerada
        return [
            line.split(".", 1)[1].strip()
            for line in text.splitlines()
            if line and line[0].isdigit()
        ]
