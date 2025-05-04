from __future__ import annotations
from typing import Dict, List, Tuple

WEIGHTS = dict(
    crecimiento  = 25,
    saturacion   = 20,
    aranceles    = 20,
    logistica    = 15,
    cultural     = 10,
    certificados = 5,
    idioma       = 5,
)

def score_country(profile: Dict, c: Dict) -> int:
    score  = c["crecimiento"] * WEIGHTS["crecimiento"]
    score += (5 - c["saturacion"]) * WEIGHTS["saturacion"]
    score += (5 - c["aranceles"]) * WEIGHTS["aranceles"]
    score += c["logistica"] * WEIGHTS["logistica"]
    if c["cultural"] in profile["preferencias_geo"]:
        score += WEIGHTS["cultural"]
    if set(profile["certificaciones"]) & set(c["certificados"]):
        score += WEIGHTS["certificados"]
    if c["idioma"] in profile["idiomas"]:
        score += WEIGHTS["idioma"]
    return score

def rank_countries(profile: Dict, countries: List[Dict]) -> List[Tuple[str,int]]:
    ranked = [(c["nombre"], score_country(profile, c)) for c in countries]
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
