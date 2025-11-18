# verdiktia/data.py

from __future__ import annotations
import pandas as pd
from typing import List, Dict
from .data_providers import (
    WorldBankProvider,
    UnescoStudentProvider,
    VisaDifficultyProvider,
)

def get_countries(year: int = 2024) -> List[Dict]:
    """Recupera indicadores académicos y demográficos para el análisis de admisiones."""
    wb = WorldBankProvider()
    unesco = UnescoStudentProvider()
    visa = VisaDifficultyProvider()

    # 1) Datos económicos (Poder adquisitivo para matrículas)
    # Usamos 'poder_adquisitivo' (GDP per capita PPP)
    df_eco = wb.fetch_indicators(["poder_adquisitivo"], year)

    # 2) Datos demográficos y de movilidad estudiantil
    df_student = unesco.fetch_indicators(["demografia_joven", "movilidad_outbound"], year)

    # 3) Datos burocráticos y culturales (Visados e Idioma)
    df_visa = visa.fetch_indicators(["facilidad_visado", "afinidad_idioma"], year)

    # 4) Merge progresivo por ISO (Left join partiendo de la lista de estudiantes UNESCO)
    
    # CRÍTICO: Renombramos 'nombre' de WB para evitar conflictos con 'nombre_unesco'
    df_eco = df_eco.rename(columns={'nombre': 'nombre_wb'})
    
    # Merge 1: UNESCO (izquierda, contiene 'nombre_unesco') + WB (derecha)
    df = df_student.merge(df_eco, on="iso", how="left")
    
    # Merge 2: Resultado + Visados
    df = df.merge(df_visa, on="iso", how="left")
    
    # --- Gestión del nombre final y valores nulos ---
    
    # Creamos una columna 'nombre' unificada, priorizando el nombre de WB si existe, sino usando el de UNESCO.
    df['nombre'] = df['nombre_wb'].fillna(df['nombre_unesco'])
    
    # Identificar columnas numéricas para rellenar con 0
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Rellenar solo valores numéricos nulos con 0
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Asegurarnos de que el nombre tampoco sea nulo (usando una string vacía como fallback)
    df['nombre'] = df['nombre'].fillna("")


    # 5) Genera la lista de dicts en el formato esperado por logic.py
    countries = []
    for _, row in df.iterrows():
        # Normalización de métricas grandes para el sistema de pesos (target: escala 0-10)
        
        # Poder adquisitivo: 50,000 USD -> ~5 puntos
        gdp_val = float(row.get("poder_adquisitivo", 0))
        score_poder = min(gdp_val / 10000, 10)
        
        # Movilidad (Outbound): 50,000 estudiantes -> ~5 puntos
        mob_val = float(row.get("movilidad_outbound", 0))
        score_interes = min(mob_val / 10000, 10)

        # Demografía joven (viene en 0-1) -> pasar a 0-10
        score_demo = float(row.get("demografia_joven", 0)) * 10

        countries.append({
            "nombre":               row["nombre"],
            
            # Métricas clave normalizadas
            "poder_adquisitivo":    score_poder,
            "demografia_joven":     score_demo,
            "interes_espana":       score_interes,   # Proxy basado en volumen de movilidad
            "facilidad_visado":     float(row.get("facilidad_visado", 0)), # Escala 1-5 original
            "afinidad_idioma":      float(row.get("afinidad_idioma", 0)),  # Escala 1-5 original
            
            # Placeholders para lógica futura
            "convenios_existentes": 0, 
            "seguridad":            5,
        })
    
    return countries
