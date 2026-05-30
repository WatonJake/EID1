from src.conicas.canonica import transformar_a_canonica
from src.conicas.clasificador_conica import clasificar_conica
from src.conicas.coeficientes import calcular_coeficientes
from src.conicas.elementos_conica import obtener_elementos_conica
from src.conicas.procedimiento_conica import ProcedimientoConica
from src.conicas.reglas_conica import aplicar_reglas_especiales
from src.funciones_tramos import (
    evaluar_en_tabla,
    generar_funcion_por_tramos,
    generar_procedimiento_funcion,
    generar_puntos_cercanos,
)
from src.rut.parser_rut import generar_procedimiento_parser, obtener_datos_rut
from src.rut.validador_rut import validar_rut


class App:
    def _obtener_rut_valido(self):
        """Obtiene una entrada con caracteres validos para el RUT."""
        while True:
            rut_input = input("\nIngrese su RUT (ejemplo: 12345678-9): ").strip()

            if not rut_input:
                print("[!] Error: El RUT no puede estar vacio. Intente nuevamente.")
                continue

            caracteres_validos = "0123456789kK-. "
            if any(char not in caracteres_validos for char in rut_input):
                print("[!] Error: Use solo numeros, puntos, guion, espacios y la letra K.")
                continue

            return rut_input

    def ejecutar(self):
        print("=" * 60)
        print(" SISTEMA DE ANALISIS DE CONICAS Y FUNCIONES POR TRAMOS")
        print("=" * 60)

        rut_input = self._obtener_rut_valido()

        print("\n" + "=" * 60)
        print(" SECCION 1: VALIDACION DEL RUT")
        print("=" * 60)

        resultado_rut = validar_rut(rut_input)
        print(resultado_rut["mensaje"])

        if resultado_rut["procedimiento"]:
            print("")
            print(resultado_rut["procedimiento"])

        if not resultado_rut["valido"]:
            print("\n[!] EL PROGRAMA SE DETENDRA: El RUT ingresado es invalido.")
            return

        datos_rut = obtener_datos_rut(
            resultado_rut["cuerpo"],
            resultado_rut["dv_ingresado"],
        )

        print("")
        print(generar_procedimiento_parser(resultado_rut["cuerpo"], resultado_rut["dv_ingresado"]))

        digitos = [datos_rut[f"d{i}"] for i in range(1, 9)]
        v = datos_rut["v"]

        print("\n" + "=" * 60)
        print(" SECCION 2: ANALISIS DE LA CONICA")
        print("=" * 60)

        reporte_conica = self._calcular_conica(digitos, v)
        reporte_conica.imprimir_reporte()

        print("\n" + "=" * 60)
        print(" SECCION 3: FORMA CANONICA")
        print("=" * 60)

        datos_canonica = self._transformar_a_canonica(reporte_conica)
        if datos_canonica is None:
            print("[!] La forma canonica no esta disponible para esta conica.")
        else:
            print(f"Ecuacion canonica : {datos_canonica['forma_canonica']}")

            pasos = datos_canonica.get("pasos")
            if pasos:
                print("")
                print(pasos)

            descripcion = datos_canonica.get("descripcion_elementos")
            if descripcion:
                print("")
                print(descripcion)

        print("\n" + "=" * 60)
        print(" SECCION 4: FUNCION POR TRAMOS")
        print("=" * 60)

        self._mostrar_funcion_por_tramos(datos_rut)

        print("\n" + "=" * 60)
        print(" FIN DEL ANALISIS ".center(60, "="))
        print("=" * 60 + "\n")

    def _calcular_conica(self, digitos, v):
        a_inicial, b_inicial, c, d, e = calcular_coeficientes(digitos, v)
        a_final, b_final = aplicar_reglas_especiales(a_inicial, b_inicial, digitos)

        reglas_aplicadas = self._describir_reglas(a_inicial, b_inicial, a_final, b_final, digitos)
        tipo_conica = clasificar_conica(a_final, b_final)

        coef_iniciales = {
            "A": a_inicial,
            "B": b_inicial,
            "C": c,
            "D": d,
            "E": e,
        }
        coef_finales = {
            "A": a_final,
            "B": b_final,
            "C": c,
            "D": d,
            "E": e,
        }

        return ProcedimientoConica(
            digitos=digitos,
            v=v,
            coef_iniciales=coef_iniciales,
            coef_finales=coef_finales,
            reglas_aplicadas=reglas_aplicadas,
            ecuacion=self._formatear_ecuacion_general(a_final, b_final, c, d, e),
            tipo_conica=tipo_conica,
            justificacion=self._justificar_conica(tipo_conica, a_final, b_final),
        )

    def _transformar_a_canonica(self, reporte_conica):
        if reporte_conica.tipo_conica == "Indeterminada":
            return None

        coef = reporte_conica.coef_finales
        datos = transformar_a_canonica(
            (
                coef["A"],
                coef["B"],
                coef["C"],
                coef["D"],
                coef["E"],
            ),
            reporte_conica.tipo_conica,
        )

        if not datos or "forma_canonica" not in datos:
            return None

        if self._conica_no_real(datos, reporte_conica.tipo_conica):
            datos["descripcion_elementos"] = "La ecuacion no genera una conica real con estos coeficientes."
            datos["elementos"] = {}
            return datos

        elementos = obtener_elementos_conica(datos, reporte_conica.tipo_conica)
        datos["descripcion_elementos"] = elementos.get("descripcion", "")
        datos["elementos"] = elementos.get("elementos", {})
        return datos

    def _mostrar_funcion_por_tramos(self, datos_rut):
        funcion_info = generar_funcion_por_tramos(datos_rut)
        procedimiento = generar_procedimiento_funcion(datos_rut, funcion_info)
        puntos_info = generar_puntos_cercanos(funcion_info["punto_critico"])
        tabla = evaluar_en_tabla(
            puntos_info,
            self._crear_evaluador_funcion(datos_rut, funcion_info),
        )

        print(f"Punto critico de analisis (a) : {funcion_info['punto_critico']}")
        print(f"Regla de seleccion            : {self._texto_consola(funcion_info['regla_usada'])}")
        print(f"Tipo de discontinuidad        : {self._texto_consola(funcion_info['tipo_discontinuidad'])}")
        print("-" * 50)
        print("Funcion por tramos generada:")
        for clave in ("izquierda", "punto", "derecha"):
            print(f"  {self._texto_consola(funcion_info['funcion_def'][clave])}")

        print("-" * 50)
        print("Procedimiento detallado:")
        print(self._texto_consola(procedimiento))

        print("-" * 50)
        print("Evidencia computacional (valores cercanos a 'a'):")
        for punto in tabla:
            x_val = self._formatear_numero(punto["x"])
            if punto["f(x)"] is None:
                fx_val = "No definida"
            else:
                fx_val = self._formatear_numero(punto["f(x)"])

            print(f"  x = {x_val:>8} | {punto['posicion']:<14} | f(x) = {fx_val}")

    def _crear_evaluador_funcion(self, datos_rut, funcion_info):
        a = funcion_info["punto_critico"]
        residuo = datos_rut["d8"] % 3

        if residuo == 0:
            def evaluar(x):
                if x == a:
                    raise ValueError("Funcion no definida en el punto critico.")
                return (x ** 2) + 1

            return evaluar

        if residuo == 1:
            def evaluar(x):
                if x <= a:
                    return (2 * x) + 1
                return x + 5

            return evaluar

        def evaluar(x):
            if x == a:
                raise ValueError("Funcion no definida en el punto critico.")
            return 1 / (x - a)

        return evaluar

    def _describir_reglas(self, a_inicial, b_inicial, a_final, b_final, digitos):
        d1, d2, d3, d4, d5, d6, d7, d8 = digitos
        reglas = []

        if d8 % 2 != 0:
            reglas.append("d8 es impar, por lo tanto B cambia de signo.")

        if d1 == d2:
            reglas.append("d1 es igual a d2, por lo tanto B toma el valor de A.")

        if (d5 + d6) % 3 == 0:
            if d7 % 2 == 0:
                reglas.append("d5 + d6 es multiplo de 3 y d7 es par, por lo tanto B = 0.")
            else:
                reglas.append("d5 + d6 es multiplo de 3 y d7 es impar, por lo tanto A = 0.")

        if not reglas and a_inicial == a_final and b_inicial == b_final:
            reglas.append("No se aplicaron reglas especiales.")

        return reglas

    def _justificar_conica(self, tipo_conica, a_coef, b_coef):
        if tipo_conica == "Circunferencia":
            return f"A = B = {self._formatear_numero(a_coef)} y ambos son distintos de 0."
        if tipo_conica == "Elipse":
            return "A y B tienen el mismo signo, pero valores distintos."
        if tipo_conica == "Hiperbola":
            return "A y B tienen signos opuestos."
        if tipo_conica == "Parabola":
            return "Uno de los coeficientes cuadraticos es 0 y el otro es distinto de 0."
        return "Los coeficientes no cumplen una condicion clasica de conica."

    def _conica_no_real(self, datos_canonica, tipo_conica):
        if tipo_conica == "Circunferencia":
            return datos_canonica.get("radio_cuadrado", 0) < 0

        if tipo_conica == "Elipse":
            return (
                datos_canonica.get("a_cuadrado", 0) <= 0
                or datos_canonica.get("b_cuadrado", 0) <= 0
            )

        return False

    def _formatear_ecuacion_general(self, a_coef, b_coef, c_coef, d_coef, e_coef):
        terminos = [
            self._formatear_termino(a_coef, "x^2", primero=True),
            self._formatear_termino(b_coef, "y^2"),
            self._formatear_termino(c_coef, "x"),
            self._formatear_termino(d_coef, "y"),
            self._formatear_termino(e_coef, ""),
        ]
        ecuacion = "".join(termino for termino in terminos if termino)
        return f"{ecuacion} = 0"

    def _formatear_termino(self, coeficiente, variable, primero=False):
        if coeficiente == 0:
            return ""

        valor = self._formatear_numero(abs(coeficiente))
        termino = f"{valor}{variable}" if variable else valor

        if primero:
            return f"-{termino}" if coeficiente < 0 else termino

        signo = " - " if coeficiente < 0 else " + "
        return f"{signo}{termino}"

    def _formatear_numero(self, numero):
        if isinstance(numero, int):
            return str(numero)
        if float(numero).is_integer():
            return str(int(numero))
        return f"{numero:.4f}"

    def _texto_consola(self, texto):
        reemplazos = {
            "→": "->",
            "∞": "infinito",
            "≤": "<=",
            "≥": ">=",
            "≠": "!=",
            "•": "-",
            "┌": "+",
            "┐": "+",
            "└": "+",
            "┘": "+",
            "├": "+",
            "┤": "+",
            "┬": "+",
            "┴": "+",
            "┼": "+",
            "─": "-",
            "│": "|",
            "╔": "+",
            "╗": "+",
            "╚": "+",
            "╝": "+",
            "╠": "+",
            "╣": "+",
            "╦": "+",
            "╩": "+",
            "╬": "+",
            "═": "=",
            "║": "|",
            "⁻": "-",
            "₊": "+",
        }

        for origen, destino in reemplazos.items():
            texto = texto.replace(origen, destino)

        return texto.encode("cp1252", errors="replace").decode("cp1252")
