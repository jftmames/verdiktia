# tests/test_logic_weights.py

import pytest
from verdiktia import logic

@pytest.mark.parametrize("key", list(logic.WEIGHTS.keys()))
def test_weight_affects_score(key):
    """Verifica que variar cada atributo individualmente cambia el score en la magnitud esperada."""
    # perfil vacío (sin preferencias ni certificaciones)
    profile = {"preferencias_geo": [], "certificaciones": [], "idiomas": []}

    # base country con todo a nivel mínimo
    base = {
        "nombre": "X", "crecimiento": 0, "saturacion": 5,
        "aranceles": 5, "logistica": 0,
        "cultural": "Z", "certificados": [], "idioma": "Z"
    }
    # copia y modifica solo el atributo que nos interesa
    modified = base.copy()
    w = logic.WEIGHTS[key]

    if key == "crecimiento":
        modified["crecimiento"] = 5
        expected_diff = 5 * w
    elif key == "saturacion":
        modified["saturacion"] = 0
        expected_diff = 5 * w
    elif key == "aranceles":
        modified["aranceles"] = 0
        expected_diff = 5 * w
    elif key == "logistica":
        modified["logistica"] = 5
        expected_diff = 5 * w
    elif key == "cultural":
        # ajustamos perfil para que coincida
        profile["preferencias_geo"] = [base["cultural"]]
        expected_diff = w
    elif key == "certificados":
        # ajustamos país y perfil para que coincida
        cert = "TEST-CERT"
        base["certificados"] = [cert]
        modified = base
        profile["certificaciones"] = [cert]
        expected_diff = w
    elif key == "idioma":
        lang = "TEST-LANG"
        base["idioma"] = lang
        modified = base
        profile["idiomas"] = [lang]
        expected_diff = w
    else:
        pytest.skip(f"No hay lógica definida para la clave {key}")

    score_base = logic.score_country(profile, base)
    score_mod  = logic.score_country(profile, modified)
    assert score_mod - score_base == expected_diff, (
        f"El cambio en '{key}' debería aportar exactamente {expected_diff}, "
        f"pero fue {score_mod - score_base}"
    )
