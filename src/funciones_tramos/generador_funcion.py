"""
Módulo para generar funciones por tramos con diferentes tipos de discontinuidades.
El tipo de discontinuidad se determina por el residuo de d8 % 3.
"""


def generar_funcion_por_tramos(datos_rut):
    """
    Genera una función por tramos con base en los datos del RUT.
    
    Parámetros:
    -----------
    datos_rut : dict
        Diccionario con información del RUT que contiene:
        - 'd3': tercer dígito del RUT
        - 'd8': octavo dígito del RUT
    
    Retorna:
    --------
    dict con las claves:
        - 'tipo_discontinuidad': str, tipo de discontinuidad (removible, salto, infinita)
        - 'punto_critico': float, valor de 'a' donde ocurre la discontinuidad
        - 'descripcion': str, descripción textual de la función
        - 'regla_usada': str, explicación de cómo se seleccionó el caso
        - 'funcion_def': str, definición de la función por tramos
    """
    
    # Extraer dígitos del RUT
    d3 = datos_rut.get('d3', 0)
    d8 = datos_rut.get('d8', 0)
    
    # Definir punto crítico
    a = d3
    
    # Calcular residuo para determinar el tipo de discontinuidad
    residuo = d8 % 3
    
    # Generar función según el residuo
    if residuo == 0:
        # Discontinuidad removible
        tipo_discontinuidad = "Discontinuidad Removible"
        descripcion = f"""
Función por tramos con discontinuidad removible en x = {a}:

    f(x) = {{
        x² + 1,                    si x < {a}
        indefinida,                si x = {a}
        x² + 1,                    si x > {a}
    }}

La función tiene el mismo límite por ambos lados en x = {a},
pero no está definida en ese punto.
El "agujero" se puede "remover" redefiniendo f({a}) = {a**2 + 1}.
"""
        regla_usada = f"d8 % 3 = {residuo} (residuo 0) → Discontinuidad Removible"
        funcion_def = {
            "izquierda": f"f(x) = x² + 1, para x < {a}",
            "punto": f"No definida en x = {a}",
            "derecha": f"f(x) = x² + 1, para x > {a}"
        }
    
    elif residuo == 1:
        # Discontinuidad de salto
        tipo_discontinuidad = "Discontinuidad de Salto"
        descripcion = f"""
Función por tramos con discontinuidad de salto en x = {a}:

    f(x) = {{
        2x + 1,                    si x ≤ {a}
        x + 5,                     si x > {a}
    }}

Los límites por la izquierda y derecha son diferentes.
Límite izquierdo: lim(x→{a}⁻) f(x) = {2*a + 1}
Límite derecho: lim(x→{a}⁺) f(x) = {a + 5}
Salto = |{2*a + 1} - {a + 5}| = {abs((2*a + 1) - (a + 5))}
"""
        regla_usada = f"d8 % 3 = {residuo} (residuo 1) → Discontinuidad de Salto"
        funcion_def = {
            "izquierda": f"f(x) = 2x + 1, para x ≤ {a}",
            "punto": f"f({a}) = {2*a + 1}",
            "derecha": f"f(x) = x + 5, para x > {a}"
        }
    
    else:  # residuo == 2
        # Discontinuidad infinita
        tipo_discontinuidad = "Discontinuidad Infinita"
        descripcion = f"""
Función por tramos con discontinuidad infinita en x = {a}:

    f(x) = {{
        1/(x - {a}),               si x ≠ {a}
        indefinida,                si x = {a}
    }}

Los límites laterales tienden a infinito.
Límite izquierdo: lim(x→{a}⁻) f(x) = -∞
Límite derecho: lim(x→{a}⁺) f(x) = +∞
La función tiene una asíntota vertical en x = {a}.
"""
        regla_usada = f"d8 % 3 = {residuo} (residuo 2) → Discontinuidad Infinita"
        funcion_def = {
            "izquierda": f"f(x) = 1/(x - {a}), para x < {a}",
            "punto": f"No definida en x = {a}",
            "derecha": f"f(x) = 1/(x - {a}), para x > {a}"
        }
    
    return {
        'tipo_discontinuidad': tipo_discontinuidad,
        'punto_critico': a,
        'descripcion': descripcion,
        'regla_usada': regla_usada,
        'funcion_def': funcion_def
    }
