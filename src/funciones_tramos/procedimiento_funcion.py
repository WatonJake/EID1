"""
Módulo para generar procedimientos paso a paso de funciones con discontinuidades.
Genera documentación detallada del análisis de funciones por tramos.
"""


def generar_procedimiento_funcion(datos_rut, funcion_info):
    """
    Genera un procedimiento paso a paso para el análisis de la función.
    
    Parámetros:
    -----------
    datos_rut : dict
        Diccionario con información del RUT
    funcion_info : dict
        Resultado de generar_funcion_por_tramos()
    
    Retorna:
    --------
    str, procedimiento formateado con todos los pasos
    """
    
    d3 = datos_rut.get('d3', 0)
    d8 = datos_rut.get('d8', 0)
    residuo = d8 % 3
    a = funcion_info['punto_critico']
    tipo_discontinuidad = funcion_info['tipo_discontinuidad']
    
    procedimiento = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PROCEDIMIENTO DE ANÁLISIS DE FUNCIÓN                      ║
║                           POR TRAMOS (DISCONTINUA)                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

DATOS DEL RUT:
──────────────
• d3 (tercer dígito):   {d3}
• d8 (octavo dígito):   {d8}


PASO 1: IDENTIFICAR EL PUNTO CRÍTICO
─────────────────────────────────────
El punto crítico 'a' se define como el tercer dígito del RUT:
    
    a = d3 = {d3}

Este es el punto donde ocurrirá la discontinuidad de la función.


PASO 2: CALCULAR EL RESIDUO DE d8 MOD 3
─────────────────────────────────────────
Se calcula el residuo de la división de d8 entre 3:
    
    residuo = d8 % 3
    residuo = {d8} % 3
    residuo = {residuo}

Este residuo determina qué tipo de discontinuidad genera la función.


PASO 3: CLASIFICAR EL TIPO DE DISCONTINUIDAD
──────────────────────────────────────────────
Según el valor del residuo:

    • Si residuo = 0 → Discontinuidad REMOVIBLE
    • Si residuo = 1 → Discontinuidad de SALTO
    • Si residuo = 2 → Discontinuidad INFINITA

En este caso: residuo = {residuo}

{_generar_caso_discontinuidad(residuo, a)}


PASO 4: DEFINIR LA FUNCIÓN POR TRAMOS
──────────────────────────────────────
Según el tipo de discontinuidad clasificado ({tipo_discontinuidad}):

{_generar_definicion_funcion(residuo, a)}


PASO 5: ANÁLISIS DE LÍMITES
─────────────────────────────
{_generar_analisis_limites(residuo, a)}


PASO 6: DESCRIPCIÓN GENERAL
────────────────────────────
{funcion_info['descripcion']}


RESUMEN FINAL
──────────────
• Punto crítico (a):        {a}
• Tipo de discontinuidad:   {tipo_discontinuidad}
• Regla de selección:       {funcion_info['regla_usada']}

╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    return procedimiento


def _generar_caso_discontinuidad(residuo, a):
    """Genera la descripción del caso específico de discontinuidad."""
    
    if residuo == 0:
        return f"""
    → DISCONTINUIDAD REMOVIBLE en x = {a}
    
    Características:
    • Los límites laterales existen y son iguales
    • La función NO está definida en el punto
    • Se puede "remover" el "agujero" redefiniendo el punto
    • lim(x→{a}⁻) f(x) = lim(x→{a}⁺) f(x) ≠ f({a})
"""
    
    elif residuo == 1:
        return f"""
    → DISCONTINUIDAD DE SALTO en x = {a}
    
    Características:
    • Los límites laterales existen pero son diferentes
    • Hay un "salto" finito en el valor de la función
    • Ambos límites son finitos pero distintos
    • |lim(x→{a}⁻) f(x) - lim(x→{a}⁺) f(x)| > 0
"""
    
    else:  # residuo == 2
        return f"""
    → DISCONTINUIDAD INFINITA en x = {a}
    
    Características:
    • Al menos uno de los límites laterales es infinito (±∞)
    • La función se comporta de forma explosiva cerca del punto
    • Típicamente indica una asíntota vertical
    • lim(x→{a}⁻) f(x) = ±∞  o  lim(x→{a}⁺) f(x) = ±∞
"""


def _generar_definicion_funcion(residuo, a):
    """Genera la definición formal de la función."""
    
    if residuo == 0:
        return f"""
    f(x) = {{
        x² + 1,                    si x < {a}
        [no definida],             si x = {a}
        x² + 1,                    si x > {a}
    }}
    
    La función es x² + 1 a ambos lados, pero no está definida en x = {a}.
    Límites: lim(x→{a}⁻) f(x) = lim(x→{a}⁺) f(x) = {a**2 + 1}
"""
    
    elif residuo == 1:
        return f"""
    f(x) = {{
        2x + 1,                    si x ≤ {a}
        x + 5,                     si x > {a}
    }}
    
    Dos reglas diferentes generan un "salto" en el punto x = {a}.
    Por izquierda: f({a}) = 2({a}) + 1 = {2*a + 1}
    Por derecha:  lim(x→{a}⁺) f(x) = {a} + 5 = {a + 5}
    Magnitud del salto: |{2*a + 1} - {a + 5}| = {abs((2*a + 1) - (a + 5))}
"""
    
    else:  # residuo == 2
        return f"""
    f(x) = 1/(x - {a})           para x ≠ {a}
    
    Función racional que diverge en x = {a}.
    • Cuando x → {a} por la izquierda:   f(x) → -∞
    • Cuando x → {a} por la derecha:    f(x) → +∞
    
    La recta x = {a} es una asíntota vertical.
"""


def _generar_analisis_limites(residuo, a):
    """Genera el análisis de límites según el tipo de discontinuidad."""
    
    if residuo == 0:
        return f"""
    Límite por la izquierda:
        lim(x→{a}⁻) f(x) = lim(x→{a}⁻) (x² + 1) = {a}² + 1 = {a**2 + 1}
    
    Límite por la derecha:
        lim(x→{a}⁺) f(x) = lim(x→{a}⁺) (x² + 1) = {a}² + 1 = {a**2 + 1}
    
    Conclusión:
        Los límites son iguales: {a**2 + 1}
        Pero f({a}) no está definida → Discontinuidad REMOVIBLE
"""
    
    elif residuo == 1:
        izq = 2*a + 1
        der = a + 5
        return f"""
    Límite por la izquierda:
        lim(x→{a}⁻) f(x) = lim(x→{a}⁻) (2x + 1) = 2({a}) + 1 = {izq}
    
    Valor en el punto:
        f({a}) = 2({a}) + 1 = {izq}
    
    Límite por la derecha:
        lim(x→{a}⁺) f(x) = lim(x→{a}⁺) (x + 5) = {a} + 5 = {der}
    
    Conclusión:
        Límites diferentes: {izq} ≠ {der}
        Salto de magnitud: |{izq} - {der}| = {abs(izq - der)}
        → Discontinuidad de SALTO
"""
    
    else:  # residuo == 2
        return f"""
    Límite por la izquierda:
        lim(x→{a}⁻) f(x) = lim(x→{a}⁻) 1/(x - {a}) = -∞
        (numerador positivo, denominador negativo pequeño)
    
    Límite por la derecha:
        lim(x→{a}⁺) f(x) = lim(x→{a}⁺) 1/(x - {a}) = +∞
        (numerador positivo, denominador positivo pequeño)
    
    Conclusión:
        Límites infinitos → Asíntota vertical en x = {a}
        → Discontinuidad INFINITA
"""


def generar_tabla_procedimiento(datos_rut, funcion_info, puntos_info=None):
    """
    Genera una tabla resumida del procedimiento.
    
    Parámetros:
    -----------
    datos_rut : dict
        Información del RUT
    funcion_info : dict
        Información de la función
    puntos_info : dict, optional
        Información de puntos cercanos al crítico
    
    Retorna:
    --------
    str, tabla formateada
    """
    
    d3 = datos_rut.get('d3', 0)
    d8 = datos_rut.get('d8', 0)
    residuo = d8 % 3
    
    tabla = f"""
┌─────────────────────────────────────────────────────────────┐
│              TABLA RESUMEN DEL PROCEDIMIENTO                │
├─────────────────────────────────────────────────────────────┤
│ Paso 1: Identificar d3 (punto crítico)                      │
│   d3 = {d3:>51}│
├─────────────────────────────────────────────────────────────┤
│ Paso 2: Calcular d8 % 3                                     │
│   {d8} % 3 = {residuo:>50}│
├─────────────────────────────────────────────────────────────┤
│ Paso 3: Clasificar discontinuidad                           │
│   residuo = {residuo} → {funcion_info['tipo_discontinuidad']:<36}│
├─────────────────────────────────────────────────────────────┤
│ Paso 4: Definir función por tramos                          │
│   (Ver detalles en sección anterior)                        │
├─────────────────────────────────────────────────────────────┤
│ Paso 5: Analizar límites laterales                          │
│   (Ver detalles en sección anterior)                        │
└─────────────────────────────────────────────────────────────┘
"""
    
    return tabla
