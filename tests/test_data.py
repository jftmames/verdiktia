# tests/test_data.py

import pytest
from verdiktia.data import get_countries

def test_get_countries_returns_list():
    countries = get_countries()
    assert isinstance(countries, list), "Debe devolver una lista"

@pytest.mark.parametrize("country", get_countries())
def test_country_keys(country):
    # Cada país debe tener estas llaves
    expected = {
        "nombre", "crecimiento", "saturacion", "aranceles",
        "logistica", "cultural", "certificados", "idioma"
    }
    assert expected.issubset(set(country.keys())), f"Faltan claves en {country}"
