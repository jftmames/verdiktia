# verdiktia/logic.py
from __future__ import annotations
import yaml
from pathlib import Path
from typing import Union, Dict, List, Tuple

def load_weights(path: Union[Path, str] = "config.yaml") -> Dict[str, int]:
    """Carga los pesos desde el YAML de configuración."""
    cfg = yaml.safe_load(Path(path).read_text())
    return cfg.get("weights", {})

def score_country(profile: Dict, country: Dict, weights: Dict[str, int]) -> float:
    """
    Calcula puntuación para un país origen basándose en métricas académicas/demográficas
    y ajustando los pesos según el perfil del programa educativo.
    """
    score = 0.0
    
    # --- FACTORES DIRECTOS ---
    # 1. Demografía (Volumen de estudiantes potenciales)
    score += country.get("demografia_joven", 0) * weights.get("demografia_joven", 0)
    
    # 2. Interés previo (Movilidad Outbound histórica hacia España/Europa)
    score += country.get("interes_espana", 0) * weights.get("interes_espana", 0)
    
    # 3. Facilidad Burocrática (Visados)
    score += country.get("facilidad_visado", 0) * weights.get("facilidad_visado", 0)

    # --- FACTORES CONDICIONALES ---
    
    # 4. Poder Adquisitivo (Ajustado por política de Becas)
    # Si la universidad tiene muchas becas ("Alta"), el nivel económico del país importa menos.
    # Si no hay becas ("Nula"), es crítico que el país tenga alto poder adquisitivo.
    w_poder = weights.get("poder_adquisitivo", 0)
    becas   = profile.get("recursos_becas", "Media")
    
    if becas == "Alta":
        w_poder *= 0.5  # Reducimos importancia del factor económico
    elif becas == "Nula":
        w_poder *= 1.5  # Aumentamos importancia (necesitamos alumnos "full-pay")
    
    score += country.get("poder_adquisitivo", 0) * w_poder

    # 5. Afinidad Idiomática (Ajustado por Idioma del Programa)
    w_idioma = weights.get("afinidad_idioma", 0)
    idioma_prog = profile.get("idioma_imparticion", "Español")

    val_idioma = country.get("afinidad_idioma", 0)

    if idioma_prog == "Español":
        # Si el curso es en español, que el país hable español es CRÍTICO.
        score += val_idioma * w_idioma
    elif idioma_prog == "Inglés":
        # Si es en inglés, saber español ayuda a la vida social, pero no es bloqueante.
        score += val_idioma * (w_idioma * 0.3)
    else:
        # Caso Bilingüe u otros
        score += val_idioma * (w_idioma * 0.8)

    return score

def rank_countries(
    profile: Dict,
    countries: List[Dict],
    weights: Dict[str, int]
) -> List[Tuple[str, float]]:
    """Devuelve arreglo ordenado de tuplas (nombre, puntuación)."""
    ranked = [
        (c.get("nombre", ""), score_country(profile, c, weights))
        for c in countries
    ]
    # Ordenamos de mayor a menor score
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
