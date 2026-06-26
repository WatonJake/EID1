import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk

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
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Sistema de análisis matemático")
        self.root.geometry("1360x860")
        self.root.minsize(1180, 760)

        self.current_reporte_conica = None
        self.current_datos_canonica = None
        self.current_analisis_funcion = None
        self.current_conica_limites = None
        self.current_funcion_limites = None
        self.grafico_conica_expandido = True
        self.grafico_funcion_expandido = True
        self.tabla_apoyo_expandida = True
        self.drag_start = {
            "conica": None,
            "funcion": None,
        }
        self.colores = {
            "fondo": "#f4efe7",
            "panel": "#fbf8f2",
            "panel_alt": "#f1e7d8",
            "borde": "#d9c8b5",
            "texto": "#201a16",
            "texto_sec": "#6a5748",
            "acento": "#b65a2e",
            "acento_oscuro": "#8f4522",
            "exito": "#2f7d4a",
            "error": "#b43f3f",
            "aviso": "#c98a1d",
        }
        self.metricas = {}

        self._crear_estilos()
        self._crear_interfaz()

    def ejecutar(self):
        self.root.mainloop()

    def _crear_estilos(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color=self.colores["fondo"])
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("TNotebook", background=self.colores["fondo"], borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI Semibold", 10))
        estilo.configure(
            "Treeview",
            background="#fffdfa",
            fieldbackground="#fffdfa",
            foreground=self.colores["texto"],
            rowheight=28,
            bordercolor=self.colores["borde"],
        )
        estilo.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _crear_interfaz(self):
        contenedor = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        contenedor.pack(fill="both", expand=True, padx=16, pady=16)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)

        encabezado = ctk.CTkFrame(
            contenedor,
            fg_color=self.colores["panel_alt"],
            corner_radius=18,
            border_width=1,
            border_color=self.colores["borde"],
        )
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.columnconfigure(1, weight=1)
        encabezado.columnconfigure(4, weight=1)
        ctk.CTkLabel(
            encabezado,
            text="Sistema de análisis de cónicas y funciones por tramos",
            text_color="#1f1a17",
            font=("Segoe UI Semibold", 18),
        ).grid(row=0, column=0, columnspan=4, sticky="w")
        ctk.CTkLabel(
            encabezado,
            text="La interfaz expone validación, procedimiento algebraico, forma canónica, gráfica y espacios de defensa.",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 11),
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 14))

        ctk.CTkLabel(encabezado, text="RUT:").grid(row=2, column=0, sticky="w")
        self.rut_var = tk.StringVar()
        ctk.CTkEntry(encabezado, textvariable=self.rut_var, width=220).grid(
            row=2, column=1, sticky="w", padx=(8, 10)
        )
        ctk.CTkButton(encabezado, text="Analizar", command=self._analizar).grid(
            row=2, column=2, sticky="w"
        )

        self.estado_var = tk.StringVar(value="Ingrese un RUT válido para generar el análisis.")
        ctk.CTkLabel(encabezado, textvariable=self.estado_var).grid(row=2, column=3, sticky="e")

        widgets_encabezado = encabezado.winfo_children()
        titulo_label = widgets_encabezado[0]
        subtitulo_label = widgets_encabezado[1]
        rut_label = widgets_encabezado[2]
        self.rut_entry = widgets_encabezado[3]
        boton_analizar = widgets_encabezado[4]
        self.estado_badge = widgets_encabezado[5]

        encabezado.columnconfigure(4, weight=1)
        titulo_label.configure(
            text="Explorador de canonicas y funciones",
            text_color=self.colores["texto"],
            font=("Georgia", 28, "bold"),
        )
        titulo_label.grid_configure(columnspan=5, padx=24, pady=(20, 0))
        subtitulo_label.configure(
            text="Ingresa un RUT y revisa en un flujo mas claro la validacion, el resultado clave, la grafica y el desarrollo de defensa.",
            text_color=self.colores["texto_sec"],
            font=("Segoe UI", 12),
            wraplength=950,
            justify="left",
        )
        subtitulo_label.grid_configure(columnspan=5, padx=24, pady=(8, 16))
        rut_label.configure(text="RUT", text_color=self.colores["texto"], font=("Segoe UI Semibold", 11))
        rut_label.grid_configure(padx=(24, 8), pady=(0, 14))
        self.rut_entry.configure(
            height=40,
            corner_radius=12,
            fg_color="#fffdfa",
            border_color=self.colores["borde"],
            text_color=self.colores["texto"],
            font=("Segoe UI", 13),
        )
        self.rut_entry.grid_configure(pady=(0, 14))
        self.rut_entry.bind("<Return>", lambda event: self._analizar())
        boton_analizar.configure(
            height=40,
            corner_radius=12,
            fg_color=self.colores["acento"],
            hover_color=self.colores["acento_oscuro"],
            font=("Segoe UI Semibold", 12),
        )
        boton_analizar.grid_configure(padx=(0, 10), pady=(0, 14))
        self.estado_var.set("Listo para analizar. Ejemplo: 12.345.678-5")
        self.estado_badge.configure(
            text_color="#fffaf4",
            fg_color=self.colores["aviso"],
            corner_radius=12,
            font=("Segoe UI Semibold", 13),
            justify="left",
            wraplength=320,
            padx=12,
            pady=10,
        )
        self.estado_badge.grid_configure(column=4, padx=(12, 24), pady=(0, 14), sticky="e")

        self.boton_limpiar = ctk.CTkButton(
            encabezado,
            text="Limpiar",
            command=self._limpiar_analisis,
            height=40,
            corner_radius=12,
            fg_color="#eadfce",
            hover_color="#dfcfb7",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 12),
        )
        self.boton_limpiar.grid(row=2, column=3, sticky="w", pady=(0, 14))

        chips = ctk.CTkFrame(encabezado, fg_color="transparent")
        chips.grid(row=3, column=0, columnspan=5, sticky="w", padx=24, pady=(0, 18))
        for indice, texto in enumerate(
            [
                "1. Validar RUT",
                "2. Leer la canónica",
                "3. Revisar la función",
                "4. Completar la defensa",
            ]
        ):
            ctk.CTkLabel(
                chips,
                text=texto,
                text_color=self.colores["texto"],
                fg_color="#f8f2e8",
                corner_radius=12,
                padx=10,
                pady=6,
                font=("Segoe UI Semibold", 10),
            ).grid(row=0, column=indice, padx=(0, 8), sticky="w")

        franja_resumen = ctk.CTkFrame(contenedor, fg_color="transparent")
        franja_resumen.grid(row=1, column=0, sticky="ew", pady=(16, 14))
        franja_resumen.columnconfigure((0, 1, 2, 3), weight=1)
        self._crear_metricas(franja_resumen)

        resumen_card = ctk.CTkFrame(
            contenedor,
            fg_color=self.colores["panel"],
            corner_radius=16,
            border_width=1,
            border_color=self.colores["borde"],
        )
        resumen_card.grid(row=2, column=0, sticky="ew", pady=(0, 14), padx=(0, 0))
        resumen_card.columnconfigure(0, weight=1)
        ctk.CTkLabel(
            resumen_card,
            text="Lectura rapida del resultado",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 13),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 6))
        self.resumen_label = ctk.CTkLabel(
            resumen_card,
            text="Sin análisis ejecutado.",
            text_color=self.colores["texto_sec"],
            wraplength=1080,
            anchor="w",
            justify="left",
            font=("Segoe UI", 12),
        )
        self.resumen_label.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 18))

        self.notebook = ttk.Notebook(contenedor)
        self.notebook.grid(row=3, column=0, sticky="nsew")

        self.tab_resumen = ttk.Frame(self.notebook, padding=10)
        self.tab_conicas = ttk.Frame(self.notebook, padding=10)
        self.tab_funciones = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_resumen, text="Validación y resumen")
        self.notebook.add(self.tab_conicas, text="Cónicas")
        self.notebook.add(self.tab_funciones, text="Funciones por tramos")

        self._crear_tab_resumen()
        self._crear_tab_conicas()
        self._crear_tab_funciones()
        self._limpiar_analisis()

    def _crear_tab_resumen(self):
        self.tab_resumen.columnconfigure(0, weight=1)
        self.tab_resumen.rowconfigure(1, weight=1)
        intro = self._crear_panel_lateral(
            self.tab_resumen,
            "Desarrollo completo de validacion y resumen",
            "Usa esta pestaña para explicar el procedimiento paso a paso. La franja superior resume el resultado y aqui­ queda el detalle.",
        )
        intro.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.tarjetas_resumen = self._crear_contenedor_tarjetas(self.tab_resumen)
        self.tarjetas_resumen.grid(row=1, column=0, sticky="nsew")

    def _crear_metricas(self, parent):
        definiciones = [
            ("rut", "RUT", "Pendiente"),
            ("conica", "Cónica", "Sin analizar"),
            ("canonica", "Forma canónica", "Sin analizar"),
            ("funcion", "Función", "Sin analizar"),
        ]
        for columna, (clave, titulo, valor_inicial) in enumerate(definiciones):
            tarjeta = ctk.CTkFrame(
                parent,
                fg_color=self.colores["panel"],
                corner_radius=14,
                border_width=1,
                border_color=self.colores["borde"],
            )
            tarjeta.grid(row=0, column=columna, sticky="ew", padx=6)
            ctk.CTkLabel(
                tarjeta,
                text=titulo,
                text_color=self.colores["texto_sec"],
                font=("Segoe UI Semibold", 10),
            ).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 2))
            valor = ctk.CTkLabel(
                tarjeta,
                text=valor_inicial,
                text_color=self.colores["texto"],
                font=("Segoe UI Semibold", 15),
                wraplength=220,
                justify="left",
            )
            valor.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))
            self.metricas[clave] = valor

    def _crear_panel_lateral(self, parent, titulo, descripcion):
        panel = ctk.CTkFrame(
            parent,
            fg_color=self.colores["panel"],
            corner_radius=14,
            border_width=1,
            border_color=self.colores["borde"],
        )
        titulo_label = ctk.CTkLabel(
            panel,
            text=titulo,
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 12),
        )
        titulo_label.grid(row=0, column=0, sticky="w", padx=14, pady=(14, 4))
        titulo_label._persistir_panel = True
        descripcion_label = ctk.CTkLabel(
            panel,
            text=descripcion,
            text_color=self.colores["texto_sec"],
            font=("Segoe UI", 10),
            wraplength=360,
            justify="left",
        )
        descripcion_label.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 10))
        descripcion_label._persistir_panel = True
        return panel

    def _crear_tab_conicas(self):
        self.tab_conicas.columnconfigure(0, weight=3)
        self.tab_conicas.columnconfigure(1, weight=2)
        self.tab_conicas.rowconfigure(0, weight=1)

        self.tarjetas_conicas = self._crear_contenedor_tarjetas(self.tab_conicas)
        self.tarjetas_conicas.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        panel_derecho = ctk.CTkFrame(self.tab_conicas, fg_color="transparent")
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=1, minsize=460)
        self.panel_derecho_conicas = panel_derecho

        panel_grafico = self._crear_panel_lateral(
            panel_derecho,
            "Grafico de la conica",
            "Arrastra para mover la vista y usa la rueda del mouse para acercar o alejar.",
        )
        panel_grafico.grid(row=0, column=0, sticky="nsew")
        panel_grafico.columnconfigure(0, weight=1)
        panel_grafico.columnconfigure(1, weight=0)
        panel_grafico.rowconfigure(2, weight=1, minsize=360)
        self.panel_grafico_conica = panel_grafico
        self.descripcion_grafico_conica = panel_grafico.winfo_children()[1]
        self.boton_grafico_conica = ctk.CTkButton(
            panel_grafico,
            text="Ocultar",
            width=96,
            height=30,
            corner_radius=10,
            fg_color="#eadfce",
            hover_color="#dfcfb7",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 11),
            command=self._toggle_grafico_conica,
        )
        self.boton_grafico_conica.grid(row=0, column=1, rowspan=2, sticky="e", padx=14, pady=(12, 8))

        self.canvas_conica = tk.Canvas(
            panel_grafico,
            width=520,
            height=420,
            bg="#fffdfa",
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
        )
        self.canvas_conica.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.canvas_conica.bind("<Configure>", self._on_canvas_conica_resize)
        self.canvas_conica.bind("<ButtonPress-1>", lambda event: self._inicio_arrastre(event, "conica"))
        self.canvas_conica.bind("<B1-Motion>", lambda event: self._mover_arrastre(event, "conica"))
        self.canvas_conica.bind("<ButtonRelease-1>", lambda event: self._finalizar_arrastre(event, "conica"))
        self.canvas_conica.bind("<MouseWheel>", lambda event: self._zoom(event, "conica"))
        self.canvas_conica.bind("<Button-4>", lambda event: self._zoom(event, "conica"))
        self.canvas_conica.bind("<Button-5>", lambda event: self._zoom(event, "conica"))

        self.frame_inputs_conica = ctk.CTkFrame(self.tab_conicas, fg_color="transparent")
        self.frame_inputs_conica.columnconfigure(1, weight=1)

    def _crear_tab_funciones(self):
        self.tab_funciones.columnconfigure(0, weight=3)
        self.tab_funciones.columnconfigure(1, weight=2)
        self.tab_funciones.rowconfigure(0, weight=1)

        self.tarjetas_funciones = self._crear_contenedor_tarjetas(self.tab_funciones)
        self.tarjetas_funciones.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        panel_derecho = ctk.CTkFrame(self.tab_funciones, fg_color="transparent")
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=4, minsize=360)
        panel_derecho.rowconfigure(2, weight=2, minsize=260)
        self.panel_derecho_funciones = panel_derecho

        panel_grafico = self._crear_panel_lateral(
            panel_derecho,
            "Grafico de la funcion",
            "Combina este panel con la tabla para leer mejor el punto critico y los limites laterales.",
        )
        panel_grafico.grid(row=0, column=0, sticky="nsew")
        panel_grafico.columnconfigure(0, weight=1)
        panel_grafico.columnconfigure(1, weight=0)
        panel_grafico.rowconfigure(2, weight=1, minsize=280)
        self.panel_grafico_funcion = panel_grafico
        self.descripcion_grafico_funcion = panel_grafico.winfo_children()[1]
        self.boton_grafico_funcion = ctk.CTkButton(
            panel_grafico,
            text="Ocultar",
            width=96,
            height=30,
            corner_radius=10,
            fg_color="#eadfce",
            hover_color="#dfcfb7",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 11),
            command=self._toggle_grafico_funcion,
        )
        self.boton_grafico_funcion.grid(row=0, column=1, rowspan=2, sticky="e", padx=14, pady=(12, 8))

        self.canvas_funcion = tk.Canvas(
            panel_grafico,
            width=520,
            height=320,
            bg="#fffdfa",
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
        )
        self.canvas_funcion.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.canvas_funcion.bind("<Configure>", self._on_canvas_funcion_resize)
        self.canvas_funcion.bind("<ButtonPress-1>", lambda event: self._inicio_arrastre(event, "funcion"))
        self.canvas_funcion.bind("<B1-Motion>", lambda event: self._mover_arrastre(event, "funcion"))
        self.canvas_funcion.bind("<ButtonRelease-1>", lambda event: self._finalizar_arrastre(event, "funcion"))
        self.canvas_funcion.bind("<MouseWheel>", lambda event: self._zoom(event, "funcion"))
        self.canvas_funcion.bind("<Button-4>", lambda event: self._zoom(event, "funcion"))
        self.canvas_funcion.bind("<Button-5>", lambda event: self._zoom(event, "funcion"))

        self.frame_inputs_funcion = ctk.CTkFrame(self.tab_funciones, fg_color="transparent")
        self.frame_inputs_funcion.columnconfigure(1, weight=1)

        panel_tabla = self._crear_panel_lateral(
            panel_derecho,
            "Tabla de apoyo",
            "La fila del punto critico queda resaltada para facilitar la lectura.",
        )
        panel_tabla.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        panel_tabla.columnconfigure(0, weight=1)
        panel_tabla.columnconfigure(1, weight=0)
        panel_tabla.rowconfigure(2, weight=1, minsize=180)
        self.panel_tabla_apoyo = panel_tabla
        self.descripcion_tabla_apoyo = panel_tabla.winfo_children()[1]
        self.boton_tabla_apoyo = ctk.CTkButton(
            panel_tabla,
            text="Ocultar",
            width=96,
            height=30,
            corner_radius=10,
            fg_color="#eadfce",
            hover_color="#dfcfb7",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 11),
            command=self._toggle_tabla_apoyo,
        )
        self.boton_tabla_apoyo.grid(row=0, column=1, rowspan=2, sticky="e", padx=14, pady=(12, 8))

        self.tabla_valores = ttk.Treeview(
            panel_tabla,
            columns=("x", "lado", "fx"),
            show="headings",
            height=8,
        )
        self.tabla_valores.heading("x", text="x")
        self.tabla_valores.heading("lado", text="Posicion")
        self.tabla_valores.heading("fx", text="f(x)")
        self.tabla_valores.column("x", width=90, anchor="center")
        self.tabla_valores.column("lado", width=140, anchor="center")
        self.tabla_valores.column("fx", width=120, anchor="center")
        self.tabla_valores.tag_configure("critico", background="#f9ecd3")
        self.tabla_valores.tag_configure("normal", background="#fffdfa")
        self.tabla_valores.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 14))

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
                self.tarjetas_conicas,
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
                self.tarjetas_funciones,
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
        self.estado_var.set(mensaje)
        colores_estado = {
            "exito": self.colores["exito"],
            "error": self.colores["error"],
            "aviso": self.colores["aviso"],
        }
        if hasattr(self, "estado_badge"):
            self.estado_badge.configure(fg_color=colores_estado.get(estado, self.colores["aviso"]))

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

    def _limpiar_analisis(self):
        self.rut_var.set("")
        self._actualizar_estado_visual("Listo para analizar. Ejemplo: 12.345.678-5", "aviso")
        self.resumen_label.configure(text="Aquí aparecerá un resumen compacto del RUT, la cónica y la función por tramos.")
        self._actualizar_metricas(
            rut="Pendiente",
            conica="Sin analizar",
            canonica="Sin analizar",
            funcion="Sin analizar",
        )
        self._escribir_texto(self.tarjetas_resumen, "Sin análisis ejecutado.")
        self._escribir_texto(self.tarjetas_conicas, "Sin datos de canonicas.")
        self._escribir_texto(self.tarjetas_funciones, "Sin datos de funciones por tramos.")
        self._reiniciar_canvas(self.canvas_conica, "Canonica no disponible")
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
        self.current_reporte_conica = None
        self.current_datos_canonica = None
        self.current_analisis_funcion = None
        self.current_conica_limites = None
        self.current_funcion_limites = None
        if hasattr(self, "rut_entry"):
            self.rut_entry.focus_set()

    def _cargar_estado_invalido(self, texto_validacion):
        self._actualizar_estado_visual("RUT inválido. Revisa formato y dígito verificador.", "error")
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
                raise ValueError("Función no definida en a.")
            return (datos_rut["d5"] + 1) / (x - a)

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
        limites_por_defecto = None

        if tipo_conica == "Circunferencia":
            h, k = datos_canonica["centro"]
            r = datos_canonica["radio"]
            for indice in range(181):
                angulo = (indice * PI) / 90
                puntos.append((h + (r * coseno(angulo)), k + (r * seno(angulo))))
            limites_por_defecto = (h - r - 2, h + r + 2, k - r - 2, k + r + 2)

        elif tipo_conica == "Elipse":
            h, k = datos_canonica["centro"]
            a = raiz_cuadrada(datos_canonica["a_cuadrado"])
            b = raiz_cuadrada(datos_canonica["b_cuadrado"])
            for indice in range(181):
                angulo = (indice * PI) / 90
                puntos.append((h + (a * coseno(angulo)), k + (b * seno(angulo))))
            limites_por_defecto = (h - a - 2, h + a + 2, k - b - 2, k + b + 2)

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
            limites_por_defecto = (h - 8, h + 8, k - 8, k + 8)

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
            limites_por_defecto = (vertice[0] - 8, vertice[0] + 8, vertice[1] - 8, vertice[1] + 8)
        else:
            self._reiniciar_canvas(canvas, "Cónica no disponible")
            return

        limites = self.current_conica_limites if self.current_conica_limites is not None else limites_por_defecto
        mapper = self._crear_transformador(canvas, limites)
        self._dibujar_ejes(canvas, mapper, limites, width, height)
        self.current_conica_limites = limites

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
        limites = (
            self.current_funcion_limites
            if self.current_funcion_limites is not None
            else self._calcular_limites_funcion(analisis_funcion)
        )
        if self.current_funcion_limites is None:
            self.current_funcion_limites = limites
        mapper = self._crear_transformador(canvas, limites)
        self._dibujar_ejes(canvas, mapper, limites, int(canvas["width"]), int(canvas["height"]))

        if "Removible" in tipo:
            puntos = []
            for indice in range(161):
                x = a - 4 + (indice * 0.05)
                if valor_absoluto(x - a) > 1e-6:
                    puntos.append((x, x + analisis_funcion["funcion_info"]["parametros"]["d1"]))
            self._dibujar_curva(canvas, mapper, puntos, "#d46a00")
            x, y = mapper(a, a + analisis_funcion["funcion_info"]["parametros"]["d1"])
            canvas.create_oval(x - 6, y - 6, x + 6, y + 6, outline="#d46a00", width=2)
        elif "Salto" in tipo:
            izquierda = []
            derecha = []
            for indice in range(81):
                x_izq = a - 4 + (indice * 0.05)
                x_der = a + (indice * 0.05)
                if x_izq < a:
                    izquierda.append((x_izq, x_izq + analisis_funcion["funcion_info"]["parametros"]["d2"]))
                if x_der >= a:
                    derecha.append((x_der, x_der + analisis_funcion["funcion_info"]["parametros"]["d4"]))
            self._dibujar_curva(canvas, mapper, izquierda, "#d46a00")
            self._dibujar_curva(canvas, mapper, derecha, "#355c7d")
            x1, y1 = mapper(a, a + analisis_funcion["funcion_info"]["parametros"]["d2"])
            x2, y2 = mapper(a, a + analisis_funcion["funcion_info"]["parametros"]["d4"])
            canvas.create_oval(x1 - 6, y1 - 6, x1 + 6, y1 + 6, outline="#d46a00", width=2)
            canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill="#355c7d", outline="#355c7d")
        else:
            izquierda = []
            derecha = []
            for indice in range(132):
                x_izq = a - 4 + (indice * 0.03)
                x_der = a + 0.06 + (indice * 0.03)
                if x_izq < a - 0.06:
                    izquierda.append((x_izq, analisis_funcion["funcion_info"]["parametros"]["d5_mas_1"] / (x_izq - a)))
                if x_der > a + 0.06:
                    derecha.append((x_der, analisis_funcion["funcion_info"]["parametros"]["d5_mas_1"] / (x_der - a)))
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

    def _calcular_limites_funcion(self, analisis_funcion):
        a = analisis_funcion["punto_critico"]
        tipo = analisis_funcion["funcion_info"]["tipo_discontinuidad"]
        xmin = a - 4
        xmax = a + 4
        valores_y = []

        if "Removible" in tipo:
            for indice in range(161):
                x = xmin + (indice * 0.05)
                if valor_absoluto(x - a) > 1e-6:
                    valores_y.append(x + analisis_funcion["funcion_info"]["parametros"]["d1"])
        elif "Salto" in tipo:
            for indice in range(81):
                x_izq = xmin + (indice * 0.05)
                x_der = a + (indice * 0.05)
                if x_izq < a:
                    valores_y.append(x_izq + analisis_funcion["funcion_info"]["parametros"]["d2"])
                if x_der >= a:
                    valores_y.append(x_der + analisis_funcion["funcion_info"]["parametros"]["d4"])
        else:
            for indice in range(132):
                x_izq = xmin + (indice * 0.03)
                x_der = a + 0.06 + (indice * 0.03)
                if x_izq < a - 0.06:
                    y_izq = analisis_funcion["funcion_info"]["parametros"]["d5_mas_1"] / (x_izq - a)
                    if valor_absoluto(y_izq) <= 15:
                        valores_y.append(y_izq)
                if x_der > a + 0.06:
                    y_der = analisis_funcion["funcion_info"]["parametros"]["d5_mas_1"] / (x_der - a)
                    if valor_absoluto(y_der) <= 15:
                        valores_y.append(y_der)

        if not valores_y:
            return (xmin, xmax, -8, 12)

        ymin = min(valores_y)
        ymax = max(valores_y)
        margen = max((ymax - ymin) * 0.15, 2)
        return (xmin, xmax, ymin - margen, ymax + margen)

    def _on_canvas_conica_resize(self, event):
        if self.current_reporte_conica and self.current_datos_canonica:
            self.canvas_conica.config(width=event.width, height=event.height)
            self._dibujar_conica(self.current_reporte_conica.tipo_conica, self.current_datos_canonica)

    def _on_canvas_funcion_resize(self, event):
        if self.current_analisis_funcion:
            self.canvas_funcion.config(width=event.width, height=event.height)
            self._dibujar_funcion(self.current_analisis_funcion)

    def _toggle_grafico_conica(self):
        self.grafico_conica_expandido = not self.grafico_conica_expandido
        if self.grafico_conica_expandido:
            self.descripcion_grafico_conica.grid()
            self.canvas_conica.grid()
            self.panel_grafico_conica.rowconfigure(2, weight=1, minsize=360)
            self.panel_derecho_conicas.rowconfigure(0, weight=1, minsize=460)
            self.boton_grafico_conica.configure(text="Ocultar")
        else:
            self.descripcion_grafico_conica.grid_remove()
            self.canvas_conica.grid_remove()
            self.panel_grafico_conica.rowconfigure(2, weight=0, minsize=0)
            self.panel_derecho_conicas.rowconfigure(0, weight=0, minsize=72)
            self.boton_grafico_conica.configure(text="Mostrar")

    def _toggle_grafico_funcion(self):
        self.grafico_funcion_expandido = not self.grafico_funcion_expandido
        if self.grafico_funcion_expandido:
            self.descripcion_grafico_funcion.grid()
            self.canvas_funcion.grid()
            self.panel_grafico_funcion.rowconfigure(2, weight=1, minsize=280)
            self.panel_derecho_funciones.rowconfigure(0, weight=4, minsize=360)
            self.boton_grafico_funcion.configure(text="Ocultar")
        else:
            self.descripcion_grafico_funcion.grid_remove()
            self.canvas_funcion.grid_remove()
            self.panel_grafico_funcion.rowconfigure(2, weight=0, minsize=0)
            self.panel_derecho_funciones.rowconfigure(0, weight=0, minsize=72)
            self.boton_grafico_funcion.configure(text="Mostrar")

    def _toggle_tabla_apoyo(self):
        self.tabla_apoyo_expandida = not self.tabla_apoyo_expandida
        if self.tabla_apoyo_expandida:
            self.descripcion_tabla_apoyo.grid()
            self.tabla_valores.grid()
            self.panel_tabla_apoyo.rowconfigure(2, weight=1, minsize=180)
            self.panel_derecho_funciones.rowconfigure(2, weight=2, minsize=260)
            self.boton_tabla_apoyo.configure(text="Ocultar")
        else:
            self.descripcion_tabla_apoyo.grid_remove()
            self.tabla_valores.grid_remove()
            self.panel_tabla_apoyo.rowconfigure(2, weight=0, minsize=0)
            self.panel_derecho_funciones.rowconfigure(2, weight=0, minsize=72)
            self.boton_tabla_apoyo.configure(text="Mostrar")

    def _pixel_a_coordenada(self, canvas, px, py, limites):
        xmin, xmax, ymin, ymax = limites
        width = int(canvas["width"])
        height = int(canvas["height"])
        padding = 35
        x = xmin + ((px - padding) / (width - 2 * padding)) * (xmax - xmin)
        y = ymax - ((py - padding) / (height - 2 * padding)) * (ymax - ymin)
        return x, y

    def _inicio_arrastre(self, event, tipo):
        if tipo == "conica":
            limites = self.current_conica_limites
        else:
            limites = self.current_funcion_limites
        if limites is None:
            return
        self.drag_start[tipo] = {
            "x": event.x,
            "y": event.y,
            "limites": limites,
        }

    def _mover_arrastre(self, event, tipo):
        estado = self.drag_start.get(tipo)
        if not estado:
            return
        limites = estado["limites"]
        dx = event.x - estado["x"]
        dy = event.y - estado["y"]
        width = int(self.canvas_conica["width"]) if tipo == "conica" else int(self.canvas_funcion["width"])
        height = int(self.canvas_conica["height"]) if tipo == "conica" else int(self.canvas_funcion["height"])
        padding = 35
        rango_x = limites[1] - limites[0]
        rango_y = limites[3] - limites[2]

        desplazamiento_x = -dx * rango_x / (width - 2 * padding)
        desplazamiento_y = dy * rango_y / (height - 2 * padding)

        nuevos_limites = (
            limites[0] + desplazamiento_x,
            limites[1] + desplazamiento_x,
            limites[2] + desplazamiento_y,
            limites[3] + desplazamiento_y,
        )

        if tipo == "conica":
            self.current_conica_limites = nuevos_limites
            self._dibujar_conica(self.current_reporte_conica.tipo_conica, self.current_datos_canonica)
        else:
            self.current_funcion_limites = nuevos_limites
            self._dibujar_funcion(self.current_analisis_funcion)

    def _finalizar_arrastre(self, event, tipo):
        estado = self.drag_start.get(tipo)
        if not estado:
            return
        dx = event.x - estado["x"]
        dy = event.y - estado["y"]
        distancia = dx * dx + dy * dy
        if distancia <= 9:
            self._recentrar_por_click(event, tipo)
        self.drag_start[tipo] = None

    def _recentrar_por_click(self, event, tipo):
        limites = self.current_conica_limites if tipo == "conica" else self.current_funcion_limites
        if limites is None:
            return
        canvas = self.canvas_conica if tipo == "conica" else self.canvas_funcion
        x_click, y_click = self._pixel_a_coordenada(canvas, event.x, event.y, limites)
        x_centro = (limites[0] + limites[1]) / 2
        y_centro = (limites[2] + limites[3]) / 2
        dx = x_click - x_centro
        dy = y_click - y_centro
        nuevos_limites = (
            limites[0] + dx,
            limites[1] + dx,
            limites[2] + dy,
            limites[3] + dy,
        )
        if tipo == "conica":
            self.current_conica_limites = nuevos_limites
            self._dibujar_conica(self.current_reporte_conica.tipo_conica, self.current_datos_canonica)
        else:
            self.current_funcion_limites = nuevos_limites
            self._dibujar_funcion(self.current_analisis_funcion)

    def _zoom(self, event, tipo):
        if tipo == "conica":
            limites = self.current_conica_limites
            canvas = self.canvas_conica
        else:
            limites = self.current_funcion_limites
            canvas = self.canvas_funcion
        if limites is None:
            return

        if hasattr(event, 'delta') and event.delta != 0:
            delta = event.delta
        elif event.num == 4:
            delta = 120
        elif event.num == 5:
            delta = -120
        else:
            return

        zoom_factor = 1.1 if delta > 0 else 0.9
        x_mouse, y_mouse = self._pixel_a_coordenada(canvas, event.x, event.y, limites)

        xmin, xmax, ymin, ymax = limites
        ancho = xmax - xmin
        alto = ymax - ymin

        nuevo_ancho = ancho / zoom_factor
        nuevo_alto = alto / zoom_factor

        x_rel = (x_mouse - xmin) / ancho if ancho != 0 else 0.5
        y_rel = (y_mouse - ymin) / alto if alto != 0 else 0.5

        nuevo_xmin = x_mouse - x_rel * nuevo_ancho
        nuevo_xmax = nuevo_xmin + nuevo_ancho
        nuevo_ymin = y_mouse - y_rel * nuevo_alto
        nuevo_ymax = nuevo_ymin + nuevo_alto

        nuevos_limites = (nuevo_xmin, nuevo_xmax, nuevo_ymin, nuevo_ymax)

        if tipo == "conica":
            self.current_conica_limites = nuevos_limites
            self._dibujar_conica(self.current_reporte_conica.tipo_conica, self.current_datos_canonica)
        else:
            self.current_funcion_limites = nuevos_limites
            self._dibujar_funcion(self.current_analisis_funcion)

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

    def _paso_cuadricula(self, rango):
        if rango <= 0:
            return 1

        pasos_objetivo = 8
        paso = rango / pasos_objetivo
        escala = 1
        while escala * 10 <= paso:
            escala *= 10

        if paso <= escala:
            return escala
        if paso <= escala * 2:
            return escala * 2
        if paso <= escala * 5:
            return escala * 5
        return escala * 10

    def _alinear_hacia_abajo(self, valor, paso):
        if paso == 0:
            return valor
        numerador = valor / paso
        entero = int(numerador)
        while entero * paso > valor:
            entero -= 1
        return entero * paso

    def _alinear_hacia_arriba(self, valor, paso):
        if paso == 0:
            return valor
        numerador = valor / paso
        entero = int(numerador)
        while entero * paso < valor:
            entero += 1
        return entero * paso

    def _dibujar_ejes(self, canvas, mapper, limites, width, height):
        xmin, xmax, ymin, ymax = limites
        paso_x = self._paso_cuadricula(xmax - xmin)
        paso_y = self._paso_cuadricula(ymax - ymin)
        x_inicio = self._alinear_hacia_abajo(xmin, paso_x)
        x_final = self._alinear_hacia_arriba(xmax, paso_x)
        y_inicio = self._alinear_hacia_abajo(ymin, paso_y)
        y_final = self._alinear_hacia_arriba(ymax, paso_y)
        cero_x, cero_y = mapper(0, 0)

        linea_x = x_inicio
        while linea_x <= x_final + 1e-9:
            px1, py1 = mapper(linea_x, ymin)
            px2, py2 = mapper(linea_x, ymax)
            es_eje_y = abs(linea_x) < 1e-9
            color = "#e7dfd1" if not es_eje_y else "#c7b8a4"
            width_line = 1 if not es_eje_y else 2
            canvas.create_line(px1, py1, px2, py2, fill=color, width=width_line)

            if ymin <= 0 <= ymax:
                label_y = cero_y + 14 if cero_y + 14 < height - 12 else height - 12
            else:
                label_y = height - 12
            canvas.create_text(
                px1 + 2,
                label_y,
                text=self._formatear_numero_etiqueta(linea_x, paso_x),
                fill="#6f6154",
                font=("Segoe UI", 8),
                anchor="n",
            )
            linea_x += paso_x

        linea_y = y_inicio
        while linea_y <= y_final + 1e-9:
            px1, py1 = mapper(xmin, linea_y)
            px2, py2 = mapper(xmax, linea_y)
            es_eje_x = abs(linea_y) < 1e-9
            color = "#e7dfd1" if not es_eje_x else "#c7b8a4"
            width_line = 1 if not es_eje_x else 2
            canvas.create_line(px1, py1, px2, py2, fill=color, width=width_line)

            if xmin <= 0 <= xmax:
                label_x = cero_x + 12 if cero_x + 12 < width - 12 else width - 12
            else:
                label_x = 12
            canvas.create_text(
                label_x,
                py2 - 2,
                text=self._formatear_numero_etiqueta(linea_y, paso_y),
                fill="#6f6154",
                font=("Segoe UI", 8),
                anchor="w",
            )
            linea_y += paso_y

        if xmin <= 0 <= xmax:
            canvas.create_line(cero_x, 18, cero_x, height - 18, fill="#7a6a55", width=2)
        if ymin <= 0 <= ymax:
            canvas.create_line(18, cero_y, width - 18, cero_y, fill="#7a6a55", width=2)

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
            if getattr(child, "_persistir_panel", False):
                continue
            child.destroy()

        fila_inicial = 2
        for fila, etiqueta in enumerate(etiquetas, start=fila_inicial):
            ctk.CTkLabel(frame, text=etiqueta, text_color="#2d241d").grid(row=fila, column=0, sticky="w", pady=4)
            ctk.CTkEntry(frame, width=400).grid(row=fila, column=1, sticky="ew", padx=(10, 0), pady=4)

    def _actualizar_tabla(self, filas):
        for item in self.tabla_valores.get_children():
            self.tabla_valores.delete(item)

        for fila in filas:
            fx = "No definida" if fila["f(x)"] is None else self._formatear_numero(fila["f(x)"])
            etiqueta = "critico" if fila.get("tipo") == "critico" else "normal"
            self.tabla_valores.insert(
                "",
                "end",
                values=(self._formatear_numero(fila["x"]), fila["posicion"], fx),
                tags=(etiqueta,),
            )

    def _escribir_texto(self, widget, contenido):
        if hasattr(widget, 'limpiar') and hasattr(widget, 'agregar_tarjeta'):
            # Es un contenedor de tarjetas
            self._agregar_tarjetas(widget, contenido)
        else:
            # Es un ScrolledText (mantener compatibilidad)
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, self._limpiar_texto(contenido))
            widget.config(state="disabled")

    def _crear_contenedor_tarjetas(self, parent):
        """Crea un contenedor scrollable para tarjetas"""
        contenedor = ctk.CTkFrame(parent, fg_color="transparent")
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)
        
        # Canvas para scroll
        canvas = tk.Canvas(contenedor, bg="#fffdfa", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")
        
        # Frame interno que contendrá las tarjetas
        frame_tarjetas = ctk.CTkFrame(canvas, fg_color="transparent")
        frame_tarjetas.columnconfigure(0, weight=1)
        
        # Crear ventana en el canvas
        window_id = canvas.create_window(0, 0, window=frame_tarjetas, anchor="nw")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.config(yscrollcommand=scrollbar.set)
        
        # Actualizar región del scroll
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(window_id, width=canvas.winfo_width() - 15)
        
        frame_tarjetas.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_frame_configure)
        
        # Bind mouse wheel
        def on_mousewheel(event):
            if event.delta > 0:
                canvas.yview_scroll(-3, "units")
            else:
                canvas.yview_scroll(3, "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Guardar referencias
        contenedor.canvas = canvas
        contenedor.frame_tarjetas = frame_tarjetas
        contenedor.contador_tarjetas = 0
        contenedor.limpiar = lambda: self._limpiar_tarjetas(contenedor, frame_tarjetas)
        contenedor.agregar_tarjeta = lambda titulo, contenido: self._agregar_tarjeta_visual(contenedor, frame_tarjetas, titulo, contenido)
        
        return contenedor

    def _limpiar_tarjetas(self, contenedor, frame_tarjetas):
        """Elimina todas las tarjetas del contenedor"""
        for widget in frame_tarjetas.winfo_children():
            widget.destroy()
        contenedor.contador_tarjetas = 0

    def _agregar_tarjeta_visual(self, contenedor, frame_tarjetas, titulo, contenido):
        """Agrega una tarjeta visual con título y contenido"""
        tarjeta = ctk.CTkFrame(
            frame_tarjetas,
            fg_color=self.colores["panel"],
            corner_radius=12,
            border_width=1,
            border_color=self.colores["borde"],
        )
        tarjeta.grid(row=contenedor.contador_tarjetas, column=0, sticky="ew", padx=8, pady=6)
        tarjeta.columnconfigure(0, weight=1)
        contenedor.contador_tarjetas += 1
        
        # Título
        if titulo:
            titulo_label = ctk.CTkLabel(
                tarjeta,
                text=titulo,
                text_color=self.colores["texto"],
                font=("Segoe UI Semibold", 11),
                anchor="w",
                justify="left"
            )
            titulo_label.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        
        # Contenido
        contenido_label = ctk.CTkLabel(
            tarjeta,
            text=self._limpiar_texto(contenido),
            text_color=self.colores["texto"],
            font=("Consolas", 9),
            anchor="nw",
            justify="left",
            wraplength=500
        )
        contenido_label.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        
        return tarjeta

    def _agregar_tarjetas(self, widget_contenedor, contenido):
        """Divide el contenido en secciones y crea tarjetas"""
        # Limpiar tarjetas previas
        widget_contenedor.limpiar()
        
        # Dividir por secciones usando líneas que comienzan con "SECCIÓN" o números con punto
        lineas = contenido.split("\n")
        tarjetas_datos = []
        titulo_actual = None
        contenido_actual = []
        
        for linea in lineas:
            linea_strip = linea.strip()
            # Detectar títulos de sección
            if linea_strip.startswith("SECCIÓN") or (linea_strip and linea_strip[0].isdigit() and "." in linea_strip[:3]):
                # Guardar tarjeta anterior si existe
                if titulo_actual or contenido_actual:
                    tarjetas_datos.append((titulo_actual, "\n".join(contenido_actual)))
                
                titulo_actual = linea_strip
                contenido_actual = []
            elif linea_strip or contenido_actual:  # Agregar línea si no está vacía o ya hay contenido
                contenido_actual.append(linea)
        
        # Guardar última tarjeta
        if titulo_actual or contenido_actual:
            tarjetas_datos.append((titulo_actual, "\n".join(contenido_actual)))
        
        # Crear tarjetas visuales
        for titulo, contenido_tarjeta in tarjetas_datos:
            if titulo or contenido_tarjeta.strip():
                widget_contenedor.agregar_tarjeta(titulo, contenido_tarjeta)

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

    def _dibujar_funcion(self, analisis_funcion):
        canvas = self.canvas_funcion
        canvas.delete("all")
        a = analisis_funcion["punto_critico"]
        funcion_info = analisis_funcion["funcion_info"]
        caso = funcion_info["caso"]
        limites = (
            self.current_funcion_limites
            if self.current_funcion_limites is not None
            else self._calcular_limites_funcion(analisis_funcion)
        )
        if self.current_funcion_limites is None:
            self.current_funcion_limites = limites
        mapper = self._crear_transformador(canvas, limites)
        self._dibujar_ejes(canvas, mapper, limites, int(canvas["width"]), int(canvas["height"]))

        if caso == "removible":
            d1 = funcion_info["parametros"]["d1"]
            puntos = []
            for indice in range(161):
                x = a - 4 + (indice * 0.05)
                if valor_absoluto(x - a) > 1e-6:
                    puntos.append((x, x + d1))
            self._dibujar_curva(canvas, mapper, puntos, "#d46a00")
            x_hueco, y_hueco = mapper(a, a + d1)
            canvas.create_oval(x_hueco - 6, y_hueco - 6, x_hueco + 6, y_hueco + 6, outline="#d46a00", width=2)
        elif caso == "salto":
            d2 = funcion_info["parametros"]["d2"]
            d4 = funcion_info["parametros"]["d4"]
            izquierda = []
            derecha = []
            for indice in range(81):
                x_izq = a - 4 + (indice * 0.05)
                x_der = a + (indice * 0.05)
                if x_izq < a:
                    izquierda.append((x_izq, x_izq + d2))
                derecha.append((x_der, x_der + d4))
            self._dibujar_curva(canvas, mapper, izquierda, "#d46a00")
            self._dibujar_curva(canvas, mapper, derecha, "#355c7d")
            x1, y1 = mapper(a, a + d2)
            x2, y2 = mapper(a, a + d4)
            canvas.create_oval(x1 - 6, y1 - 6, x1 + 6, y1 + 6, outline="#d46a00", width=2)
            canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill="#355c7d", outline="#355c7d")
        else:
            numerador = funcion_info["parametros"]["d5_mas_1"]
            izquierda = []
            derecha = []
            for indice in range(132):
                x_izq = a - 4 + (indice * 0.03)
                x_der = a + 0.06 + (indice * 0.03)
                if x_izq < a - 0.06:
                    izquierda.append((x_izq, numerador / (x_izq - a)))
                if x_der > a + 0.06:
                    derecha.append((x_der, numerador / (x_der - a)))
            self._dibujar_curva(canvas, mapper, izquierda, "#d46a00")
            self._dibujar_curva(canvas, mapper, derecha, "#355c7d")
            x1, _ = mapper(a, 0)
            canvas.create_line(x1, 20, x1, int(canvas["height"]) - 20, fill="#9f7f5b", dash=(5, 4), width=2)

        canvas.create_text(
            12,
            12,
            anchor="nw",
            text=f"{funcion_info['tipo_discontinuidad']} en x = {a}",
            fill="#2d241d",
            font=("Segoe UI Semibold", 10),
        )

    def _calcular_limites_funcion(self, analisis_funcion):
        a = analisis_funcion["punto_critico"]
        funcion_info = analisis_funcion["funcion_info"]
        caso = funcion_info["caso"]
        xmin = a - 4
        xmax = a + 4
        valores_y = []

        if caso == "removible":
            d1 = funcion_info["parametros"]["d1"]
            for indice in range(161):
                x = xmin + (indice * 0.05)
                if valor_absoluto(x - a) > 1e-6:
                    valores_y.append(x + d1)
        elif caso == "salto":
            d2 = funcion_info["parametros"]["d2"]
            d4 = funcion_info["parametros"]["d4"]
            for indice in range(81):
                x_izq = xmin + (indice * 0.05)
                x_der = a + (indice * 0.05)
                if x_izq < a:
                    valores_y.append(x_izq + d2)
                valores_y.append(x_der + d4)
        else:
            numerador = funcion_info["parametros"]["d5_mas_1"]
            for indice in range(132):
                x_izq = xmin + (indice * 0.03)
                x_der = a + 0.06 + (indice * 0.03)
                if x_izq < a - 0.06:
                    y_izq = numerador / (x_izq - a)
                    if valor_absoluto(y_izq) <= 15:
                        valores_y.append(y_izq)
                if x_der > a + 0.06:
                    y_der = numerador / (x_der - a)
                    if valor_absoluto(y_der) <= 15:
                        valores_y.append(y_der)

        if not valores_y:
            return (xmin, xmax, -8, 12)

        ymin = min(valores_y)
        ymax = max(valores_y)
        margen = max((ymax - ymin) * 0.15, 2)
        return (xmin, xmax, ymin - margen, ymax + margen)

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

    def _formatear_numero_etiqueta(self, numero, paso):
        if isinstance(numero, str):
            return numero
        if float(paso).is_integer():
            return str(int(round(numero)))
        return f"{numero:.1f}"

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
