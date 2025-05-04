# verdiktia/logic.py
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

def load_weights(path: Path | str = "config.yaml") -> Dict[str,int]:
    cfg = yaml.safe_load(Path(path).read_text())
    return cfg.get("weights", {})

def score_country(profile: Dict, country: Dict, weights: Dict[str,int]) -> int:
    score  = country["crecimiento"] * weights["crecimiento"]
    score += (5 - country["saturacion"]) * weights["saturacion"]
    score += (5 - country["aranceles"]) * weights["aranceles"]
    score += country["logistica"] * weights["logistica"]

    if country["cultural"] in profile["preferencias_geo"]:
        score += weights["cultural"]

    if set(profile["certificaciones"]) & set(country["certificados"]):
        score += weights["certificados"]

    if country["idioma"] in profile["idiomas"]:
        score += weights["idioma"]

    return score

def rank_countries(
    profile: Dict, countries: List[Dict], weights: Dict[str,int]
) -> List[Tuple[str,int]]:
    ranked = [
        (c["nombre"], score_country(profile, c, weights))
        for c in countries
    ]
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
