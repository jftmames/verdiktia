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
    INDICATORS = {
        "poder_adquisitivo": "NY.GDP.PCAP.PP.CD"
    }

    def fetch_indicators(self, indicators: List[str], year: int) -> pd.DataFrame:
        # SIMULACIÓN (Stub): Se simulan nombres y PIB para garantizar que el merge funcione.
        if "poder_adquisitivo" in indicators:
            data = {
                "iso": ["COL", "CHN", "USA", "MAR", "ITA", "MEX", "BRA", "IND"],
                # Estos nombres simulan ser el campo 'country.value' de la API de WB
                "nombre": ["Colombia (WB)", "China (WB)", "United States (WB)", "Morocco (WB)", "Italy (WB)", "Mexico (WB)", "Brazil (WB)", "India (WB)"],
                "poder_adquisitivo": [14000, 18000, 65000, 9000, 45000, 20000, 16000, 7000] # Valores de PIB PPA
            }
            df = pd.DataFrame(data)
            # Nos aseguramos de que el nombre sea String
            df["nombre"] = df["nombre"].astype(str)
            return df[["iso", "nombre", "poder_adquisitivo"]]
            
        return pd.DataFrame()


class UnescoStudentProvider(BaseProvider):
    """
    Proveedor de datos de movilidad estudiantil y demografía.
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
        # Nos aseguramos de que el nombre sea String
        df["nombre_unesco"] = df["nombre_unesco"].astype(str)
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
