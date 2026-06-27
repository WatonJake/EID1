"""
Modulo para generar funciones por tramos alineadas con la pauta del EID.
"""


def generar_funcion_por_tramos(datos_rut):
    """
    Genera la funcion por tramos definida por la pauta a partir del RUT.
    """

    d1 = datos_rut.get("d1", 0)
    d2 = datos_rut.get("d2", 0)
    d3 = datos_rut.get("d3", 0)
    d4 = datos_rut.get("d4", 0)
    d5 = datos_rut.get("d5", 0)
    d8 = datos_rut.get("d8", 0)

    a = d3
    residuo = d8 % 3

    if residuo == 0:
        limite = a + d1
        return {
            "caso": "removible",
            "tipo_discontinuidad": "Discontinuidad Removible",
            "punto_critico": a,
            "regla_usada": f"d8 % 3 = {residuo} (multiplo de 3) -> caso removible.",
            "parametros": {
                "d1": d1,
            },
            "funcion_def": {
                "izquierda": f"f(x) = ((x - {a})(x + {d1})) / (x - {a}), para x < {a}",
                "punto": f"f({a}) no esta definida porque el denominador se anula en x = {a}.",
                "derecha": f"f(x) = ((x - {a})(x + {d1})) / (x - {a}), para x > {a}",
                "simplificada": f"Para x != {a}, la expresion se simplifica a f(x) = x + {d1}.",
            },
            "descripcion": (
                f"Se genera el caso removible con la funcion racional "
                f"((x - {a})(x + {d1})) / (x - {a}). "
                f"Al simplificar para x != {a}, queda x + {d1}. "
                f"Los limites laterales coinciden en {limite}, pero f({a}) no existe."
            ),
        }

    if residuo == 1:
        limite_izq = a + d2
        limite_der = a + d4
        if limite_izq != limite_der:
            tipo = "Discontinuidad de Salto"
        else:
            tipo = "Continua en el punto critico"
        return {
            "caso": "salto",
            "tipo_discontinuidad": tipo,
            "punto_critico": a,
            "regla_usada": f"d8 % 3 = {residuo} (residuo 1) -> caso por tramos lineal.",
            "parametros": {
                "d2": d2,
                "d4": d4,
            },
            "funcion_def": {
                "izquierda": f"f(x) = x + {d2}, para x < {a}",
                "punto": f"f({a}) = {a} + {d4} = {limite_der}, porque el segundo tramo incluye x >= {a}.",
                "derecha": f"f(x) = x + {d4}, para x >= {a}",
            },
            "descripcion": (
                f"Se genera el caso por tramos lineal con x + {d2} a la izquierda y x + {d4} "
                f"a la derecha del punto critico x = {a}. "
                f"El limite izquierdo vale {limite_izq} y el derecho vale {limite_der}."
            ),
        }

    numerador = d5 + 1
    return {
        "caso": "infinita",
        "tipo_discontinuidad": "Discontinuidad Infinita",
        "punto_critico": a,
        "regla_usada": f"d8 % 3 = {residuo} (residuo 2) -> caso de discontinuidad infinita.",
        "parametros": {
            "d5_mas_1": numerador,
        },
        "funcion_def": {
            "izquierda": f"f(x) = {numerador} / (x - {a}), para x < {a}",
            "punto": f"f({a}) no esta definida porque el denominador se anula en x = {a}.",
            "derecha": f"f(x) = {numerador} / (x - {a}), para x > {a}",
        },
        "descripcion": (
            f"Se genera la funcion racional {numerador} / (x - {a}). "
            f"Como el numerador es positivo y el denominador cambia de signo al cruzar x = {a}, "
            f"la funcion tiende a -infinito por la izquierda y a +infinito por la derecha."
        ),
    }
