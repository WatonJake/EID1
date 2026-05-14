from src.rut.validador_rut import validar_rut
from src.rut.parser_rut import obtener_datos_rut
from src.rut.parser_rut import generar_procedimiento_parser


rut = input("Ingrese un RUT: ")

resultado = validar_rut(rut)

print("")
print("Resultado de validación:")
print(resultado["mensaje"])

print("")
print(resultado["procedimiento"])

if resultado["valido"]:
    datos = obtener_datos_rut(
        resultado["cuerpo"],
        resultado["dv_ingresado"]
    )

    procedimiento_parser = generar_procedimiento_parser(
        resultado["cuerpo"],
        resultado["dv_ingresado"]
    )

    print("")
    print(procedimiento_parser)

    print("")
    print("Datos finales del RUT:")
    print(datos)
else:
    print("")
    print("No se pueden extraer los datos porque el RUT no es válido.")