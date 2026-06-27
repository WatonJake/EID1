from tkinter import messagebox

from src.conicas.canonica import transformar_a_canonica
from src.conicas.clasificador_conica import clasificar_conica
from src.conicas.coeficientes import calcular_coeficientes
from src.conicas.elementos_conica import obtener_elementos_conica
from src.conicas.procedimiento_conica import ProcedimientoConica
from src.conicas.reglas_conica import aplicar_reglas_especiales
from src.funciones_tramos import evaluar_en_tabla, generar_funcion_por_tramos, generar_puntos_cercanos
from src.rut.parser_rut import generar_procedimiento_parser, obtener_datos_rut
from src.rut.validador_rut import validar_rut
from src.utilidades.matematica_manual import raiz_cuadrada, valor_absoluto


class AnalysisMixin:
    def _analizar(self):
        rut_input = self.rut_var.get().strip()
        if not rut_input:
            messagebox.showerror("RUT requerido", "Debe ingresar un RUT antes de analizar.")
            return

        try:
            resultado_rut = validar_rut(rut_input)
            resumen_validacion = [
                "SECCIN 1: VALIDACIN DEL RUT",
                resultado_rut["mensaje"],
            ]
            if resultado_rut["procedimiento"]:
                resumen_validacion.extend(["", resultado_rut["procedimiento"]])

            if not resultado_rut["valido"]:
                self._cargar_estado_invalido("\n".join(resumen_validacion))
                return

            datos_rut = obtener_datos_rut(resultado_rut["cuerpo"], resultado_rut["dv_ingresado"])
            parser_texto = generar_procedimiento_parser(
                resultado_rut["cuerpo"], resultado_rut["dv_ingresado"]
            )

            digitos = [datos_rut[f"d{i}"] for i in range(1, 9)]
            reporte_conica = self._calcular_conica(digitos, datos_rut["v"])
            datos_canonica = self._transformar_a_canonica(reporte_conica)
            descripcion_conica = self._describir_conica_completa(
                reporte_conica.tipo_conica, datos_canonica
            )
            analisis_funcion = self._analizar_funcion_por_tramos(datos_rut)

            self.resumen_label.configure(
                text=self._construir_resumen_general(
                    resultado_rut,
                    datos_rut,
                    reporte_conica,
                    datos_canonica,
                    analisis_funcion,
                )
            )
            self.estado_var.set("Análisis completo. Revise procedimiento, gráficos e inputs de defensa.")

            self._actualizar_estado_visual(
                "Análisis completo. Revisa el resumen rápido y luego entra a las pestañas para el desarrollo y la defensa.",
                "exito",
            )
            self._actualizar_metricas(
                rut="Válido",
                conica=reporte_conica.tipo_conica,
                canonica=self._resumir_forma_canonica(datos_canonica),
                funcion=analisis_funcion["funcion_info"]["tipo_discontinuidad"],
            )

            self._escribir_texto(
                self.tarjetas_resumen,
                "\n".join(
                    [
                        "\n".join(resumen_validacion),
                        "",
                        "SECCIN 2: EXTRACCIN DE DÍGITOS Y VARIABLE AUXILIAR",
                        parser_texto,
                        "",
                        "SECCIN 3: RESUMEN DE LA CNICA",
                        reporte_conica.generar_reporte(),
                        "",
                        "SECCIN 4: RESUMEN DE FUNCIN POR TRAMOS",
                        analisis_funcion["resumen_texto"],
                    ]
                ),
            )

            self._escribir_texto(
                self.tarjetas_conicas,
                "\n".join(
                    [
                        "SECCIN CNICAS",
                        "",
                        "1. Construcción de coeficientes",
                        self._procedimiento_coeficientes(datos_rut),
                        "",
                        "2. Aplicación de reglas especiales y clasificación",
                        reporte_conica.generar_reporte(),
                        "",
                        "3. Transformación a forma canónica",
                        self._texto_canonica(datos_canonica),
                        "",
                        "4. Elementos geométricos y lectura de la gráfica",
                        descripcion_conica["texto"],
                        "",
                        "5. Procedimiento inverso hacia la ecuación general",
                        self._generar_procedimiento_inverso(reporte_conica, datos_canonica),
                    ]
                ),
            )

            self._escribir_texto(
                self.tarjetas_funciones,
                "\n".join(
                    [
                        "SECCIN FUNCIONES POR TRAMOS",
                        "",
                        analisis_funcion["procedimiento"],
                        "",
                        "Tabla de valores cercanos al punto crítico",
                        analisis_funcion["tabla_texto"],
                    ]
                ),
            )

            self._dibujar_conica(reporte_conica.tipo_conica, datos_canonica)
            self._dibujar_funcion(analisis_funcion)
            self._crear_campos_vacios(self.frame_inputs_conica, descripcion_conica["campos"])
            self._crear_campos_vacios(
                self.frame_inputs_funcion,
                [
                    "Límite por izquierda",
                    "Límite por derecha",
                    "¿Existe el límite?",
                    "Valor de la función en a",
                    "¿Es continua?",
                    "Tipo de discontinuidad",
                    "Justificación escrita",
                ],
            )
            self.campos_defensa_conica = descripcion_conica["campos"]
            self.campos_defensa_funcion = [
                "Límite por izquierda",
                "Límite por derecha",
                "¿Existe el límite?",
                "Valor de la función en a",
                "¿Es continua?",
                "Tipo de discontinuidad",
                "Justificación escrita",
            ]
            if self.frame_defensa_conica is not None:
                self._crear_campos_vacios(self.frame_defensa_conica, self.campos_defensa_conica)
            if self.frame_defensa_funcion is not None:
                self._crear_campos_vacios(self.frame_defensa_funcion, self.campos_defensa_funcion)
            self._actualizar_tabla(analisis_funcion["tabla"])

            self.current_reporte_conica = reporte_conica
            self.current_datos_canonica = datos_canonica
            self.current_analisis_funcion = analisis_funcion
        except Exception as error:
            self._actualizar_estado_visual("Se produjo un error al procesar el análisis.", "error")
            self._actualizar_metricas(
                rut="Error",
                conica="Sin resultado",
                canonica="Sin resultado",
                funcion="Sin resultado",
            )
            self.estado_var.set("Se produjo un error al procesar el análisis.")
            messagebox.showerror("Error de análisis", str(error))

    def _actualizar_estado_visual(self, mensaje, estado):
        self.estado_var.set("")
        colores_estado = {
            "exito": self.colores["exito"],
            "error": self.colores["error"],
            "aviso": self.colores["aviso"],
        }
        if getattr(self, "estado_badge", None) is not None:
            self.estado_badge.configure(fg_color=colores_estado.get(estado, self.colores["aviso"]))
            self.estado_badge.grid_remove()

    def _actualizar_metricas(self, rut=None, conica=None, canonica=None, funcion=None):
        valores = {
            "rut": rut,
            "conica": conica,
            "canonica": canonica,
            "funcion": funcion,
        }
        for clave, valor in valores.items():
            if valor is not None and clave in self.metricas:
                self.metricas[clave].configure(text=valor)

    def _resumir_forma_canonica(self, datos_canonica):
        if not datos_canonica:
            return "No disponible"
        forma = self._limpiar_texto(datos_canonica.get("forma_canonica", "No disponible"))
        return forma if len(forma) <= 44 else f"{forma[:41]}..."

    def _calcular_conica(self, digitos, v):
        a_inicial, b_inicial, c, d, e = calcular_coeficientes(digitos, v)
        a_final, b_final = aplicar_reglas_especiales(a_inicial, b_inicial, digitos)
        reglas_aplicadas = self._describir_reglas(a_inicial, b_inicial, a_final, b_final, digitos)
        tipo_conica = clasificar_conica(a_final, b_final)
        return ProcedimientoConica(
            digitos=digitos,
            v=v,
            coef_iniciales={"A": a_inicial, "B": b_inicial, "C": c, "D": d, "E": e},
            coef_finales={"A": a_final, "B": b_final, "C": c, "D": d, "E": e},
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
            (coef["A"], coef["B"], coef["C"], coef["D"], coef["E"]),
            reporte_conica.tipo_conica,
        )
        if not datos or "forma_canonica" not in datos:
            return None
        forma = datos.get("forma_canonica", "")
        if forma.startswith("No fue posible"):
            return datos
        if self._conica_no_real(datos, reporte_conica.tipo_conica):
            datos["descripcion_elementos"] = "La ecuación no representa una cónica real."
            datos["elementos"] = {}
            return datos
        elementos = obtener_elementos_conica(datos, reporte_conica.tipo_conica)
        datos["descripcion_elementos"] = elementos.get("descripcion", "")
        datos["elementos"] = elementos.get("elementos", {})
        return datos

    def _describir_conica_completa(self, tipo_conica, datos_canonica):
        if not datos_canonica or "forma_canonica" not in datos_canonica:
            return {
                "texto": "No fue posible obtener la forma canónica.",
                "campos": ["Centro", "Vértices", "Focos", "Ejes", "Asíntotas o directriz"],
            }
        if datos_canonica["forma_canonica"].startswith("No fue posible"):
            return {
                "texto": datos_canonica["forma_canonica"],
                "campos": ["Centro", "Vértices", "Focos", "Ejes", "Asíntotas o directriz"],
            }
        if tipo_conica == "Circunferencia":
            centro = datos_canonica["centro"]
            radio = datos_canonica["radio"]
            return {
                "texto": "\n".join(
                    [f"Centro: {self._formatear_punto(centro)}", f"Radio: {self._formatear_numero(radio)}"]
                ),
                "campos": ["Centro", "Radio"],
            }
        if tipo_conica == "Elipse":
            centro = datos_canonica["centro"]
            a2 = datos_canonica["a_cuadrado"]
            b2 = datos_canonica["b_cuadrado"]
            a = raiz_cuadrada(a2)
            b = raiz_cuadrada(b2)
            if a >= b:
                c = raiz_cuadrada(a2 - b2)
                vertices = [(centro[0] - a, centro[1]), (centro[0] + a, centro[1])]
                focos = [(centro[0] - c, centro[1]), (centro[0] + c, centro[1])]
                ejes = f"Mayor horizontal = {self._formatear_numero(2 * a)} | Menor = {self._formatear_numero(2 * b)}"
            else:
                c = raiz_cuadrada(b2 - a2)
                vertices = [(centro[0], centro[1] - b), (centro[0], centro[1] + b)]
                focos = [(centro[0], centro[1] - c), (centro[0], centro[1] + c)]
                ejes = f"Mayor vertical = {self._formatear_numero(2 * b)} | Menor = {self._formatear_numero(2 * a)}"
            return {
                "texto": "\n".join(
                    [
                        f"Centro: {self._formatear_punto(centro)}",
                        f"Vértices principales: {self._formatear_lista_puntos(vertices)}",
                        f"Focos: {self._formatear_lista_puntos(focos)}",
                        f"Ejes: {ejes}",
                    ]
                ),
                "campos": ["Centro", "Vértices", "Focos", "Ejes"],
            }
        if tipo_conica == "Hiperbola":
            centro = datos_canonica["centro"]
            a2 = datos_canonica["a_cuadrado"]
            b2 = datos_canonica["b_cuadrado"]
            a = raiz_cuadrada(a2)
            b = raiz_cuadrada(b2)
            c = raiz_cuadrada(a2 + b2)
            orientacion = datos_canonica.get("orientacion", "horizontal")
            if orientacion == "horizontal":
                vertices = [(centro[0] - a, centro[1]), (centro[0] + a, centro[1])]
                focos = [(centro[0] - c, centro[1]), (centro[0] + c, centro[1])]
                asintotas = (
                    f"y - {self._formatear_numero(centro[1])} = +/-"
                    f"{self._formatear_numero(b / a)}(x - {self._formatear_numero(centro[0])})"
                )
            else:
                vertices = [(centro[0], centro[1] - a), (centro[0], centro[1] + a)]
                focos = [(centro[0], centro[1] - c), (centro[0], centro[1] + c)]
                asintotas = (
                    f"y - {self._formatear_numero(centro[1])} = +/-"
                    f"{self._formatear_numero(a / b)}(x - {self._formatear_numero(centro[0])})"
                )
            return {
                "texto": "\n".join(
                    [
                        f"Centro: {self._formatear_punto(centro)}",
                        f"Vértices: {self._formatear_lista_puntos(vertices)}",
                        f"Focos: {self._formatear_lista_puntos(focos)}",
                        f"Ejes: transverso = {self._formatear_numero(2 * a)} | conjugado = {self._formatear_numero(2 * b)}",
                        f"Asíntotas: {asintotas}",
                    ]
                ),
                "campos": ["Centro", "Vértices", "Focos", "Ejes", "Asíntotas"],
            }
        if tipo_conica == "Parabola":
            vertice = datos_canonica["vertice"]
            p_estandar = datos_canonica["p"] / 4
            forma = datos_canonica["forma_canonica"]
            if forma.startswith("(x") or forma.startswith("x"):
                foco = (vertice[0], vertice[1] + p_estandar)
                directriz = f"y = {self._formatear_numero(vertice[1] - p_estandar)}"
                eje = f"x = {self._formatear_numero(vertice[0])}"
            else:
                foco = (vertice[0] + p_estandar, vertice[1])
                directriz = f"x = {self._formatear_numero(vertice[0] - p_estandar)}"
                eje = f"y = {self._formatear_numero(vertice[1])}"
            return {
                "texto": "\n".join(
                    [
                        f"Vértice: {self._formatear_punto(vertice)}",
                        f"Foco: {self._formatear_punto(foco)}",
                        f"Eje de simetría: {eje}",
                        f"Directriz: {directriz}",
                    ]
                ),
                "campos": ["Vértice", "Foco", "Eje de simetría", "Directriz"],
            }
        return {
            "texto": "No hay elementos geométricos disponibles para esta cónica.",
            "campos": ["Centro", "Vértices", "Focos", "Ejes", "Asíntotas o directriz"],
        }

    def _construir_resumen_general(
        self,
        resultado_rut,
        datos_rut,
        reporte_conica,
        datos_canonica,
        analisis_funcion,
    ):
        forma_canonica = "No disponible"
        if datos_canonica and datos_canonica.get("forma_canonica"):
            forma_canonica = self._limpiar_texto(datos_canonica["forma_canonica"])
        return "\n".join(
            [
                f"RUT validado: {resultado_rut['rut_limpio']}",
                f"DV calculado: {resultado_rut['dv_calculado']} | variable auxiliar v = {datos_rut['v']}",
                f"Cónica detectada: {reporte_conica.tipo_conica}",
                f"Ecuación general: {reporte_conica.ecuacion}",
                f"Forma canónica: {forma_canonica}",
                f"Función por tramos: {analisis_funcion['funcion_info']['tipo_discontinuidad']} en a = {analisis_funcion['punto_critico']}",
            ]
        )

    def _procedimiento_coeficientes(self, datos_rut):
        return "\n".join(
            [
                "Se usan d1, ..., d8 y la variable auxiliar v para construir:",
                "A = (d1 + d2) / v",
                "B = (d3 + d4) / v",
                "C = -(d5 + d6)",
                "D = -(d7 + d8)",
                "E = d1 + d3 + d5 + d7",
                "",
                f"A = ({datos_rut['d1']} + {datos_rut['d2']}) / {datos_rut['v']} = {self._formatear_numero((datos_rut['d1'] + datos_rut['d2']) / datos_rut['v'])}",
                f"B = ({datos_rut['d3']} + {datos_rut['d4']}) / {datos_rut['v']} = {self._formatear_numero((datos_rut['d3'] + datos_rut['d4']) / datos_rut['v'])}",
                f"C = -({datos_rut['d5']} + {datos_rut['d6']}) = {self._formatear_numero(-(datos_rut['d5'] + datos_rut['d6']))}",
                f"D = -({datos_rut['d7']} + {datos_rut['d8']}) = {self._formatear_numero(-(datos_rut['d7'] + datos_rut['d8']))}",
                f"E = {datos_rut['d1']} + {datos_rut['d3']} + {datos_rut['d5']} + {datos_rut['d7']} = {datos_rut['d1'] + datos_rut['d3'] + datos_rut['d5'] + datos_rut['d7']}",
            ]
        )

    def _texto_canonica(self, datos_canonica):
        if not datos_canonica:
            return "No fue posible transformar la ecuación a forma canónica."
        partes = [f"Forma canónica: {self._limpiar_texto(datos_canonica['forma_canonica'])}"]
        if datos_canonica.get("pasos"):
            partes.extend(["", self._limpiar_texto(datos_canonica["pasos"])])
        if datos_canonica.get("descripcion_elementos"):
            partes.extend(["", self._limpiar_texto(datos_canonica["descripcion_elementos"])])
        return "\n".join(partes)

    def _generar_procedimiento_inverso(self, reporte_conica, datos_canonica):
        if not datos_canonica or not datos_canonica.get("forma_canonica"):
            return "Sin forma canónica no es posible describir el regreso a la ecuación general."
        tipo = reporte_conica.tipo_conica
        if tipo == "Circunferencia":
            return self._inverso_circunferencia(reporte_conica, datos_canonica)
        if tipo == "Elipse":
            return self._inverso_elipse(reporte_conica, datos_canonica)
        if tipo == "Hiperbola":
            return self._inverso_hiperbola(reporte_conica, datos_canonica)
        if tipo == "Parabola":
            return self._inverso_parabola(reporte_conica, datos_canonica)
        return "No hay procedimiento inverso disponible para esta cónica."

    def _inverso_circunferencia(self, reporte_conica, datos_canonica):
        h, k = datos_canonica["centro"]
        r2 = datos_canonica["radio_cuadrado"]
        return "\n".join(
            [
                "Partimos de la forma canónica de la circunferencia:",
                f"({self._texto_desplazamiento('x', h)})^2 + ({self._texto_desplazamiento('y', k)})^2 = {self._formatear_numero(r2)}",
                "",
                "Expandimos ambos cuadrados:",
                f"x^2 {self._signo_lineal(-2 * h, 'x')} + {self._formatear_numero(h * h)} + y^2 {self._signo_lineal(-2 * k, 'y')} + {self._formatear_numero(k * k)} = {self._formatear_numero(r2)}",
                "",
                "Llevamos todo al lado izquierdo y reducimos términos:",
                reporte_conica.ecuacion,
            ]
        )

    def _inverso_elipse(self, reporte_conica, datos_canonica):
        h, k = datos_canonica["centro"]
        a2 = datos_canonica["a_cuadrado"]
        b2 = datos_canonica["b_cuadrado"]
        return "\n".join(
            [
                "Partimos de la forma canónica de la elipse:",
                f"({self._texto_desplazamiento('x', h)})^2/{self._formatear_numero(a2)} + ({self._texto_desplazamiento('y', k)})^2/{self._formatear_numero(b2)} = 1",
                "",
                "Multiplicamos por el mínimo común múltiplo de los denominadores y expandimos:",
                f"b^2(x - h)^2 + a^2(y - k)^2 = a^2 b^2",
                f"{self._formatear_numero(b2)}({self._texto_desplazamiento('x', h)})^2 + {self._formatear_numero(a2)}({self._texto_desplazamiento('y', k)})^2 = {self._formatear_numero(a2 * b2)}",
                "",
                "Expandimos, reunimos términos semejantes y llevamos todo a cero:",
                reporte_conica.ecuacion,
            ]
        )

    def _inverso_hiperbola(self, reporte_conica, datos_canonica):
        h, k = datos_canonica["centro"]
        a2 = datos_canonica["a_cuadrado"]
        b2 = datos_canonica["b_cuadrado"]
        orientacion = datos_canonica.get("orientacion", "horizontal")
        if orientacion == "horizontal":
            forma = f"({self._texto_desplazamiento('x', h)})^2/{self._formatear_numero(a2)} - ({self._texto_desplazamiento('y', k)})^2/{self._formatear_numero(b2)} = 1"
        else:
            forma = f"({self._texto_desplazamiento('y', k)})^2/{self._formatear_numero(a2)} - ({self._texto_desplazamiento('x', h)})^2/{self._formatear_numero(b2)} = 1"
        return "\n".join(
            [
                "Partimos de la forma canónica de la hipérbola:",
                forma,
                "",
                "Multiplicamos por los denominadores, expandimos los cuadrados y trasladamos todo al lado izquierdo.",
                "Al simplificar, recuperamos la ecuación general:",
                reporte_conica.ecuacion,
            ]
        )

    def _inverso_parabola(self, reporte_conica, datos_canonica):
        vertice = datos_canonica["vertice"]
        p = datos_canonica["p"]
        forma = self._limpiar_texto(datos_canonica["forma_canonica"])
        if forma.startswith("(x") or forma.startswith("x"):
            expansion = (
                f"x^2 {self._signo_lineal(-2 * vertice[0], 'x')} + {self._formatear_numero(vertice[0] ** 2)} "
                f"= {self._formatear_numero(p)}y {self._signo_constante(-p * vertice[1])}"
            )
        else:
            expansion = (
                f"y^2 {self._signo_lineal(-2 * vertice[1], 'y')} + {self._formatear_numero(vertice[1] ** 2)} "
                f"= {self._formatear_numero(p)}x {self._signo_constante(-p * vertice[0])}"
            )
        return "\n".join(
            [
                "Partimos de la forma canónica de la parábola:",
                forma,
                "",
                "Expandimos el cuadrado del lado izquierdo:",
                expansion,
                "",
                "Luego trasladamos todos los términos al lado izquierdo y ordenamos:",
                reporte_conica.ecuacion,
            ]
        )

    def _limpiar_analisis(self):
        self.rut_var.set("")
        self.estado_var.set("")
        self.resumen_label.configure(
            text="Aquí aparecerá un resumen compacto del RUT, la cónica y la función por tramos."
        )
        self.campos_defensa_conica = ["Centro", "Vértices", "Focos", "Ejes", "Asíntotas o directriz"]
        self.campos_defensa_funcion = [
            "Límite por izquierda",
            "Límite por derecha",
            "¿Existe el límite?",
            "Valor de la función en a",
            "¿Es continua?",
            "Tipo de discontinuidad",
            "Justificación escrita",
        ]
        self._actualizar_metricas(
            rut="Pendiente",
            conica="Sin analizar",
            canonica="Sin analizar",
            funcion="Sin analizar",
        )
        self._escribir_texto(self.tarjetas_resumen, "Sin análisis ejecutado.")
        self._escribir_texto(self.tarjetas_conicas, "Sin datos de cónicas.")
        self._escribir_texto(self.tarjetas_funciones, "Sin datos de funciones por tramos.")
        self._reiniciar_canvas(self.canvas_conica, "Canónica no disponible")
        self._reiniciar_canvas(self.canvas_funcion, "Función no disponible")
        self._crear_campos_vacios(self.frame_inputs_conica, self.campos_defensa_conica)
        self._crear_campos_vacios(self.frame_inputs_funcion, self.campos_defensa_funcion)
        self._crear_campos_vacios(self.frame_defensa_conica, self.campos_defensa_conica)
        self._crear_campos_vacios(self.frame_defensa_funcion, self.campos_defensa_funcion)
        self._actualizar_tabla([])
        self.current_reporte_conica = None
        self.current_datos_canonica = None
        self.current_analisis_funcion = None
        self.current_conica_limites = None
        self.current_funcion_limites = None
        if hasattr(self, "rut_entry"):
            self.rut_entry.focus_set()

    def _cargar_estado_invalido(self, texto_validacion):
        self._actualizar_estado_visual("RUT inválido. Revisa formato y dígito verificador.", "error")
        self.campos_defensa_conica = ["Centro", "Vértices", "Focos", "Ejes", "Asíntotas o directriz"]
        self.campos_defensa_funcion = [
            "Límite por izquierda",
            "Límite por derecha",
            "¿Existe el límite?",
            "Valor de la función en a",
            "¿Es continua?",
            "Tipo de discontinuidad",
            "Justificación escrita",
        ]
        self._actualizar_metricas(
            rut="Inválido",
            conica="Sin resultado",
            canonica="Sin resultado",
            funcion="Sin resultado",
        )
        self.estado_var.set("RUT inválido. Revise formato y dígito verificador.")
        self.resumen_label.configure(text="No se pudo continuar con el análisis matemático.")
        self._escribir_texto(self.tarjetas_resumen, texto_validacion)
        self._escribir_texto(self.tarjetas_conicas, "Sin datos de cónicas.")
        self._escribir_texto(self.tarjetas_funciones, "Sin datos de funciones por tramos.")
        self._reiniciar_canvas(self.canvas_conica, "Cónica no disponible")
        self._reiniciar_canvas(self.canvas_funcion, "Función no disponible")
        self._crear_campos_vacios(self.frame_inputs_conica, self.campos_defensa_conica)
        self._crear_campos_vacios(self.frame_inputs_funcion, self.campos_defensa_funcion)
        self._crear_campos_vacios(self.frame_defensa_conica, self.campos_defensa_conica)
        self._crear_campos_vacios(self.frame_defensa_funcion, self.campos_defensa_funcion)
        self._actualizar_tabla([])

    def _analizar_funcion_por_tramos(self, datos_rut):
        funcion_info = generar_funcion_por_tramos(datos_rut)
        a = funcion_info["punto_critico"]
        caso = funcion_info["caso"]
        puntos_info = generar_puntos_cercanos(a)
        tabla = evaluar_en_tabla(puntos_info, self._crear_evaluador_funcion(datos_rut))

        if caso == "removible":
            d1 = funcion_info["parametros"]["d1"]
            limite_izq = a + d1
            limite_der = a + d1
            limite_existe = "Si, ambos limites laterales coinciden."
            valor_punto = "No definida"
            continuidad = "No"
            justificacion = (
                f"La expresion original tiene un factor comun x - {a} que se cancela para x != {a}, "
                f"quedando f(x) = x + {d1}. Por eso ambos limites laterales valen "
                f"{self._formatear_numero(limite_izq)}, pero la funcion original no esta definida en x = {a}."
            )
        elif caso == "salto":
            d2 = funcion_info["parametros"]["d2"]
            d4 = funcion_info["parametros"]["d4"]
            limite_izq = a + d2
            limite_der = a + d4
            valor_punto = self._formatear_numero(limite_der)
            if limite_izq == limite_der:
                limite_existe = "Si, ambos limites laterales coinciden."
                continuidad = "Si"
                justificacion = (
                    f"El limite por izquierda y el limite por derecha valen "
                    f"{self._formatear_numero(limite_izq)}, y ademas f({a}) = "
                    f"{self._formatear_numero(limite_der)}."
                )
            else:
                limite_existe = "No, los limites laterales son distintos."
                continuidad = "No"
                justificacion = (
                    f"El limite por izquierda vale {self._formatear_numero(limite_izq)} y el de derecha "
                    f"vale {self._formatear_numero(limite_der)}; como no coinciden, el limite no existe."
                )
        else:
            numerador = funcion_info["parametros"]["d5_mas_1"]
            limite_izq = "-infinito"
            limite_der = "+infinito"
            limite_existe = "No, hay divergencia infinita."
            valor_punto = "No definida"
            continuidad = "No"
            justificacion = (
                f"La funcion {numerador}/(x - {a}) tiene numerador positivo y el denominador cambia de signo "
                "al cruzar el punto critico, por lo que aparece una asintota vertical en x = a."
            )

        procedimiento = [
            "1. Seleccion automatica del caso",
            f"   d3 = {datos_rut['d3']} -> punto critico a = {a}",
            f"   d8 = {datos_rut['d8']} -> residuo d8 % 3 = {datos_rut['d8'] % 3}",
            f"   Regla aplicada: {self._limpiar_texto(funcion_info['regla_usada'])}",
            "",
            "2. Definicion de la funcion por tramos",
            f"   {self._limpiar_texto(funcion_info['funcion_def']['izquierda'])}",
            f"   {self._limpiar_texto(funcion_info['funcion_def']['punto'])}",
            f"   {self._limpiar_texto(funcion_info['funcion_def']['derecha'])}",
        ]
        if funcion_info["funcion_def"].get("simplificada"):
            procedimiento.append(f"   {self._limpiar_texto(funcion_info['funcion_def']['simplificada'])}")
        procedimiento.extend(
            [
                "",
                "3. Limites laterales y continuidad",
                f"   Limite por izquierda  : {self._formatear_valor(limite_izq)}",
                f"   Limite por derecha    : {self._formatear_valor(limite_der)}",
                f"   Existe el limite?     : {limite_existe}",
                f"   Valor de f(a)         : {valor_punto}",
                f"   Es continua?          : {continuidad}",
                f"   Tipo observado        : {funcion_info['tipo_discontinuidad']}",
                "",
                "4. Justificacion matematica",
                f"   {justificacion}",
            ]
        )

        tabla_texto = []
        for fila in tabla:
            fx = "No definida" if fila["f(x)"] is None else self._formatear_numero(fila["f(x)"])
            tabla_texto.append(
                f"   x = {self._formatear_numero(fila['x']):>8} | {fila['posicion']:<14} | f(x) = {fx}"
            )

        resumen_texto = "\n".join(
            [
                f"Tipo de discontinuidad: {funcion_info['tipo_discontinuidad']}",
                f"Punto critico: a = {a}",
                f"Limite por izquierda: {self._formatear_valor(limite_izq)}",
                f"Limite por derecha: {self._formatear_valor(limite_der)}",
                f"Continuidad en a: {continuidad}",
            ]
        )

        return {
            "funcion_info": funcion_info,
            "punto_critico": a,
            "tabla": tabla,
            "procedimiento": "\n".join(procedimiento),
            "tabla_texto": "\n".join(tabla_texto),
            "resumen_texto": resumen_texto,
        }

    def _crear_evaluador_funcion(self, datos_rut):
        a = datos_rut["d3"]
        residuo = datos_rut["d8"] % 3

        if residuo == 0:
            def evaluar(x):
                if valor_absoluto(x - a) < 1e-12:
                    raise ValueError("Funcion no definida en a.")
                return x + datos_rut["d1"]

            return evaluar

        if residuo == 1:
            def evaluar(x):
                if x < a:
                    return x + datos_rut["d2"]
                return x + datos_rut["d4"]

            return evaluar

        def evaluar(x):
            if valor_absoluto(x - a) < 1e-12:
                raise ValueError("Funcion no definida en a.")
            return (datos_rut["d5"] + 1) / (x - a)

        return evaluar

    def _describir_reglas(self, a_inicial, b_inicial, a_final, b_final, digitos):
        d1, d2, _, _, d5, d6, d7, d8 = digitos
        reglas = []
        if d8 % 2 != 0:
            reglas.append("d8 es impar, por lo tanto B cambia de signo.")
        if d1 == d2:
            reglas.append("d1 = d2, por lo tanto B toma el valor de A.")
        if (d5 + d6) % 3 == 0:
            if d7 % 2 == 0:
                reglas.append("d5 + d6 es múltiplo de 3 y d7 es par, por lo tanto B = 0.")
            else:
                reglas.append("d5 + d6 es múltiplo de 3 y d7 es impar, por lo tanto A = 0.")
        if not reglas and a_inicial == a_final and b_inicial == b_final:
            reglas.append("No se aplicaron reglas especiales.")
        return reglas

    def _justificar_conica(self, tipo_conica, a_coef, b_coef):
        if tipo_conica == "Circunferencia":
            return f"A = B = {self._formatear_numero(a_coef)} y ambos son distintos de 0."
        if tipo_conica == "Elipse":
            return "A y B tienen el mismo signo, pero magnitudes distintas."
        if tipo_conica == "Hiperbola":
            return "A y B tienen signos opuestos."
        if tipo_conica == "Parabola":
            return "Exactamente uno de los coeficientes cuadráticos es 0."
        return "Los coeficientes no determinan una cónica clásica."

    def _conica_no_real(self, datos_canonica, tipo_conica):
        if tipo_conica == "Circunferencia":
            return datos_canonica.get("radio_cuadrado", 0) < 0
        if tipo_conica == "Elipse":
            return datos_canonica.get("a_cuadrado", 0) <= 0 or datos_canonica.get("b_cuadrado", 0) <= 0
        return False
