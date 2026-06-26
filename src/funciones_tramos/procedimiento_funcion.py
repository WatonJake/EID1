"""
Procedimientos paso a paso para el modulo de funciones por tramos.
"""


def generar_procedimiento_funcion(datos_rut, funcion_info):
    a = funcion_info["punto_critico"]
    residuo = datos_rut["d8"] % 3
    caso = funcion_info["caso"]

    lineas = [
        "PROCEDIMIENTO DE ANALISIS DE FUNCION POR TRAMOS",
        "",
        f"d3 = {datos_rut['d3']} -> punto critico a = {a}",
        f"d8 = {datos_rut['d8']} -> d8 % 3 = {residuo}",
        f"Regla aplicada: {funcion_info['regla_usada']}",
        "",
        "Definicion de la funcion:",
        f"  {funcion_info['funcion_def']['izquierda']}",
        f"  {funcion_info['funcion_def']['punto']}",
        f"  {funcion_info['funcion_def']['derecha']}",
    ]

    simplificada = funcion_info["funcion_def"].get("simplificada")
    if simplificada:
        lineas.extend(["", f"  {simplificada}"])

    lineas.extend(["", _analisis_limites(datos_rut, funcion_info, caso)])
    return "\n".join(lineas)


def _analisis_limites(datos_rut, funcion_info, caso):
    a = funcion_info["punto_critico"]

    if caso == "removible":
        d1 = funcion_info["parametros"]["d1"]
        limite = a + d1
        return "\n".join(
            [
                "Analisis de limites:",
                f"  lim x->{a}- f(x) = lim x->{a}- (x + {d1}) = {limite}",
                f"  lim x->{a}+ f(x) = lim x->{a}+ (x + {d1}) = {limite}",
                f"  f({a}) no existe porque el denominador original x - {a} se anula.",
                "  Conclusion: la discontinuidad es removible.",
            ]
        )

    if caso == "salto":
        d2 = funcion_info["parametros"]["d2"]
        d4 = funcion_info["parametros"]["d4"]
        limite_izq = a + d2
        limite_der = a + d4
        existe = "si" if limite_izq == limite_der else "no"
        tipo = funcion_info["tipo_discontinuidad"]
        return "\n".join(
            [
                "Analisis de limites:",
                f"  lim x->{a}- f(x) = lim x->{a}- (x + {d2}) = {limite_izq}",
                f"  lim x->{a}+ f(x) = lim x->{a}+ (x + {d4}) = {limite_der}",
                f"  f({a}) = {limite_der}",
                f"  El limite existe: {existe}.",
                f"  Conclusion: {tipo}.",
            ]
        )

    numerador = funcion_info["parametros"]["d5_mas_1"]
    return "\n".join(
        [
            "Analisis de limites:",
            f"  lim x->{a}- f(x) = lim x->{a}- {numerador}/(x - {a}) = -infinito",
            f"  lim x->{a}+ f(x) = lim x->{a}+ {numerador}/(x - {a}) = +infinito",
            f"  f({a}) no existe porque el denominador x - {a} se anula.",
            "  Conclusion: la discontinuidad es infinita y hay una asintota vertical en x = a.",
        ]
    )


def generar_tabla_procedimiento(datos_rut, funcion_info, puntos_info=None):
    return "\n".join(
        [
            "TABLA RESUMEN DEL PROCEDIMIENTO",
            f"d3 = {datos_rut.get('d3', 0)}",
            f"d8 % 3 = {datos_rut.get('d8', 0) % 3}",
            f"Caso generado: {funcion_info['caso']}",
            f"Clasificacion observada: {funcion_info['tipo_discontinuidad']}",
        ]
    )
