def calcular_digito_verificador(cuerpo_rut):
    """
    Calcula el dígito verificador de un RUT chileno usando módulo 11.

    Parámetro:
        cuerpo_rut: string con los 8 dígitos del cuerpo del RUT.

    Retorna:
        string con el dígito verificador calculado.
        Puede ser '0', '1', ..., '9' o 'K'.
    """

    suma = 0
    multiplicador = 2

    for digito in reversed(cuerpo_rut):
        suma += int(digito) * multiplicador

        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    resultado = 11 - resto

    if resultado == 11:
        return "0"
    elif resultado == 10:
        return "K"
    else:
        return str(resultado)


def generar_procedimiento_dv(cuerpo_rut):
    """
    Genera el procedimiento paso a paso del cálculo del dígito verificador.

    Parámetro:
        cuerpo_rut: string con los 8 dígitos del cuerpo del RUT.

    Retorna:
        string con el desarrollo completo del cálculo.
    """

    procedimiento = []
    suma = 0
    multiplicador = 2

    procedimiento.append("Procedimiento para calcular el dígito verificador:")
    procedimiento.append("")
    procedimiento.append("Se toman los dígitos del RUT de derecha a izquierda.")
    procedimiento.append("Se multiplican por la secuencia 2, 3, 4, 5, 6, 7 y se repite si es necesario.")
    procedimiento.append("")

    for digito in reversed(cuerpo_rut):
        producto = int(digito) * multiplicador
        suma += producto

        procedimiento.append(
            f"{digito} x {multiplicador} = {producto}"
        )

        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    resultado = 11 - resto

    procedimiento.append("")
    procedimiento.append(f"Suma total = {suma}")
    procedimiento.append(f"Resto de {suma} dividido en 11 = {resto}")
    procedimiento.append(f"11 - {resto} = {resultado}")

    if resultado == 11:
        dv = "0"
        procedimiento.append("Como el resultado es 11, el dígito verificador es 0.")
    elif resultado == 10:
        dv = "K"
        procedimiento.append("Como el resultado es 10, el dígito verificador es K.")
    else:
        dv = str(resultado)
        procedimiento.append(f"Como el resultado es {resultado}, el dígito verificador es {dv}.")

    procedimiento.append("")
    procedimiento.append(f"Dígito verificador calculado = {dv}")

    return "\n".join(procedimiento)