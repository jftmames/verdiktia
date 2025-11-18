# verdiktia/data_providers.py

import requests
import pandas as pd
import numpy as np
from typing import List, Dict


class BaseProvider:
    """Interfaz común para proveedores de datos."""
    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        raise NotImplementedError


class WorldBankProvider(BaseProvider):
    BASE_URL = "https://api.worldbank.org/v2"
    # Mapeamos indicadores relevantes para captación de alumnos:
    # "poder_adquisitivo" -> PIB per cápita, PPA (NY.GDP.PCAP.PP.CD)
    INDICATORS = {
        "poder_adquisitivo": "NY.GDP.PCAP.PP.CD"
    }

    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        dfs = []
        for ind in indicators:
            # Si el indicador no está en nuestro mapa, saltamos o usamos un default
            if ind not in self.INDICATORS:
                continue
                
            code = self.INDICATORS[ind]
            url = f"{self.BASE_URL}/country/all/indicator/{code}"
            params = {
                "date": f"{year}:{year}",
                "format": "json",
                "per_page": 300
            }
            try:
                resp = requests.get(url, params=params)
                resp.raise_for_status()
                # La API devuelve [metadata, data]
                if len(resp.json()) > 1:
                    data = resp.json()[1]
                    df = pd.json_normalize(data)
                    # Extraemos país, valor e indicador
                    df = df[["country.id", "country.value", "value"]]
                    df.columns = ["iso", "nombre", ind]
                    dfs.append(df)
            except Exception as e:
                print(f"Error fetching {ind} from WorldBank: {e}")
                
        if not dfs:
            return pd.DataFrame()
            
        # Unimos por país y eliminamos columnas duplicadas
        final_df = pd.concat(dfs, axis=1)
        return final_df.loc[:, ~final_df.columns.duplicated()]


class UnescoStudentProvider(BaseProvider):
    """
    Proveedor de datos de movilidad estudiantil y demografía.
    En producción conectarías con la API de UNESCO UIS.
    Aquí simulamos datos (Stubs).
    """
    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        # Simulamos datos para países clave en reclutamiento
        data = {
            "iso": ["COL", "CHN", "USA", "MAR", "ITA", "MEX", "BRA", "IND"],
            "nombre_unesco": ["Colombia", "China", "United States", "Morocco", "Italy", "Mexico", "Brazil", "India"]
        }
        
        # Generamos datos simulados si se piden
        if "demografia_joven" in indicators:
            # Score 0-1 de población universitaria potencial
            data["demografia_joven"] = [0.85, 0.40, 0.55, 0.90, 0.30, 0.75, 0.70, 0.95]
            
        if "movilidad_outbound" in indicators:
            # Número absoluto de estudiantes que salen del país
            data["movilidad_outbound"] = [50000, 700000, 100000, 45000, 35000, 30000, 40000, 500000]

        df = pd.DataFrame(data)
        return df


class VisaDifficultyProvider(BaseProvider):
    """
    Proveedor de datos sobre dificultad burocrática y visados para estudiar en España.
    """
    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        # Stub: 1 = Muy difícil/Lento, 5 = Trámite automático/UE
        df = pd.DataFrame({
            "iso": ["COL", "CHN", "USA", "MAR", "ITA", "MEX", "BRA", "IND"],
            "facilidad_visado": [3, 2, 4, 2, 5, 3, 3, 2],
            "afinidad_idioma":  [5, 1, 2, 3, 4, 5, 4, 2] # 5=Nativo, 1=Barrera alta
        })
        
        # Filtramos solo las columnas solicitadas + ISO
        cols = ["iso"] + [ind for ind in indicators if ind in df.columns]
        return df[cols]
