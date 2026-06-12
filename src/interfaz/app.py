import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from src.conicas.canonica import transformar_a_canonica
from src.conicas.clasificador_conica import clasificar_conica
from src.conicas.coeficientes import calcular_coeficientes
from src.conicas.elementos_conica import obtener_elementos_conica
from src.conicas.procedimiento_conica import ProcedimientoConica
from src.conicas.reglas_conica import aplicar_reglas_especiales
from src.funciones_tramos import evaluar_en_tabla, generar_funcion_por_tramos, generar_puntos_cercanos
from src.rut.parser_rut import generar_procedimiento_parser, obtener_datos_rut
from src.rut.validador_rut import validar_rut
from src.utilidades.matematica_manual import (
    PI,
    coseno,
    coseno_hiperbolico,
    raiz_cuadrada,
    seno,
    seno_hiperbolico,
    valor_absoluto,
)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de análisis matemático")
        self.root.geometry("1360x860")
        self.root.minsize(1180, 760)

        self._crear_estilos()
        self._crear_interfaz()

    def ejecutar(self):
        self.root.mainloop()

    def _crear_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f4f1ea")
        estilo.configure("Card.TFrame", background="#fffdf8", relief="flat")
        estilo.configure("TLabel", background="#f4f1ea", foreground="#2d241d")
        estilo.configure("Title.TLabel", font=("Segoe UI Semibold", 18), foreground="#1f1a17")
        estilo.configure("Subtitle.TLabel", font=("Segoe UI Semibold", 11), foreground="#4e4035")
        estilo.configure("TButton", font=("Segoe UI Semibold", 10))
        estilo.configure("Treeview", font=("Consolas", 10), rowheight=24)
        estilo.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=16)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        encabezado = ttk.Frame(contenedor)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.columnconfigure(1, weight=1)

        ttk.Label(
            encabezado,
            text="Sistema de análisis de cónicas y funciones por tramos",
            style="Title.TLabel",
        ).grid(row=0, column=0, columnspan=4, sticky="w")
        ttk.Label(
            encabezado,
            text="La interfaz expone validación, procedimiento algebraico, forma canónica, gráfica y espacios de defensa.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 14))

        ttk.Label(encabezado, text="RUT:").grid(row=2, column=0, sticky="w")
        self.rut_var = tk.StringVar()
        ttk.Entry(encabezado, textvariable=self.rut_var, width=24).grid(
            row=2, column=1, sticky="w", padx=(8, 10)
        )
        ttk.Button(encabezado, text="Analizar", command=self._analizar).grid(
            row=2, column=2, sticky="w"
        )

        self.estado_var = tk.StringVar(value="Ingrese un RUT válido para generar el análisis.")
        ttk.Label(encabezado, textvariable=self.estado_var).grid(
            row=2, column=3, sticky="e"
        )

        resumen_card = ttk.Frame(contenedor, style="Card.TFrame", padding=10)
        resumen_card.grid(row=1, column=0, sticky="ew", pady=(14, 14))
        resumen_card.columnconfigure(0, weight=1)
        ttk.Label(
            resumen_card,
            text="Resumen de resultados",
            style="Subtitle.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.resumen_label = ttk.Label(
            resumen_card,
            text="Sin análisis ejecutado.",
            background="#fffdf8",
            justify="left",
        )
        self.resumen_label.grid(row=1, column=0, sticky="ew")

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.grid(row=2, column=0, sticky="nsew")

        self.tab_resumen = ttk.Frame(self.notebook, padding=10)
        self.tab_conicas = ttk.Frame(self.notebook, padding=10)
        self.tab_funciones = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_resumen, text="Validación y resumen")
        self.notebook.add(self.tab_conicas, text="Cónicas")
        self.notebook.add(self.tab_funciones, text="Funciones por tramos")

        self._crear_tab_resumen()
        self._crear_tab_conicas()
        self._crear_tab_funciones()

    def _crear_tab_resumen(self):
        self.tab_resumen.columnconfigure(0, weight=1)
        self.tab_resumen.rowconfigure(0, weight=1)
        self.texto_resumen = ScrolledText(
            self.tab_resumen,
            wrap="word",
            font=("Consolas", 10),
            bg="#fffdf8",
            fg="#2d241d",
        )
        self.texto_resumen.grid(row=0, column=0, sticky="nsew")

    def _crear_tab_conicas(self):
        self.tab_conicas.columnconfigure(0, weight=3)
        self.tab_conicas.columnconfigure(1, weight=2)
        self.tab_conicas.rowconfigure(0, weight=1)

        self.texto_conicas = ScrolledText(
            self.tab_conicas,
            wrap="word",
            font=("Consolas", 10),
            bg="#fffdf8",
            fg="#2d241d",
        )
        self.texto_conicas.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        panel_derecho = ttk.Frame(self.tab_conicas)
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=3)
        panel_derecho.rowconfigure(1, weight=2)

        self.canvas_conica = tk.Canvas(
            panel_derecho,
            width=520,
            height=420,
            bg="#fffdf8",
            highlightthickness=1,
            highlightbackground="#cbbca8",
        )
        self.canvas_conica.grid(row=0, column=0, sticky="nsew")

        self.frame_inputs_conica = ttk.LabelFrame(
            panel_derecho,
            text="Campos para completar durante la defensa",
            padding=10,
        )
        self.frame_inputs_conica.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.frame_inputs_conica.columnconfigure(1, weight=1)

    def _crear_tab_funciones(self):
        self.tab_funciones.columnconfigure(0, weight=3)
        self.tab_funciones.columnconfigure(1, weight=2)
        self.tab_funciones.rowconfigure(0, weight=1)

        self.texto_funciones = ScrolledText(
            self.tab_funciones,
            wrap="word",
            font=("Consolas", 10),
            bg="#fffdf8",
            fg="#2d241d",
        )
        self.texto_funciones.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        panel_derecho = ttk.Frame(self.tab_funciones)
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=3)
        panel_derecho.rowconfigure(1, weight=2)
        panel_derecho.rowconfigure(2, weight=2)

        self.canvas_funcion = tk.Canvas(
            panel_derecho,
            width=520,
            height=320,
            bg="#fffdf8",
            highlightthickness=1,
            highlightbackground="#cbbca8",
        )
        self.canvas_funcion.grid(row=0, column=0, sticky="nsew")

        self.frame_inputs_funcion = ttk.LabelFrame(
            panel_derecho,
            text="Campos para completar durante la defensa",
            padding=10,
        )
        self.frame_inputs_funcion.grid(row=1, column=0, sticky="nsew", pady=(10, 10))
        self.frame_inputs_funcion.columnconfigure(1, weight=1)

        self.tabla_valores = ttk.Treeview(
            panel_derecho,
            columns=("x", "lado", "fx"),
            show="headings",
            height=8,
        )
        self.tabla_valores.heading("x", text="x")
        self.tabla_valores.heading("lado", text="Posición")
        self.tabla_valores.heading("fx", text="f(x)")
        self.tabla_valores.column("x", width=90, anchor="center")
        self.tabla_valores.column("lado", width=140, anchor="center")
        self.tabla_valores.column("fx", width=120, anchor="center")
        self.tabla_valores.grid(row=2, column=0, sticky="nsew")

    def _analizar(self):
        rut_input = self.rut_var.get().strip()
        if not rut_input:
            messagebox.showerror("RUT requerido", "Debe ingresar un RUT antes de analizar.")
            return

        try:
            resultado_rut = validar_rut(rut_input)
            resumen_validacion = [
                "SECCIÓN 1: VALIDACIÓN DEL RUT",
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

            self.resumen_label.config(
                text=self._construir_resumen_general(
                    resultado_rut,
                    datos_rut,
                    reporte_conica,
                    datos_canonica,
                    analisis_funcion,
                )
            )
            self.estado_var.set("Análisis completo. Revise procedimiento, gráficos e inputs de defensa.")

            self._escribir_texto(
                self.texto_resumen,
                "\n".join(
                    [
                        "\n".join(resumen_validacion),
                        "",
                        "SECCIÓN 2: EXTRACCIÓN DE DÍGITOS Y VARIABLE AUXILIAR",
                        parser_texto,
                        "",
                        "SECCIÓN 3: RESUMEN DE LA CÓNICA",
                        reporte_conica.generar_reporte(),
                        "",
                        "SECCIÓN 4: RESUMEN DE FUNCIÓN POR TRAMOS",
                        analisis_funcion["resumen_texto"],
                    ]
                ),
            )

            self._escribir_texto(
                self.texto_conicas,
                "\n".join(
                    [
                        "SECCIÓN CÓNICAS",
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
                self.texto_funciones,
                "\n".join(
                    [
                        "SECCIÓN FUNCIONES POR TRAMOS",
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
            self._actualizar_tabla(analisis_funcion["tabla"])
        except Exception as error:
            self.estado_var.set("Se produjo un error al procesar el análisis.")
            messagebox.showerror("Error de análisis", str(error))

    def _cargar_estado_invalido(self, texto_validacion):
        self.estado_var.set("RUT inválido. Revise formato y dígito verificador.")
        self.resumen_label.config(text="No se pudo continuar con el análisis matemático.")
        self._escribir_texto(self.texto_resumen, texto_validacion)
        self._escribir_texto(self.texto_conicas, "Sin datos de cónicas.")
        self._escribir_texto(self.texto_funciones, "Sin datos de funciones por tramos.")
        self._reiniciar_canvas(self.canvas_conica, "Cónica no disponible")
        self._reiniciar_canvas(self.canvas_funcion, "Función no disponible")
        self._crear_campos_vacios(
            self.frame_inputs_conica,
            ["Centro", "Vértices", "Focos", "Ejes", "Asíntotas o directriz"],
        )
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
        self._actualizar_tabla([])

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

    def _analizar_funcion_por_tramos(self, datos_rut):
        funcion_info = generar_funcion_por_tramos(datos_rut)
        a = funcion_info["punto_critico"]
        residuo = datos_rut["d8"] % 3
        puntos_info = generar_puntos_cercanos(a)
        tabla = evaluar_en_tabla(puntos_info, self._crear_evaluador_funcion(datos_rut))

        if residuo == 0:
            limite_izq = a ** 2 + 1
            limite_der = a ** 2 + 1
            limite_existe = "Sí, ambos límites laterales coinciden."
            valor_punto = "No definida"
            continuidad = "No"
            justificacion = (
                f"Los límites laterales valen {self._formatear_numero(limite_izq)}, "
                "pero la función no está definida en el punto crítico."
            )
        elif residuo == 1:
            limite_izq = (2 * a) + 1
            limite_der = a + 5
            limite_existe = "No, los límites laterales son distintos."
            valor_punto = self._formatear_numero(limite_izq)
            continuidad = "No"
            justificacion = (
                f"El límite por izquierda vale {self._formatear_numero(limite_izq)} y el de derecha "
                f"vale {self._formatear_numero(limite_der)}; como no coinciden, el límite no existe."
            )
        else:
            limite_izq = "-∞"
            limite_der = "+∞"
            limite_existe = "No, hay divergencia infinita."
            valor_punto = "No definida"
            continuidad = "No"
            justificacion = (
                "La función presenta una asíntota vertical en x = a; los límites laterales divergen con signo opuesto."
            )

        procedimiento = [
            "1. Selección automática del caso",
            f"   d3 = {datos_rut['d3']} -> punto crítico a = {a}",
            f"   d8 = {datos_rut['d8']} -> residuo d8 % 3 = {residuo}",
            f"   Regla aplicada: {self._limpiar_texto(funcion_info['regla_usada'])}",
            "",
            "2. Definición de la función por tramos",
            f"   {self._limpiar_texto(funcion_info['funcion_def']['izquierda'])}",
            f"   {self._limpiar_texto(funcion_info['funcion_def']['punto'])}",
            f"   {self._limpiar_texto(funcion_info['funcion_def']['derecha'])}",
            "",
            "3. Límites laterales y continuidad",
            f"   Límite por izquierda  : {self._formatear_valor(limite_izq)}",
            f"   Límite por derecha    : {self._formatear_valor(limite_der)}",
            f"   ¿Existe el límite?    : {limite_existe}",
            f"   Valor de f(a)         : {valor_punto}",
            f"   ¿Es continua?         : {continuidad}",
            f"   Tipo de discontinuidad: {funcion_info['tipo_discontinuidad']}",
            "",
            "4. Justificación matemática",
            f"   {justificacion}",
        ]

        tabla_texto = []
        for fila in tabla:
            fx = "No definida" if fila["f(x)"] is None else self._formatear_numero(fila["f(x)"])
            tabla_texto.append(
                f"   x = {self._formatear_numero(fila['x']):>8} | {fila['posicion']:<14} | f(x) = {fx}"
            )

        resumen_texto = "\n".join(
            [
                f"Tipo de discontinuidad: {funcion_info['tipo_discontinuidad']}",
                f"Punto crítico: a = {a}",
                f"Límite por izquierda: {self._formatear_valor(limite_izq)}",
                f"Límite por derecha: {self._formatear_valor(limite_der)}",
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
                    raise ValueError("Función no definida en a.")
                return (x ** 2) + 1

            return evaluar

        if residuo == 1:
            def evaluar(x):
                if x <= a:
                    return (2 * x) + 1
                return x + 5

            return evaluar

        def evaluar(x):
            if valor_absoluto(x - a) < 1e-12:
                raise ValueError("Función no definida en a.")
            return 1 / (x - a)

        return evaluar

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
                    [
                        f"Centro: {self._formatear_punto(centro)}",
                        f"Radio: {self._formatear_numero(radio)}",
                    ]
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

    def _dibujar_conica(self, tipo_conica, datos_canonica):
        if not datos_canonica or not datos_canonica.get("forma_canonica"):
            self._reiniciar_canvas(self.canvas_conica, "Cónica no disponible")
            return

        if datos_canonica["forma_canonica"].startswith("No fue posible"):
            self._reiniciar_canvas(self.canvas_conica, datos_canonica["forma_canonica"])
            return

        canvas = self.canvas_conica
        canvas.delete("all")
        width = int(canvas["width"])
        height = int(canvas["height"])

        puntos = []
        lineas = []

        if tipo_conica == "Circunferencia":
            h, k = datos_canonica["centro"]
            r = datos_canonica["radio"]
            for indice in range(181):
                angulo = (indice * PI) / 90
                puntos.append((h + (r * coseno(angulo)), k + (r * seno(angulo))))
            limites = (h - r - 2, h + r + 2, k - r - 2, k + r + 2)

        elif tipo_conica == "Elipse":
            h, k = datos_canonica["centro"]
            a = raiz_cuadrada(datos_canonica["a_cuadrado"])
            b = raiz_cuadrada(datos_canonica["b_cuadrado"])
            for indice in range(181):
                angulo = (indice * PI) / 90
                puntos.append((h + (a * coseno(angulo)), k + (b * seno(angulo))))
            limites = (h - a - 2, h + a + 2, k - b - 2, k + b + 2)

        elif tipo_conica == "Hiperbola":
            h, k = datos_canonica["centro"]
            a = raiz_cuadrada(datos_canonica["a_cuadrado"])
            b = raiz_cuadrada(datos_canonica["b_cuadrado"])
            orientacion = datos_canonica.get("orientacion", "horizontal")
            if orientacion == "horizontal":
                izquierda = []
                derecha = []
                for entero in range(-25, 26):
                    t = entero / 15
                    cosh = coseno_hiperbolico(t)
                    sinh = seno_hiperbolico(t)
                    derecha.append((h + (a * cosh), k + (b * sinh)))
                    izquierda.append((h - (a * cosh), k + (b * sinh)))
                puntos = [izquierda, derecha]
                pendiente = b / a
            else:
                inferior = []
                superior = []
                for entero in range(-25, 26):
                    t = entero / 15
                    cosh = coseno_hiperbolico(t)
                    sinh = seno_hiperbolico(t)
                    superior.append((h + (b * sinh), k + (a * cosh)))
                    inferior.append((h + (b * sinh), k - (a * cosh)))
                puntos = [inferior, superior]
                pendiente = a / b
            for signo in (-1, 1):
                lineas.append(((h - 8, k + (signo * pendiente * -8)), (h + 8, k + (signo * pendiente * 8))))
            limites = (h - 8, h + 8, k - 8, k + 8)

        elif tipo_conica == "Parabola":
            vertice = datos_canonica["vertice"]
            p = datos_canonica["p"]
            forma = datos_canonica["forma_canonica"]
            curva = []
            if forma.startswith("(x") or forma.startswith("x"):
                for indice in range(117):
                    x = vertice[0] - 7 + (indice * 0.12)
                    y = vertice[1] + (((x - vertice[0]) ** 2) / p)
                    curva.append((x, y))
                directriz_y = vertice[1] - (p / 4)
                lineas.append(((vertice[0] - 8, directriz_y), (vertice[0] + 8, directriz_y)))
            else:
                for indice in range(117):
                    y = vertice[1] - 7 + (indice * 0.12)
                    x = vertice[0] + (((y - vertice[1]) ** 2) / p)
                    curva.append((x, y))
                directriz_x = vertice[0] - (p / 4)
                lineas.append(((directriz_x, vertice[1] - 8), (directriz_x, vertice[1] + 8)))
            puntos = curva
            limites = (vertice[0] - 8, vertice[0] + 8, vertice[1] - 8, vertice[1] + 8)
        else:
            self._reiniciar_canvas(canvas, "Cónica no disponible")
            return

        mapper = self._crear_transformador(canvas, limites)
        self._dibujar_ejes(canvas, mapper, limites, width, height)

        for linea in lineas:
            x1, y1 = mapper(*linea[0])
            x2, y2 = mapper(*linea[1])
            canvas.create_line(x1, y1, x2, y2, fill="#9f7f5b", dash=(5, 4), width=2)

        if puntos and isinstance(puntos[0], list):
            for rama in puntos:
                self._dibujar_curva(canvas, mapper, rama, "#0a6c74")
        else:
            self._dibujar_curva(canvas, mapper, puntos, "#0a6c74")

        canvas.create_text(
            12,
            12,
            anchor="nw",
            text=f"{tipo_conica}: {self._limpiar_texto(datos_canonica['forma_canonica'])}",
            fill="#2d241d",
            font=("Segoe UI Semibold", 10),
        )

    def _dibujar_funcion(self, analisis_funcion):
        canvas = self.canvas_funcion
        canvas.delete("all")
        a = analisis_funcion["punto_critico"]
        tipo = analisis_funcion["funcion_info"]["tipo_discontinuidad"]
        limites = (a - 4, a + 4, -8, 12)
        mapper = self._crear_transformador(canvas, limites)
        self._dibujar_ejes(canvas, mapper, limites, int(canvas["width"]), int(canvas["height"]))

        if "Removible" in tipo:
            puntos = []
            for indice in range(161):
                x = a - 4 + (indice * 0.05)
                if valor_absoluto(x - a) > 1e-6:
                    puntos.append((x, (x ** 2) + 1))
            self._dibujar_curva(canvas, mapper, puntos, "#d46a00")
            x, y = mapper(a, (a ** 2) + 1)
            canvas.create_oval(x - 6, y - 6, x + 6, y + 6, outline="#d46a00", width=2)
        elif "Salto" in tipo:
            izquierda = []
            derecha = []
            for indice in range(81):
                x_izq = a - 4 + (indice * 0.05)
                x_der = a + (indice * 0.05)
                if x_izq <= a:
                    izquierda.append((x_izq, (2 * x_izq) + 1))
                if x_der > a:
                    derecha.append((x_der, x_der + 5))
            self._dibujar_curva(canvas, mapper, izquierda, "#d46a00")
            self._dibujar_curva(canvas, mapper, derecha, "#355c7d")
            x1, y1 = mapper(a, (2 * a) + 1)
            x2, y2 = mapper(a, a + 5)
            canvas.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill="#d46a00", outline="#d46a00")
            canvas.create_oval(x2 - 6, y2 - 6, x2 + 6, y2 + 6, outline="#355c7d", width=2)
        else:
            izquierda = []
            derecha = []
            for indice in range(132):
                x_izq = a - 4 + (indice * 0.03)
                x_der = a + 0.06 + (indice * 0.03)
                if x_izq < a - 0.06:
                    izquierda.append((x_izq, 1 / (x_izq - a)))
                if x_der > a + 0.06:
                    derecha.append((x_der, 1 / (x_der - a)))
            self._dibujar_curva(canvas, mapper, izquierda, "#d46a00")
            self._dibujar_curva(canvas, mapper, derecha, "#355c7d")
            x1, _ = mapper(a, 0)
            canvas.create_line(x1, 20, x1, int(canvas["height"]) - 20, fill="#9f7f5b", dash=(5, 4), width=2)

        canvas.create_text(
            12,
            12,
            anchor="nw",
            text=f"{tipo} en x = {a}",
            fill="#2d241d",
            font=("Segoe UI Semibold", 10),
        )

    def _crear_transformador(self, canvas, limites):
        xmin, xmax, ymin, ymax = limites
        width = int(canvas["width"])
        height = int(canvas["height"])
        padding = 35

        def transformar(x, y):
            px = padding + (((x - xmin) / (xmax - xmin)) * (width - 2 * padding))
            py = height - padding - (((y - ymin) / (ymax - ymin)) * (height - 2 * padding))
            return px, py

        return transformar

    def _dibujar_ejes(self, canvas, mapper, limites, width, height):
        xmin, xmax, ymin, ymax = limites
        cero_x, cero_y = mapper(0, 0)

        if xmin <= 0 <= xmax:
            canvas.create_line(cero_x, 18, cero_x, height - 18, fill="#c7b8a4")
        if ymin <= 0 <= ymax:
            canvas.create_line(18, cero_y, width - 18, cero_y, fill="#c7b8a4")

        canvas.create_rectangle(8, 8, width - 8, height - 8, outline="#d7cab7")

    def _dibujar_curva(self, canvas, mapper, puntos, color):
        if len(puntos) < 2:
            return
        coordenadas = []
        for x, y in puntos:
            px, py = mapper(x, y)
            coordenadas.extend([px, py])
        canvas.create_line(*coordenadas, fill=color, width=2, smooth=True)

    def _reiniciar_canvas(self, canvas, mensaje):
        canvas.delete("all")
        width = int(canvas["width"])
        height = int(canvas["height"])
        canvas.create_rectangle(8, 8, width - 8, height - 8, outline="#d7cab7")
        canvas.create_text(
            width / 2,
            height / 2,
            text=mensaje,
            fill="#6f6154",
            font=("Segoe UI", 12),
            width=width - 40,
        )

    def _crear_campos_vacios(self, frame, etiquetas):
        for child in frame.winfo_children():
            child.destroy()

        for fila, etiqueta in enumerate(etiquetas):
            ttk.Label(frame, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=4)
            ttk.Entry(frame, width=46).grid(row=fila, column=1, sticky="ew", padx=(10, 0), pady=4)

    def _actualizar_tabla(self, filas):
        for item in self.tabla_valores.get_children():
            self.tabla_valores.delete(item)

        for fila in filas:
            fx = "No definida" if fila["f(x)"] is None else self._formatear_numero(fila["f(x)"])
            self.tabla_valores.insert(
                "",
                "end",
                values=(self._formatear_numero(fila["x"]), fila["posicion"], fx),
            )

    def _escribir_texto(self, widget, contenido):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, self._limpiar_texto(contenido))
        widget.config(state="disabled")

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

    def _formatear_ecuacion_general(self, a_coef, b_coef, c_coef, d_coef, e_coef):
        terminos = [
            self._formatear_termino(a_coef, "x^2", True),
            self._formatear_termino(b_coef, "y^2"),
            self._formatear_termino(c_coef, "x"),
            self._formatear_termino(d_coef, "y"),
            self._formatear_termino(e_coef, ""),
        ]
        return f"{''.join(termino for termino in terminos if termino)} = 0"

    def _formatear_termino(self, coeficiente, variable, primero=False):
        if coeficiente == 0:
            return ""

        valor = self._formatear_numero(valor_absoluto(coeficiente))
        termino = f"{valor}{variable}" if variable else valor
        if primero:
            return f"-{termino}" if coeficiente < 0 else termino
        return f"{' - ' if coeficiente < 0 else ' + '}{termino}"

    def _formatear_numero(self, numero):
        if isinstance(numero, str):
            return numero
        if float(numero).is_integer():
            return str(int(numero))
        return f"{numero:.4f}"

    def _formatear_punto(self, punto):
        return f"({self._formatear_numero(punto[0])}, {self._formatear_numero(punto[1])})"

    def _formatear_lista_puntos(self, puntos):
        return ", ".join(self._formatear_punto(punto) for punto in puntos)

    def _formatear_valor(self, valor):
        if isinstance(valor, str):
            return valor
        return self._formatear_numero(valor)

    def _texto_desplazamiento(self, variable, valor):
        if valor == 0:
            return variable
        if valor > 0:
            return f"{variable} - {self._formatear_numero(valor)}"
        return f"{variable} + {self._formatear_numero(valor_absoluto(valor))}"

    def _signo_lineal(self, coeficiente, variable):
        if coeficiente == 0:
            return ""
        signo = "-" if coeficiente < 0 else "+"
        return f"{signo} {self._formatear_numero(valor_absoluto(coeficiente))}{variable}"

    def _signo_constante(self, constante):
        if constante == 0:
            return ""
        signo = "-" if constante < 0 else "+"
        return f"{signo} {self._formatear_numero(valor_absoluto(constante))}"

    def _limpiar_texto(self, texto):
        reemplazos = {
            "→": "->",
            "∞": "infinito",
            "≤": "<=",
            "≥": ">=",
            "≠": "!=",
            "±": "+/-",
            "²": "^2",
            "⁻": "-",
            "⁺": "+",
        }
        for origen, destino in reemplazos.items():
            texto = texto.replace(origen, destino)
        return texto
