from src.rut.digito_verificador import calcular_digito_verificador
from src.rut.digito_verificador import generar_procedimiento_dv


def limpiar_rut(rut):
    """
    Limpia el RUT ingresado por el usuario.

    Ejemplos:
        12.345.678-5 -> 123456785
        12345678-5   -> 123456785
        12 345 678 5 -> 123456785

    Parámetro:
        rut: string ingresado por el usuario.

    Retorna:
        string limpio, sin puntos, guion ni espacios.
    """

    rut_limpio = rut.strip()
    rut_limpio = rut_limpio.replace(".", "")
    rut_limpio = rut_limpio.replace("-", "")
    rut_limpio = rut_limpio.replace(" ", "")
    rut_limpio = rut_limpio.upper()

    return rut_limpio


def validar_formato_rut(rut_limpio):
    """
    Valida que el RUT tenga un formato compatible con el proyecto.

    Para este proyecto se exige:
        - 8 dígitos en el cuerpo del RUT.
        - 1 dígito verificador.
        - Total: 9 caracteres.
        - El cuerpo debe contener solo números.
        - El DV puede ser número o K.

    Parámetro:
        rut_limpio: string sin puntos, guion ni espacios.

    Retorna:
        True si el formato es válido.
        False si el formato es inválido.
    """

    if len(rut_limpio) != 9:
        return False

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    if not cuerpo.isdigit():
        return False

    if not (dv.isdigit() or dv == "K"):
        return False

    return True


def separar_cuerpo_dv(rut_limpio):
    """
    Separa el cuerpo del RUT y el dígito verificador.

    Parámetro:
        rut_limpio: string limpio.

    Retorna:
        cuerpo, dv
    """

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    return cuerpo, dv


def validar_rut(rut):
    """
    Valida un RUT chileno usando el algoritmo módulo 11.

    Parámetro:
        rut: string ingresado por el usuario.

    Retorna:
        diccionario con:
            valido
            rut_limpio
            cuerpo
            dv_ingresado
            dv_calculado
            procedimiento
            mensaje
    """

    rut_limpio = limpiar_rut(rut)

    if not validar_formato_rut(rut_limpio):
        return {
            "valido": False,
            "rut_limpio": rut_limpio,
            "cuerpo": "",
            "dv_ingresado": "",
            "dv_calculado": "",
            "procedimiento": "",
            "mensaje": "Formato de RUT inválido. Para este proyecto se requiere un cuerpo de 8 dígitos y un dígito verificador."
        }

    cuerpo, dv_ingresado = separar_cuerpo_dv(rut_limpio)

    dv_calculado = calcular_digito_verificador(cuerpo)
    procedimiento = generar_procedimiento_dv(cuerpo)

    if dv_ingresado == dv_calculado:
        return {
            "valido": True,
            "rut_limpio": rut_limpio,
            "cuerpo": cuerpo,
            "dv_ingresado": dv_ingresado,
            "dv_calculado": dv_calculado,
            "procedimiento": procedimiento,
            "mensaje": "RUT válido. El dígito verificador ingresado coincide con el calculado."
        }

    return {
        "valido": False,
        "rut_limpio": rut_limpio,
        "cuerpo": cuerpo,
        "dv_ingresado": dv_ingresado,
        "dv_calculado": dv_calculado,
        "procedimiento": procedimiento,
        "mensaje": "RUT inválido. El dígito verificador ingresado no coincide con el calculado."
    }