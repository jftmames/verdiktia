# verdiktia/expansion.py
import openai

class ExpansionEngine:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_plan(self, ranked, profile, top_n=3) -> str:
        """
        ranked: lista de tuplas (country_name, score)
        profile: dict con datos del perfil de la empresa
        top_n: cuántos mercados tomar para el plan
        """
        prompt = (
            "Genera un plan de expansión de mercado para la empresa con este perfil:\n"
            f"{profile}\n\n"
            "Prioriza estos mercados:\n"
        )
        # Desempaquetar correctamente la tupla (nombre, score)
        for idx, entry in enumerate(ranked[:top_n], start=1):
            country, score = entry  # entry = (nombre, score)
            prompt += f"{idx}. {country} (score={score:.1f})\n"

        # Llamada a la API de ChatCompletion
        resp = openai.ChatCompletion.create(
            model="gpt-4-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente generador de planes de expansión."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        plan = resp.choices[0].message.content
        return plan
