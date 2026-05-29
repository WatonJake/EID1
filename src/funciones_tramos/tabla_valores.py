"""
Módulo para generar tabla de valores cerca del punto crítico.
Crea puntos de evaluación por izquierda y derecha del punto de discontinuidad.
"""


def generar_puntos_cercanos(a):
    """
    Genera una tabla de valores cercanos al punto crítico 'a'.
    
    Parámetros:
    -----------
    a : float
        Punto crítico (punto de discontinuidad)
    
    Retorna:
    --------
    dict con las claves:
        - 'puntos_izquierda': list, valores por izquierda de 'a'
        - 'puntos_derecha': list, valores por derecha de 'a'
        - 'todos_puntos': list, todos los puntos ordenados
        - 'tabla': list, estructura tabular con evaluaciones
    """
    
    # Generar puntos por izquierda
    puntos_izquierda = [
        a - 1,
        a - 0.1,
        a - 0.01,
        a - 0.001
    ]
    
    # Generar puntos por derecha
    puntos_derecha = [
        a + 0.001,
        a + 0.01,
        a + 0.1,
        a + 1
    ]
    
    # Combinar todos los puntos
    todos_puntos = puntos_izquierda + puntos_derecha
    
    # Crear estructura tabular
    tabla = []
    
    # Agregar puntos por izquierda
    tabla.append({
        'posicion': 'Izquierda de a',
        'distancia_a_a': -1,
        'x': a - 1,
        'tipo': 'izquierda'
    })
    tabla.append({
        'posicion': 'Izquierda de a',
        'distancia_a_a': -0.1,
        'x': a - 0.1,
        'tipo': 'izquierda'
    })
    tabla.append({
        'posicion': 'Izquierda de a',
        'distancia_a_a': -0.01,
        'x': a - 0.01,
        'tipo': 'izquierda'
    })
    tabla.append({
        'posicion': 'Izquierda de a',
        'distancia_a_a': -0.001,
        'x': a - 0.001,
        'tipo': 'izquierda'
    })
    
    # Punto crítico
    tabla.append({
        'posicion': 'Punto crítico',
        'distancia_a_a': 0,
        'x': a,
        'tipo': 'critico'
    })
    
    # Agregar puntos por derecha
    tabla.append({
        'posicion': 'Derecha de a',
        'distancia_a_a': 0.001,
        'x': a + 0.001,
        'tipo': 'derecha'
    })
    tabla.append({
        'posicion': 'Derecha de a',
        'distancia_a_a': 0.01,
        'x': a + 0.01,
        'tipo': 'derecha'
    })
    tabla.append({
        'posicion': 'Derecha de a',
        'distancia_a_a': 0.1,
        'x': a + 0.1,
        'tipo': 'derecha'
    })
    tabla.append({
        'posicion': 'Derecha de a',
        'distancia_a_a': 1,
        'x': a + 1,
        'tipo': 'derecha'
    })
    
    return {
        'puntos_izquierda': puntos_izquierda,
        'puntos_derecha': puntos_derecha,
        'todos_puntos': todos_puntos,
        'tabla': tabla,
        'punto_critico': a
    }


def evaluar_en_tabla(puntos_info, funcion_evaluadora):
    """
    Evalúa una función en los puntos de la tabla.
    
    Parámetros:
    -----------
    puntos_info : dict
        Resultado de generar_puntos_cercanos()
    funcion_evaluadora : callable
        Función que toma x y retorna f(x)
    
    Retorna:
    --------
    list, tabla extendida con valores de f(x)
    """
    tabla_evaluada = []
    
    for punto in puntos_info['tabla']:
        try:
            valor = funcion_evaluadora(punto['x'])
            punto['f(x)'] = valor
            punto['error'] = None
        except Exception as e:
            punto['f(x)'] = None
            punto['error'] = str(e)
        
        tabla_evaluada.append(punto)
    
    return tabla_evaluada
