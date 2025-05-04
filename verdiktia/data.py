# verdiktia/data.py

from __future__ import annotations
import pandas as pd
from typing import List, Dict
from .data_providers import (
    WorldBankProvider,
    UNComtradeProvider,
    GoogleMarketFinderProvider,
)

def get_countries(year: int = 2023) -> List[Dict]:
    """Recupera indicadores de distintos proveedores y los unifica en el formato esperado."""
    wb = WorldBankProvider()
    un = UNComtradeProvider()
    gm = GoogleMarketFinderProvider()

    # 1) Trae crecimiento (gdp_growth)
    df_growth = wb.fetch_indicators(["gdp_growth"], year)
    # 2) Trae saturación de mercado
    df_sat    = un.fetch_indicators(["market_saturation"], year)
    # 3) Trae tamaño de mercado
    df_size   = gm.fetch_indicators(["market_size"], year)

    # 4) Merge por ISO
    df = df_growth.merge(df_sat, on="iso", how="left")
    df = df.merge(df_size, on="iso", how="left")
    df = df.fillna(0)

    # 5) Genera la lista de dicts en el formato que espera logic.py
    countries = []
    for _, row in df.iterrows():
        countries.append({
            "nombre":        row["nombre"],
            "crecimiento":   float(row["gdp_growth"]),
            "saturacion":    float(row["market_saturation"]) * 5,  # reescalamos a 0–5
            "aranceles":     0,                                    # por defecto
            "logistica":     0,                                    # por defecto
            "cultural":      "",                                   # rellénalo luego
            "certificados":  [],                                   # idem
            "idioma":        "",                                   # idem
        })
    return countries
