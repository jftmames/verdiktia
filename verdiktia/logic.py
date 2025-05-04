# verdiktia/logic.py
from __future__ import annotations
import yaml
from pathlib import Path
from typing import Union, Dict, List, Tuple

def load_weights(path: Union[Path, str] = "config.yaml") -> Dict[str, int]:
    """Carga los pesos desde el YAML de configuración."""
    cfg = yaml.safe_load(Path(path).read_text())
    return cfg.get("weights", {})

def score_country(profile: Dict, country: Dict, weights: Dict[str, int]) -> int:
    """Calcula puntuación ponderada para un país dado un perfil de empresa y pesos dinámicos."""
    score = 0
    score += country.get("crecimiento", 0) * weights.get("crecimiento", 0)
    score += (5 - country.get("saturacion", 5)) * weights.get("saturacion", 0)
    score += (5 - country.get("aranceles", 5)) * weights.get("aranceles", 0)
    score += country.get("logistica", 0) * weights.get("logistica", 0)

    if country.get("cultural") in profile.get("preferencias_geo", []):
        score += weights.get("cultural", 0)

    if set(profile.get("certificaciones", [])) & set(country.get("certificados", [])):
        score += weights.get("certificados", 0)

    if country.get("idioma") in profile.get("idiomas", []):
        score += weights.get("idioma", 0)

    return score

def rank_countries(
    profile: Dict,
    countries: List[Dict],
    weights: Dict[str, int]
) -> List[Tuple[str, int]]:
    """Devuelve arreglo ordenado de tuplas (nombre, puntuación)."""
    ranked = [
        (c.get("nombre", ""), score_country(profile, c, weights))
        for c in countries
    ]
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
