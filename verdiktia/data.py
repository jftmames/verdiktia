from __future__ import annotations
from functools import lru_cache
from typing import List, Dict

_COUNTRIES = [
    {"nombre":"Alemania","crecimiento":4,"saturacion":2,"aranceles":0,"logistica":3,
     "cultural":"UE","certificados":["BIO","IFS"],"idioma":"Alemán"},
    {"nombre":"Chile","crecimiento":5,"saturacion":1,"aranceles":0,"logistica":2,
     "cultural":"LatAm","certificados":["BIO","D.O."],"idioma":"Español"},
    {"nombre":"Emiratos Árabes","crecimiento":3,"saturacion":2,"aranceles":5,"logistica":2,
     "cultural":"MENA","certificados":["BRC"],"idioma":"Inglés"},
]

@lru_cache
def get_countries() -> List[Dict]:
    """En futuras versiones se sustituirá por llamadas a APIs externas."""
    return _COUNTRIES.copy()
