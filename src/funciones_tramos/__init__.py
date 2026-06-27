"""
Paquete funciones_tramos
==========================

Módulo para generar y analizar funciones por tramos con diferentes tipos de discontinuidades.

Módulos incluidos:
    - generador_funcion: Genera funciones con discontinuidades basadas en datos del RUT
    - tabla_valores: Genera tabla de puntos cercanos al punto crítico
    - procedimiento_funcion: Genera procedimientos paso a paso del análisis
"""

from .generador_funcion import generar_funcion_por_tramos
from .tabla_valores import generar_puntos_cercanos, evaluar_en_tabla
from .procedimiento_funcion import (
    generar_procedimiento_funcion,
    generar_tabla_procedimiento
)

__all__ = [
    'generar_funcion_por_tramos',
    'generar_puntos_cercanos',
    'evaluar_en_tabla',
    'generar_procedimiento_funcion',
    'generar_tabla_procedimiento'
]
