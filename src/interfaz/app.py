# src/interfaz/app.py
from src.conicas.procedimiento_conica import ProcedimientoConica

# FUTURAS IMPORTACIONES (Cuando tus compañeros terminen su parte):
# from src.rut.validador_rut import validar_rut
# from src.conicas.coeficientes import calcular_coeficientes
# from src.conicas.clasificador_conica import clasificar_conica

class App:
    def __init__(self):
        pass

    def ejecutar(self):
        print("="*60)
        print(" SISTEMA DE ANÁLISIS DE CÓNICAS Y FUNCIONES POR TRAMOS")
        print("="*60)

        # a) Solicitar al usuario que ingrese su RUT
        rut_input = input("\nIngrese su RUT (ejemplo: 12345678-9): ")

        # b) Llamar a función simulada de validación
        if not self._mock_validar_rut(rut_input):
            print("\n[!] ERROR: El RUT ingresado no es válido según el módulo 11.")
            return

        # c) Mostrar espacio para el "Procedimiento del dígito verificador"
        print("\n--- Procedimiento del dígito verificador ---")
        print("[PLACEHOLDER: Aquí el Integrante 1 imprimirá el paso a paso del módulo 11]")
        print("Resultado: Validación exitosa. El dígito verificador coincide.")

        # d) Extraer los dígitos del RUT y definir la variable auxiliar 'v'
        rut_limpio = ""
        for char in rut_input:
            if char != "." and char != "-":
                rut_limpio += char
        
        rut_limpio = rut_limpio.upper()
        cuerpo_rut = rut_limpio[:-1]
        dv = rut_limpio[-1]

        # Rellenar con ceros a la izquierda si tiene menos de 8 dígitos
        if len(cuerpo_rut) < 8:
            ceros_faltantes = 8 - len(cuerpo_rut)
            cuerpo_rut = ("0" * ceros_faltantes) + cuerpo_rut
        elif len(cuerpo_rut) > 8:
            cuerpo_rut = cuerpo_rut[-8:]

        digitos = []
        for d in cuerpo_rut:
            digitos.append(int(d))

        if dv == 'K':
            v = 10
        elif dv == '0':
            v = 11
        else:
            v = int(dv)

        # e) Llamar a función simulada para calcular coeficientes
        reporte_conica = self._mock_calcular_conica(digitos, v)

        # f) Imprimir en pantalla el flujo completo del procedimiento
        reporte_conica.imprimir_reporte()


    # =================================================================
    # ZONA DE MOCKS: Reemplazar con las funciones de src.rut y src.conicas
    # =================================================================

    def _mock_validar_rut(self, rut):
        """
        MOCK: Simula src/rut/validador_rut.py
        """
        return True

    def _mock_calcular_conica(self, digitos, v):
        """
        MOCK: Simula la orquestación de src/conicas/...
        """
        coeficientes_simulados = {'A': 2.5, 'B': 1.5, 'C': -10, 'D': -12, 'E': 15}
        reglas_simuladas = ["d8 no es impar, no se alteró el signo de B."]
        ecuacion_simulada = "2.5x^2 + 1.5y^2 - 10x - 12y + 15 = 0"
        tipo_simulado = "Elipse"
        justificacion_simulada = "A y B tienen el mismo signo y A != B."

        return ProcedimientoConica(
            digitos=digitos,
            v=v,
            coeficientes=coeficientes_simulados,
            reglas_aplicadas=reglas_simuladas,
            ecuacion=ecuacion_simulada,
            tipo_conica=tipo_simulado,
            justificacion=justificacion_simulada
        )