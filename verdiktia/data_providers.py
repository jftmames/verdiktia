# verdiktia/data_providers.py

import requests
import pandas as pd
from typing import List, Dict


class BaseProvider:
    """Interfaz común para proveedores de datos."""
    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        raise NotImplementedError


class WorldBankProvider(BaseProvider):
    BASE_URL = "https://api.worldbank.org/v2"
    # Mapea nuestro nombre interno → código World Bank
    INDICATORS = {
        "gdp_growth": "NY.GDP.MKTP.KD.ZG"
    }

    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        dfs = []
        for ind in indicators:
            code = self.INDICATORS[ind]
            url = f"{self.BASE_URL}/country/all/indicator/{code}"
            params = {
                "date": f"{year}:{year}",
                "format": "json",
                "per_page": 300
            }
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()[1]  # [0] es metadata
            df = pd.json_normalize(data)
            # Extraemos país, valor e indicador
            df = df[["country.id", "country.value", "value"]]
            df.columns = ["iso", "nombre", ind]
            dfs.append(df)
        # Unimos por país
        return pd.concat(dfs, axis=1).loc[:, ~pd.concat(dfs, axis=1).columns.duplicated()]


class UNComtradeProvider(BaseProvider):
    BASE_URL = "https://comtrade.un.org/api/get"
    # Aquí podrías mapear "market_saturation" → parámetros de Comtrade
    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        # Ejemplo stub: devuelve saturación aleatoria
        import numpy as np
        # Este stub retorna solo una columna "market_saturation"
        df = pd.DataFrame({
            "iso": ["DEU", "CHL", "ARE"],
            "market_saturation": np.random.uniform(0, 1, size=3)
        })
        return df


class GoogleMarketFinderProvider(BaseProvider):
    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        # A día de hoy no hay API pública oficial;
        # aquí podrías parsear CSVs o usar scraping ligero
        # De momento devolvemos un stub de "market_size"
        df = pd.DataFrame({
            "iso": ["DEU", "CHL", "ARE"],
            "market_size": [100_000, 50_000, 80_000]
        })
        return df
