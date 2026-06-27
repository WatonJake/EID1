import tkinter as tk
from tkinter import ttk

import customtkinter as ctk


class UiMixin:
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

        self.estado_var = tk.StringVar(value="")
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
        self.estado_badge.destroy()
        self.estado_badge = None
        self.estado_var.set("")

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
            "Usa esta pestaña para explicar el procedimiento paso a paso. La franja superior resume el resultado y aquí queda el detalle.",
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
        titulo_label.grid(row=0, column=0, sticky="w", padx=14, pady=(12, 2))
        titulo_label._persistir_panel = True
        descripcion_label = ctk.CTkLabel(
            panel,
            text=descripcion,
            text_color=self.colores["texto_sec"],
            font=("Segoe UI", 10),
            wraplength=360,
            justify="left",
        )
        descripcion_label.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 6))
        descripcion_label._persistir_panel = True
        return panel

    def _crear_tab_conicas(self):
        self.tab_conicas.columnconfigure(0, weight=5)
        self.tab_conicas.columnconfigure(1, weight=1)
        self.tab_conicas.rowconfigure(0, weight=1)

        self.tarjetas_conicas = self._crear_contenedor_tarjetas(self.tab_conicas)
        self.tarjetas_conicas.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        panel_derecho = ctk.CTkFrame(self.tab_conicas, fg_color="transparent")
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=0)
        self.panel_derecho_conicas = panel_derecho

        panel_grafico = self._crear_panel_lateral(
            panel_derecho,
            "Visualizacion de la conica",
            "Abre el grafico en una ventana separada para dejar mas espacio al desarrollo del procedimiento.",
        )
        panel_grafico.grid(row=0, column=0, sticky="nsew")
        panel_grafico.columnconfigure(0, weight=1)
        panel_grafico.rowconfigure(2, weight=0)
        self.panel_grafico_conica = panel_grafico
        self.descripcion_grafico_conica = panel_grafico.winfo_children()[1]
        self.boton_grafico_conica = ctk.CTkButton(
            panel_grafico,
            text="Graficar conica",
            width=180,
            height=40,
            corner_radius=10,
            fg_color=self.colores["acento"],
            hover_color=self.colores["acento_oscuro"],
            text_color="#fffaf4",
            font=("Segoe UI Semibold", 12),
            command=self._mostrar_popup_conica,
        )
        self.boton_grafico_conica.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 14))

        self.boton_defensa_conica = ctk.CTkButton(
            panel_grafico,
            text="Rellenado de defensa",
            width=180,
            height=40,
            corner_radius=10,
            fg_color="#eadfce",
            hover_color="#dfcfb7",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 12),
            command=self._mostrar_popup_defensa_conica,
        )
        self.boton_defensa_conica.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 14))

        self.frame_inputs_conica = ctk.CTkFrame(self.tab_conicas, fg_color="transparent")
        self.frame_inputs_conica.columnconfigure(1, weight=1)

    def _crear_tab_funciones(self):
        self.tab_funciones.columnconfigure(0, weight=5)
        self.tab_funciones.columnconfigure(1, weight=2)
        self.tab_funciones.rowconfigure(0, weight=1)

        self.tarjetas_funciones = self._crear_contenedor_tarjetas(self.tab_funciones)
        self.tarjetas_funciones.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        panel_derecho = ctk.CTkFrame(self.tab_funciones, fg_color="transparent")
        panel_derecho.grid(row=0, column=1, sticky="nsew")
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=0)
        panel_derecho.rowconfigure(2, weight=2, minsize=260)
        self.panel_derecho_funciones = panel_derecho

        panel_grafico = self._crear_panel_lateral(
            panel_derecho,
            "Visualizacion de la funcion",
            "Abre el grafico en una ventana separada para dejar mas espacio al procedimiento y la tabla.",
        )
        panel_grafico.grid(row=0, column=0, sticky="nsew")
        panel_grafico.columnconfigure(0, weight=1)
        panel_grafico.rowconfigure(2, weight=0)
        self.panel_grafico_funcion = panel_grafico
        self.descripcion_grafico_funcion = panel_grafico.winfo_children()[1]
        self.boton_grafico_funcion = ctk.CTkButton(
            panel_grafico,
            text="Graficar funcion",
            width=180,
            height=40,
            corner_radius=10,
            fg_color=self.colores["acento"],
            hover_color=self.colores["acento_oscuro"],
            text_color="#fffaf4",
            font=("Segoe UI Semibold", 12),
            command=self._mostrar_popup_funcion,
        )
        self.boton_grafico_funcion.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 14))

        self.boton_defensa_funcion = ctk.CTkButton(
            panel_grafico,
            text="Rellenado de defensa",
            width=180,
            height=40,
            corner_radius=10,
            fg_color="#eadfce",
            hover_color="#dfcfb7",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 12),
            command=self._mostrar_popup_defensa_funcion,
        )
        self.boton_defensa_funcion.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 14))

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
        panel_tabla.rowconfigure(2, weight=0, minsize=0)
        self.panel_tabla_apoyo = panel_tabla
        self.descripcion_tabla_apoyo = panel_tabla.winfo_children()[1]
        self.boton_tabla_apoyo = ctk.CTkButton(
            panel_tabla,
            text="Abrir tabla",
            width=180,
            height=40,
            corner_radius=10,
            fg_color=self.colores["acento"],
            hover_color=self.colores["acento_oscuro"],
            text_color="#fffaf4",
            font=("Segoe UI Semibold", 12),
            command=self._mostrar_popup_tabla_apoyo,
        )
        self.boton_tabla_apoyo.grid(row=2, column=0, sticky="ew", padx=14, pady=(6, 14))

        self.tabla_valores = ttk.Treeview(
            panel_tabla,
            columns=("x", "lado", "fx"),
            show="headings",
            height=8,
        )
        self._configurar_tabla_valores(self.tabla_valores)

    def _mostrar_popup_defensa_conica(self):
        self._asegurar_popup_defensa("conica")
        self.ventana_defensa_conica.deiconify()
        self.ventana_defensa_conica.lift()
        self.ventana_defensa_conica.focus_force()
        self._crear_campos_vacios(self.frame_defensa_conica, self.campos_defensa_conica)

    def _mostrar_popup_defensa_funcion(self):
        self._asegurar_popup_defensa("funcion")
        self.ventana_defensa_funcion.deiconify()
        self.ventana_defensa_funcion.lift()
        self.ventana_defensa_funcion.focus_force()
        self._crear_campos_vacios(self.frame_defensa_funcion, self.campos_defensa_funcion)

    def _asegurar_popup_defensa(self, tipo):
        if tipo == "conica" and self.ventana_defensa_conica is not None and self.ventana_defensa_conica.winfo_exists():
            return
        if tipo == "funcion" and self.ventana_defensa_funcion is not None and self.ventana_defensa_funcion.winfo_exists():
            return

        ventana = ctk.CTkToplevel(self.root)
        ventana.geometry("760x620")
        ventana.minsize(640, 500)
        ventana.configure(fg_color=self.colores["fondo"])
        ventana.protocol("WM_DELETE_WINDOW", lambda t=tipo: self._cerrar_popup_defensa(t))

        contenedor = ctk.CTkFrame(
            ventana,
            fg_color=self.colores["panel"],
            corner_radius=16,
            border_width=1,
            border_color=self.colores["borde"],
        )
        contenedor.pack(fill="both", expand=True, padx=16, pady=16)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(1, weight=1)

        if tipo == "conica":
            ventana.title("Rellenado de defensa - Conica")
            titulo = "Rellenado de defensa - Conica"
            descripcion = "Completa aqui centro, vertices, focos, ejes y directriz o asintotas segun la conica analizada."
            campos = self.campos_defensa_conica
        else:
            ventana.title("Rellenado de defensa - Funcion")
            titulo = "Rellenado de defensa - Funcion"
            descripcion = "Completa aqui limites laterales, continuidad, valor en el punto y la justificacion solicitada."
            campos = self.campos_defensa_funcion

        ctk.CTkLabel(
            contenedor,
            text=titulo,
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 16),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(
            contenedor,
            text=descripcion,
            text_color=self.colores["texto_sec"],
            font=("Segoe UI", 11),
            wraplength=680,
            justify="left",
        ).grid(row=0, column=0, sticky="e", padx=(220, 18), pady=(16, 4))

        frame_formulario = ctk.CTkFrame(
            contenedor,
            fg_color="#fffdfa",
            corner_radius=14,
            border_width=1,
            border_color=self.colores["borde"],
        )
        frame_formulario.grid(row=1, column=0, sticky="nsew", padx=18, pady=(10, 18))
        frame_formulario.columnconfigure(1, weight=1)

        if tipo == "conica":
            self.ventana_defensa_conica = ventana
            self.frame_defensa_conica = frame_formulario
        else:
            self.ventana_defensa_funcion = ventana
            self.frame_defensa_funcion = frame_formulario

        self._crear_campos_vacios(frame_formulario, campos)

    def _cerrar_popup_defensa(self, tipo):
        if tipo == "conica":
            if self.ventana_defensa_conica is not None and self.ventana_defensa_conica.winfo_exists():
                self.ventana_defensa_conica.destroy()
            self.ventana_defensa_conica = None
            self.frame_defensa_conica = None
        else:
            if self.ventana_defensa_funcion is not None and self.ventana_defensa_funcion.winfo_exists():
                self.ventana_defensa_funcion.destroy()
            self.ventana_defensa_funcion = None
            self.frame_defensa_funcion = None

    def _mostrar_popup_tabla_apoyo(self):
        self._asegurar_popup_tabla_apoyo()
        self.ventana_tabla_apoyo.deiconify()
        self.ventana_tabla_apoyo.lift()
        self.ventana_tabla_apoyo.focus_force()

    def _asegurar_popup_tabla_apoyo(self):
        if self.ventana_tabla_apoyo is not None and self.ventana_tabla_apoyo.winfo_exists():
            return

        ventana = ctk.CTkToplevel(self.root)
        ventana.geometry("760x520")
        ventana.minsize(640, 420)
        ventana.title("Tabla de apoyo")
        ventana.configure(fg_color=self.colores["fondo"])
        ventana.protocol("WM_DELETE_WINDOW", self._cerrar_popup_tabla_apoyo)

        contenedor = ctk.CTkFrame(
            ventana,
            fg_color=self.colores["panel"],
            corner_radius=16,
            border_width=1,
            border_color=self.colores["borde"],
        )
        contenedor.pack(fill="both", expand=True, padx=16, pady=16)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(1, weight=1)

        ctk.CTkLabel(
            contenedor,
            text="Tabla de apoyo",
            text_color=self.colores["texto"],
            font=("Segoe UI Semibold", 16),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(
            contenedor,
            text="La fila del punto critico queda resaltada para facilitar la lectura.",
            text_color=self.colores["texto_sec"],
            font=("Segoe UI", 11),
            wraplength=680,
            justify="left",
        ).grid(row=0, column=0, sticky="e", padx=(220, 18), pady=(16, 4))

        tabla = ttk.Treeview(
            contenedor,
            columns=("x", "lado", "fx"),
            show="headings",
            height=12,
        )
        self._configurar_tabla_valores(tabla)
        tabla.grid(row=1, column=0, sticky="nsew", padx=18, pady=(10, 18))
        self._cargar_filas_tabla(tabla, self.tabla_apoyo_filas)

        self.ventana_tabla_apoyo = ventana
        self.tabla_popup_valores = tabla

    def _cerrar_popup_tabla_apoyo(self):
        if self.ventana_tabla_apoyo is not None and self.ventana_tabla_apoyo.winfo_exists():
            self.ventana_tabla_apoyo.destroy()
        self.ventana_tabla_apoyo = None
        self.tabla_popup_valores = None

    def _configurar_tabla_valores(self, tabla):
        tabla.heading("x", text="x")
        tabla.heading("lado", text="Posicion")
        tabla.heading("fx", text="f(x)")
        tabla.column("x", width=90, anchor="center")
        tabla.column("lado", width=140, anchor="center")
        tabla.column("fx", width=120, anchor="center")
        tabla.tag_configure("critico", background="#f9ecd3")
        tabla.tag_configure("normal", background="#fffdfa")

    def _actualizar_tabla(self, filas):
        self.tabla_apoyo_filas = list(filas)
        self._cargar_filas_tabla(self.tabla_valores, filas)
        if self.tabla_popup_valores is not None:
            self._cargar_filas_tabla(self.tabla_popup_valores, filas)

    def _cargar_filas_tabla(self, tabla, filas):
        for item in tabla.get_children():
            tabla.delete(item)

        for fila in filas:
            fx = "No definida" if fila["f(x)"] is None else self._formatear_numero(fila["f(x)"])
            etiqueta = "critico" if fila.get("tipo") == "critico" else "normal"
            tabla.insert(
                "",
                "end",
                values=(self._formatear_numero(fila["x"]), fila["posicion"], fx),
                tags=(etiqueta,),
            )

    def _escribir_texto(self, widget, contenido):
        if hasattr(widget, "limpiar") and hasattr(widget, "agregar_tarjeta"):
            self._agregar_tarjetas(widget, contenido)
        else:
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, self._limpiar_texto(contenido))
            widget.config(state="disabled")

    def _crear_contenedor_tarjetas(self, parent):
        contenedor = ctk.CTkFrame(parent, fg_color="transparent")
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        canvas = tk.Canvas(contenedor, bg="#fffdfa", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        frame_tarjetas = ctk.CTkFrame(canvas, fg_color="transparent")
        frame_tarjetas.columnconfigure(0, weight=1)
        window_id = canvas.create_window(0, 0, window=frame_tarjetas, anchor="nw")

        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.config(yscrollcommand=scrollbar.set)

        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(window_id, width=canvas.winfo_width() - 15)

        frame_tarjetas.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_frame_configure)

        def on_mousewheel(event):
            if event.delta > 0:
                canvas.yview_scroll(-3, "units")
            else:
                canvas.yview_scroll(3, "units")

        canvas.bind("<MouseWheel>", on_mousewheel)

        contenedor.canvas = canvas
        contenedor.frame_tarjetas = frame_tarjetas
        contenedor.contador_tarjetas = 0
        contenedor.limpiar = lambda: self._limpiar_tarjetas(contenedor, frame_tarjetas)
        contenedor.agregar_tarjeta = lambda titulo, contenido: self._agregar_tarjeta_visual(
            contenedor, frame_tarjetas, titulo, contenido
        )
        return contenedor

    def _limpiar_tarjetas(self, contenedor, frame_tarjetas):
        for widget in frame_tarjetas.winfo_children():
            widget.destroy()
        contenedor.contador_tarjetas = 0

    def _agregar_tarjeta_visual(self, contenedor, frame_tarjetas, titulo, contenido):
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

        if titulo:
            titulo_label = ctk.CTkLabel(
                tarjeta,
                text=titulo,
                text_color=self.colores["texto"],
                font=("Segoe UI Semibold", 11),
                anchor="w",
                justify="left",
            )
            titulo_label.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))

        contenido_label = ctk.CTkLabel(
            tarjeta,
            text=self._limpiar_texto(contenido),
            text_color=self.colores["texto"],
            font=("Consolas", 9),
            anchor="nw",
            justify="left",
            wraplength=500,
        )
        contenido_label.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        return tarjeta

    def _agregar_tarjetas(self, widget_contenedor, contenido):
        widget_contenedor.limpiar()
        lineas = contenido.split("\n")
        tarjetas_datos = []
        titulo_actual = None
        contenido_actual = []

        for linea in lineas:
            linea_strip = linea.strip()
            if linea_strip.startswith("SECCIÓN") or (linea_strip and linea_strip[0].isdigit() and "." in linea_strip[:3]):
                if titulo_actual or contenido_actual:
                    tarjetas_datos.append((titulo_actual, "\n".join(contenido_actual)))
                titulo_actual = linea_strip
                contenido_actual = []
            elif linea_strip or contenido_actual:
                contenido_actual.append(linea)

        if titulo_actual or contenido_actual:
            tarjetas_datos.append((titulo_actual, "\n".join(contenido_actual)))

        for titulo, contenido_tarjeta in tarjetas_datos:
            if titulo or contenido_tarjeta.strip():
                widget_contenedor.agregar_tarjeta(titulo, contenido_tarjeta)

    def _crear_campos_vacios(self, frame, etiquetas):
        if frame is None:
            return

        for child in frame.winfo_children():
            if getattr(child, "_persistir_panel", False):
                continue
            child.destroy()

        fila_inicial = 2
        for fila, etiqueta in enumerate(etiquetas, start=fila_inicial):
            ctk.CTkLabel(frame, text=etiqueta, text_color="#2d241d").grid(
                row=fila, column=0, sticky="w", pady=4
            )
            ctk.CTkEntry(frame, width=400).grid(
                row=fila, column=1, sticky="ew", padx=(10, 0), pady=4
            )
