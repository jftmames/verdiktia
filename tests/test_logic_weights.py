# tests/test_logic_weights.py
import pytest
from verdiktia import logic
from copy import deepcopy

@pytest.mark.parametrize("key", list(logic.WEIGHTS.keys()))
def test_weight_affects_score(key):
    """Verifica que variar cada atributo individualmente cambia el score en la magnitud esperada."""
    # Perfil base sin preferencias ni certificaciones
    profile_base = {"preferencias_geo": [], "certificaciones": [], "idiomas": []}

    # País base con valores mínimos
    base_country = {
        "nombre": "X", "crecimiento": 0, "saturacion": 5,
        "aranceles": 5, "logistica": 0,
        "cultural": "Z", "certificados": [], "idioma": "Z"
    }
    w = logic.WEIGHTS[key]

    # Configuración según tipo de peso
    if key in ("crecimiento", "saturacion", "aranceles", "logistica"):
        # Atributos numéricos: aumentar en 5 unidades
        country_mod = deepcopy(base_country)
        if key == "crecimiento":
            country_mod["crecimiento"] = 5
        elif key == "saturacion":
            country_mod["saturacion"] = 0
        elif key == "aranceles":
            country_mod["aranceles"] = 0
        elif key == "logistica":
            country_mod["logistica"] = 5

        score_base = logic.score_country(profile_base, base_country)
        score_mod = logic.score_country(profile_base, country_mod)
        expected_diff = 5 * w

    elif key == "cultural":
        # Preferencia geográfica: sin vs con coincidencia
        profile_mod = deepcopy(profile_base)
        profile_mod["preferencias_geo"] = [base_country["cultural"]]

        score_base = logic.score_country(profile_base, base_country)
        score_mod = logic.score_country(profile_mod, base_country)
        expected_diff = w

    elif key == "certificados":
        # Certificados: sin vs con coincidencia
        cert = "CERT-OK"
        country_mod = deepcopy(base_country)
        country_mod["certificados"] = [cert]
        profile_mod = deepcopy(profile_base)
        profile_mod["certificaciones"] = [cert]

        score_base = logic.score_country(profile_base, base_country)
        score_mod = logic.score_country(profile_mod, country_mod)
        expected_diff = w

    elif key == "idioma":
        # Idiomas: sin vs con coincidencia
        lang = "LANG-OK"
        country_mod = deepcopy(base_country)
        country_mod["idioma"] = lang
        profile_mod = deepcopy(profile_base)
        profile_mod["idiomas"] = [lang]

        score_base = logic.score_country(profile_base, base_country)
        score_mod = logic.score_country(profile_mod, country_mod)
        expected_diff = w

    else:
        pytest.skip(f"No hay lógica definida para la clave {key}")

    assert score_mod - score_base == expected_diff, (
        f"La clave '{key}' debería cambiar el score en {expected_diff}, "
        f"pero cambió en {score_mod - score_base}"
    )
