"""
Módulo de funciones auxiliares y utilidades de formato/cálculo.
"""

import math
from src.datos import PALABRAS_MENORES, _TABLA_ACENTOS


def normalizar_nombre(nombre: str) -> str:
    """
    Normaliza el nombre de una ciudad: elimina espacios sobrantes y aplica
    mayúsculas iniciales correctas (sin capitalizar preposiciones).

    Ejemplo: "ciudad DE méxico" -> "Ciudad de México"
    """
    palabras = nombre.strip().split()
    if not palabras:
        return ""
    resultado = []
    for i, palabra in enumerate(palabras):
        palabra_low = palabra.lower()
        if palabra_low in PALABRAS_MENORES:
            resultado.append(palabra_low)
        else:
            resultado.append(palabra.capitalize())
    return " ".join(resultado)


def plegar_acentos(texto: str) -> str:
    """Convierte un texto a minúsculas y elimina los acentos."""
    return texto.lower().translate(_TABLA_ACENTOS)


def distancia_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos
    utilizando la fórmula de Haversine.
    """
    radio_tierra = 6371.0  # Radio medio de la Tierra en kilómetros

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2
         + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return radio_tierra * c


def formato_duracion(horas: float) -> str:
    """Convierte horas decimales a formato 'X h Y min'."""
    horas_enteras = int(horas)
    minutos = int(round((horas - horas_enteras) * 60))
    if minutos == 60:
        horas_enteras += 1
        minutos = 0
    return f"{horas_enteras} h {minutos:02d} min"


def formato_km(km: float) -> str:
    """Formatea kilómetros con separador de miles."""
    return f"{round(km):,}".replace(",", " ")
