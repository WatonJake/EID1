def calcular_valor_v(dv):
    """
    Calcula la variable auxiliar v según el dígito verificador.

    Reglas:
        Si DV = K, entonces v = 10.
        Si DV = 0, entonces v = 11.
        Si DV está entre 1 y 9, entonces v = DV.

    Parámetro:
        dv: string con el dígito verificador.

    Retorna:
        entero correspondiente al valor de v.
    """

    dv = dv.upper()

    if dv == "K":
        return 10

    if dv == "0":
        return 11

    return int(dv)


def extraer_digitos_rut(cuerpo_rut):
    """
    Extrae los ocho dígitos del cuerpo del RUT.

    Parámetro:
        cuerpo_rut: string con los 8 dígitos del RUT.

    Retorna:
        diccionario con d1, d2, ..., d8.
    """

    return {
        "d1": int(cuerpo_rut[0]),
        "d2": int(cuerpo_rut[1]),
        "d3": int(cuerpo_rut[2]),
        "d4": int(cuerpo_rut[3]),
        "d5": int(cuerpo_rut[4]),
        "d6": int(cuerpo_rut[5]),
        "d7": int(cuerpo_rut[6]),
        "d8": int(cuerpo_rut[7])
    }


def obtener_datos_rut(cuerpo_rut, dv):
    """
    Obtiene todos los datos necesarios del RUT para el modelo matemático.

    Parámetros:
        cuerpo_rut: string con los 8 dígitos del cuerpo del RUT.
        dv: string con el dígito verificador.

    Retorna:
        diccionario con:
            d1, d2, ..., d8
            dv
            v
    """

    digitos = extraer_digitos_rut(cuerpo_rut)
    valor_v = calcular_valor_v(dv)

    datos_rut = {
        "d1": digitos["d1"],
        "d2": digitos["d2"],
        "d3": digitos["d3"],
        "d4": digitos["d4"],
        "d5": digitos["d5"],
        "d6": digitos["d6"],
        "d7": digitos["d7"],
        "d8": digitos["d8"],
        "dv": dv.upper(),
        "v": valor_v
    }

    return datos_rut


def generar_procedimiento_parser(cuerpo_rut, dv):
    """
    Genera una explicación textual de la extracción de dígitos y cálculo de v.

    Parámetros:
        cuerpo_rut: string con los 8 dígitos del RUT.
        dv: string con el dígito verificador.

    Retorna:
        string con el procedimiento.
    """

    datos = obtener_datos_rut(cuerpo_rut, dv)

    procedimiento = []

    procedimiento.append("Extracción de datos del RUT:")
    procedimiento.append("")
    procedimiento.append(f"Cuerpo del RUT = {cuerpo_rut}")
    procedimiento.append(f"Dígito verificador = {dv.upper()}")
    procedimiento.append("")
    procedimiento.append("Dígitos extraídos:")

    procedimiento.append(f"d1 = {datos['d1']}")
    procedimiento.append(f"d2 = {datos['d2']}")
    procedimiento.append(f"d3 = {datos['d3']}")
    procedimiento.append(f"d4 = {datos['d4']}")
    procedimiento.append(f"d5 = {datos['d5']}")
    procedimiento.append(f"d6 = {datos['d6']}")
    procedimiento.append(f"d7 = {datos['d7']}")
    procedimiento.append(f"d8 = {datos['d8']}")

    procedimiento.append("")
    procedimiento.append("Cálculo de la variable auxiliar v:")

    if datos["dv"] == "K":
        procedimiento.append("Como DV = K, entonces v = 10.")
    elif datos["dv"] == "0":
        procedimiento.append("Como DV = 0, entonces v = 11.")
    else:
        procedimiento.append(f"Como DV = {datos['dv']}, entonces v = {datos['v']}.")

    procedimiento.append("")
    procedimiento.append(f"Valor final de v = {datos['v']}")

    return "\n".join(procedimiento)