# salida.py
# funciones de impresion separadas por proceso
# en el futuro se pueden reemplazar por una interfaz grafica


# separador visual

def imprimir_separador():
    print("")
    print("-" * 40)
    print("")


# validacion del rut

def imprimir_resultado_validacion(resultado_validacion):
    print("")
    print(resultado_validacion["mensaje"])


def imprimir_procedimiento_dv(resultado_validacion):
    print("")
    print(resultado_validacion["procedimiento"])


def imprimir_rut_invalido():
    print("")
    print("no se pueden extraer los datos porque el rut no es valido.")


# extraccion de digitos (parser)

def imprimir_procedimiento_parser(procedimiento_parser):
    print("")
    print(procedimiento_parser)


def imprimir_datos_rut(datos_rut):
    print("")
    print("datos extraidos del rut:")
    for clave, valor in datos_rut.items():
        print(f"  {clave} = {valor}")


# coeficientes de la conica

def imprimir_coeficientes(A, B, C, D, E):
    print("")
    print("coeficientes de la conica:")
    print(f"  A = {A}")
    print(f"  B = {B}")
    print(f"  C = {C}")
    print(f"  D = {D}")
    print(f"  E = {E}")


def imprimir_tipo_conica(tipo_conica):
    print("")
    print(f"tipo de conica: {tipo_conica}")


# forma canonica

def imprimir_procedimiento_canonica(datos_canonica):
    print("")
    print(datos_canonica["pasos"])


def imprimir_forma_canonica(datos_canonica):
    print("")
    print("forma canonica:")
    print(f"  {datos_canonica['forma_canonica']}")


# elementos geometricos

def imprimir_elementos_conica(resultado_elementos):
    print("")
    print(resultado_elementos["descripcion"])
