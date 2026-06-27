def formatear_num(n):
    """
    Muestra un número como entero si no tiene decimales,
    o como decimal con 4 cifras si las tiene.
    """
    if n == int(n):
        return str(int(n))
    return str(round(n, 4))


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def obtener_elementos_conica(datos_canonica, tipo_conica):
    """
    Obtiene los elementos geométricos de una cónica a partir de sus datos canónicos.

    Parámetros:
        datos_canonica : diccionario retornado por transformar_a_canonica()
        tipo_conica    : string con el tipo ("Circunferencia", "Elipse", etc.)

    Retorna:
        diccionario con:
            tipo        : tipo de cónica
            elementos   : diccionario con los elementos geométricos
            descripcion : string con descripción textual de los elementos
    """

    if tipo_conica == "Circunferencia":
        return _elementos_circunferencia(datos_canonica)

    elif tipo_conica == "Elipse":
        return _elementos_elipse(datos_canonica)

    elif tipo_conica == "Hiperbola":
        return _elementos_hiperbola(datos_canonica)

    elif tipo_conica == "Parabola":
        return _elementos_parabola(datos_canonica)

    else:
        return {
            "tipo": tipo_conica,
            "elementos": {},
            "descripcion": "Tipo de cónica no reconocido."
        }


# =============================================================================
# CIRCUNFERENCIA
# =============================================================================

def _elementos_circunferencia(datos_canonica):
    """
    Extrae el centro y el radio de una circunferencia.

    Forma canónica: (x - h)² + (y - k)² = r²

    Elementos:
        Centro  : (h, k)
        Radio   : r = √(radio_cuadrado)
    """

    centro = datos_canonica["centro"]
    radio  = datos_canonica["radio"]

    h = centro[0]
    k = centro[1]

    elementos = {
        "centro" : (h, k),
        "radio"  : radio
    }

    descripcion = []
    descripcion.append("=== Elementos de la Circunferencia ===")
    descripcion.append("")
    descripcion.append(f"Centro : ({formatear_num(h)}, {formatear_num(k)})")
    descripcion.append(f"Radio  : {formatear_num(radio)}")

    return {
        "tipo"        : "Circunferencia",
        "elementos"   : elementos,
        "descripcion" : "\n".join(descripcion)
    }


# =============================================================================
# ELIPSE
# =============================================================================

def _elementos_elipse(datos_canonica):
    """
    Extrae el centro, semiejes y ejes de una elipse.

    Forma canónica: (x - h)²/a² + (y - k)²/b² = 1

    Elementos:
        Centro     : (h, k)
        a          : semieje en x  = √(a_cuadrado)
        b          : semieje en y  = √(b_cuadrado)
        Eje mayor  : 2 * max(a, b)   orientado según cuál semieje es mayor
        Eje menor  : 2 * min(a, b)
    """

    centro     = datos_canonica["centro"]
    a_cuadrado = datos_canonica["a_cuadrado"]
    b_cuadrado = datos_canonica["b_cuadrado"]

    h = centro[0]
    k = centro[1]

    a = a_cuadrado ** 0.5    # semieje asociado a x
    b = b_cuadrado ** 0.5    # semieje asociado a y

    # El eje mayor corresponde al semieje más largo
    if a >= b:
        eje_mayor       = 2 * a
        eje_menor       = 2 * b
        orientacion_eje = "horizontal"    # el eje mayor va en dirección x
    else:
        eje_mayor       = 2 * b
        eje_menor       = 2 * a
        orientacion_eje = "vertical"      # el eje mayor va en dirección y

    elementos = {
        "centro"          : (h, k),
        "a"               : a,
        "b"               : b,
        "eje_mayor"       : eje_mayor,
        "eje_menor"       : eje_menor,
        "orientacion_eje" : orientacion_eje
    }

    descripcion = []
    descripcion.append("=== Elementos de la Elipse ===")
    descripcion.append("")
    descripcion.append(f"Centro           : ({formatear_num(h)}, {formatear_num(k)})")
    descripcion.append(f"Semieje a (en x) : {formatear_num(a)}")
    descripcion.append(f"Semieje b (en y) : {formatear_num(b)}")
    descripcion.append(f"Eje mayor        : {formatear_num(eje_mayor)}  ({orientacion_eje})")
    descripcion.append(f"Eje menor        : {formatear_num(eje_menor)}")

    return {
        "tipo"        : "Elipse",
        "elementos"   : elementos,
        "descripcion" : "\n".join(descripcion)
    }


# =============================================================================
# HIPÉRBOLA
# =============================================================================

def _elementos_hiperbola(datos_canonica):
    """
    Extrae el centro, ejes y orientación de una hipérbola.

    Formas canónicas posibles:
        (x - h)²/a² - (y - k)²/b² = 1   →  eje transverso horizontal
        (y - k)²/a² - (x - h)²/b² = 1   →  eje transverso vertical

    Elementos:
        Centro          : (h, k)
        a               : semeje transverso = √(a_cuadrado)
        b               : semieje conjugado = √(b_cuadrado)
        Eje transverso  : 2a  (en la dirección de las ramas abiertas)
        Eje conjugado   : 2b  (perpendicular al eje transverso)
        Orientación     : horizontal o vertical
    """

    centro     = datos_canonica["centro"]
    a_cuadrado = datos_canonica["a_cuadrado"]
    b_cuadrado = datos_canonica["b_cuadrado"]

    h = centro[0]
    k = centro[1]

    a = a_cuadrado ** 0.5    # semieje transverso
    b = b_cuadrado ** 0.5    # semieje conjugado

    eje_transverso = 2 * a
    eje_conjugado  = 2 * b

    # La orientación se detecta revisando la forma canónica:
    # Si empieza con "(x" o "x" → el término en x es positivo → eje horizontal
    # Si empieza con "(y" o "y" → el término en y es positivo → eje vertical
    forma = datos_canonica["forma_canonica"]

    if forma.startswith("(x") or forma.startswith("x"):
        orientacion = "horizontal"    # ramas abiertas hacia izquierda y derecha
    else:
        orientacion = "vertical"      # ramas abiertas hacia arriba y abajo

    elementos = {
        "centro"         : (h, k),
        "a"              : a,
        "b"              : b,
        "eje_transverso" : eje_transverso,
        "eje_conjugado"  : eje_conjugado,
        "orientacion"    : orientacion
    }

    descripcion = []
    descripcion.append("=== Elementos de la Hipérbola ===")
    descripcion.append("")
    descripcion.append(f"Centro          : ({formatear_num(h)}, {formatear_num(k)})")
    descripcion.append(f"Semieje a       : {formatear_num(a)}")
    descripcion.append(f"Semieje b       : {formatear_num(b)}")
    descripcion.append(f"Eje transverso  : {formatear_num(eje_transverso)}  ({orientacion})")
    descripcion.append(f"Eje conjugado   : {formatear_num(eje_conjugado)}")

    if orientacion == "horizontal":
        descripcion.append("Las ramas abren hacia la izquierda y hacia la derecha.")
    else:
        descripcion.append("Las ramas abren hacia arriba y hacia abajo.")

    return {
        "tipo"        : "Hiperbola",
        "elementos"   : elementos,
        "descripcion" : "\n".join(descripcion)
    }


# =============================================================================
# PARÁBOLA
# =============================================================================

def _elementos_parabola(datos_canonica):
    """
    Extrae el vértice y la orientación de una parábola.

    Formas canónicas posibles:
        (x - h)² = p(y - k)   →  parábola vertical   (abre arriba o abajo)
        (y - k)² = p(x - h)   →  parábola horizontal  (abre izquierda o derecha)

    Elementos:
        Vértice     : (h, k)
        p           : parámetro que controla la apertura
        Orientación : arriba / abajo / derecha / izquierda
    """

    vertice = datos_canonica["vertice"]
    p       = datos_canonica["p"]

    h = vertice[0]
    k = vertice[1]

    # La orientación se detecta revisando la forma canónica:
    # "(x...)² = ..." → parábola vertical  (el cuadrado está en x)
    # "(y...)² = ..." → parábola horizontal (el cuadrado está en y)
    forma = datos_canonica["forma_canonica"]

    if forma.startswith("(x") or forma.startswith("x"):
        # Parábola vertical: (x - h)² = p(y - k)
        if p > 0:
            orientacion = "arriba"
        else:
            orientacion = "abajo"
    else:
        # Parábola horizontal: (y - k)² = p(x - h)
        if p > 0:
            orientacion = "derecha"
        else:
            orientacion = "izquierda"

    elementos = {
        "vertice"    : (h, k),
        "p"          : p,
        "orientacion": orientacion
    }

    descripcion = []
    descripcion.append("=== Elementos de la Parábola ===")
    descripcion.append("")
    descripcion.append(f"Vértice     : ({formatear_num(h)}, {formatear_num(k)})")
    descripcion.append(f"Parámetro p : {formatear_num(p)}")
    descripcion.append(f"Orientación : abre hacia {orientacion}")

    return {
        "tipo"        : "Parabola",
        "elementos"   : elementos,
        "descripcion" : "\n".join(descripcion)
    }
