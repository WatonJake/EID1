# src/interfaz/app.py
from src.conicas.procedimiento_conica import ProcedimientoConica

# =================================================================
# FUTURAS IMPORTACIONES (Descomentar cuando estén listas)
# =================================================================
# -- Integrante 1 (RUT y Tramos) --
# from src.rut.validador_rut import validar_rut, obtener_procedimiento_rut
# from src.limites.funciones_tramos import generar_funcion_por_tramos, generar_puntos_cercanos, generar_procedimiento_funcion

# -- Integrante 2 (Cónicas) --
# from src.conicas.coeficientes import calcular_coeficientes
# from src.conicas.clasificador_conica import clasificar_conica
# from src.conicas.transformacion import transformar_a_canonica, obtener_elementos_conica


class App:
    def __init__(self):
        pass

    def _obtener_rut_valido(self):
        """Maneja los errores de entrada del usuario."""
        while True:
            rut_input = input("\nIngrese su RUT (ejemplo: 12345678-9): ").strip()
            
            if not rut_input:
                print("[!] Error: El RUT no puede estar vacío. Intente nuevamente.")
                continue
            
            # Validar que solo contenga caracteres permitidos
            caracteres_validos = "0123456789kK-."
            es_valido = True
            for char in rut_input:
                if char not in caracteres_validos:
                    es_valido = False
                    break
            
            if not es_valido:
                print("[!] Error: Contiene caracteres inválidos. Use solo números, puntos, guión y la letra K.")
                continue
                
            return rut_input

    def ejecutar(self):
        print("="*60)
        print(" SISTEMA DE ANÁLISIS DE CÓNICAS Y FUNCIONES POR TRAMOS")
        print("="*60)

        rut_input = self._obtener_rut_valido()

        # ==========================================
        # SECCIÓN 1: VALIDACIÓN DEL RUT
        # ==========================================
        print("\n" + "="*60)
        print(" SECCIÓN 1: VALIDACIÓN DEL RUT")
        print("="*60)
        
        es_valido, procedimiento_rut = self._mock_validar_rut(rut_input)
        print(procedimiento_rut)
        
        if not es_valido:
            print("\n[!] EL PROGRAMA SE DETENDRÁ: El RUT ingresado es inválido.")
            return
        
        print("\n[+] RUT Válido. Continuando con el análisis...")

        # Extracción de dígitos (Lógica propia sin librerías)
        rut_limpio = ""
        for char in rut_input:
            if char != "." and char != "-":
                rut_limpio += char
        
        rut_limpio = rut_limpio.upper()
        cuerpo_rut = rut_limpio[:-1]
        dv = rut_limpio[-1]

        if len(cuerpo_rut) < 8:
            cuerpo_rut = ("0" * (8 - len(cuerpo_rut))) + cuerpo_rut
        elif len(cuerpo_rut) > 8:
            cuerpo_rut = cuerpo_rut[-8:]

        digitos = [int(d) for d in cuerpo_rut]

        if dv == 'K': v = 10
        elif dv == '0': v = 11
        else: v = int(dv)

        # ==========================================
        # SECCIÓN 2: ANÁLISIS DE LA CÓNICA
        # ==========================================
        print("\n" + "="*60)
        print(" SECCIÓN 2: ANÁLISIS DE LA CÓNICA")
        print("="*60)
        
        reporte_conica = self._mock_calcular_conica(digitos, v)
        reporte_conica.imprimir_reporte()

        # ==========================================
        # SECCIÓN 3: FORMA CANÓNICA
        # ==========================================
        print("\n" + "="*60)
        print(" SECCIÓN 3: FORMA CANÓNICA")
        print("="*60)
        
        datos_canonica = self._mock_transformar_a_canonica(reporte_conica)
        if datos_canonica:
            print(f"Ecuación Canónica : {datos_canonica['ecuacion']}")
            print("Elementos Geométricos:")
            for elemento, valor in datos_canonica['elementos'].items():
                print(f"  - {elemento}: {valor}")
        else:
            print("  [!] La forma canónica no está disponible para esta cónica.")

        # ==========================================
        # SECCIÓN 4: FUNCIÓN POR TRAMOS
        # ==========================================
        print("\n" + "="*60)
        print(" SECCIÓN 4: FUNCIÓN POR TRAMOS")
        print("="*60)
        
        datos_tramos = self._mock_generar_funcion_por_tramos(digitos)
        print(f"Punto crítico de análisis (a) : {datos_tramos['a']}")
        print(f"Cálculo de selección (d8 % 3) : {datos_tramos['modulo']}")
        print(f"Tipo de discontinuidad        : {datos_tramos['tipo_discontinuidad']}")
        print("-" * 50)
        print("Función por tramos generada:")
        print(datos_tramos['funcion_str'])
        print("-" * 50)
        print("Evidencia computacional (Valores cercanos a 'a'):")
        for x_val, fx_val in datos_tramos['tabla_valores'].items():
            print(f"  f({x_val}) = {fx_val}")
        
        print("\n" + "="*60)
        print(" FIN DEL ANÁLISIS ".center(60, "="))
        print("="*60 + "\n")


    # =================================================================
    # ZONA DE MOCKS (Simulaciones de las funciones de tus compañeros)
    # =================================================================

    def _mock_validar_rut(self, rut):
        procedimiento = "Paso 1: Multiplicar dígitos...\nPaso 2: Sumar resultados...\nPaso 3: Calcular módulo 11...\nResultado: El DV coincide."
        return True, procedimiento

    def _mock_calcular_conica(self, digitos, v):
        coef_ini = {'A': 2.5, 'B': 2.5, 'C': -10, 'D': -12, 'E': 15}
        coef_fin = {'A': 2.5, 'B': -2.5, 'C': -10, 'D': -12, 'E': 15}
        reglas = ["d8 es impar, se reemplazó B por -B (Aparición de Hipérbola)."]
        
        return ProcedimientoConica(
            digitos=digitos, v=v,
            coef_iniciales=coef_ini, coef_finales=coef_fin,
            reglas_aplicadas=reglas,
            ecuacion="2.5x^2 - 2.5y^2 - 10x - 12y + 15 = 0",
            tipo_conica="Hipérbola",
            justificacion="A y B tienen signos opuestos."
        )

    def _mock_transformar_a_canonica(self, reporte_conica):
        return {
            'ecuacion': "(x - 2)^2 / 4 - (y + 2.4)^2 / 4 = 1",
            'elementos': {
                'Centro': "(2, -2.4)",
                'Vértices': "(4, -2.4) y (0, -2.4)",
                'Eje Transverso': "y = -2.4"
            }
        }

    def _mock_generar_funcion_por_tramos(self, digitos):
        a = digitos[2] # a = d3
        d8 = digitos[7]
        modulo = d8 % 3
        
        return {
            'a': a,
            'modulo': f"{d8} % 3 = {modulo}",
            'tipo_discontinuidad': "Discontinuidad de Salto",
            'funcion_str': f"f(x) = \n  {{ x + {digitos[1]}, si x < {a} \n  {{ x + {digitos[3]}, si x >= {a}",
            'tabla_valores': {
                f"{a - 0.1:.1f}": a - 0.1 + digitos[1],
                f"{a - 0.01:.2f}": a - 0.01 + digitos[1],
                f"{a + 0.01:.2f}": a + 0.01 + digitos[3],
                f"{a + 0.1:.1f}": a + 0.1 + digitos[3]
            }
        }