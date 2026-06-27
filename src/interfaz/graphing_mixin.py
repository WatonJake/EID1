import customtkinter as ctk
import tkinter as tk

from src.utilidades.matematica_manual import (
    PI,
    coseno,
    coseno_hiperbolico,
    raiz_cuadrada,
    seno,
    seno_hiperbolico,
    valor_absoluto,
)


class GraphingMixin:
    def _dibujar_conica(self, tipo_conica, datos_canonica):
        if self.canvas_conica is None:
            return
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

    def _on_canvas_conica_resize(self, event):
        if self.canvas_conica is None:
            return
        if self.current_reporte_conica and self.current_datos_canonica:
            self.canvas_conica.config(width=event.width, height=event.height)
            self._dibujar_conica(self.current_reporte_conica.tipo_conica, self.current_datos_canonica)

    def _on_canvas_funcion_resize(self, event):
        if self.canvas_funcion is None:
            return
        if self.current_analisis_funcion:
            self.canvas_funcion.config(width=event.width, height=event.height)
            self._dibujar_funcion(self.current_analisis_funcion)

    def _mostrar_popup_conica(self):
        self._asegurar_popup_grafico("conica")
        self.ventana_grafico_conica.deiconify()
        self.ventana_grafico_conica.lift()
        self.ventana_grafico_conica.focus_force()
        if self.current_reporte_conica and self.current_datos_canonica:
            self._dibujar_conica(self.current_reporte_conica.tipo_conica, self.current_datos_canonica)
        else:
            self._reiniciar_canvas(self.canvas_conica, "Canonica no disponible")

    def _mostrar_popup_funcion(self):
        self._asegurar_popup_grafico("funcion")
        self.ventana_grafico_funcion.deiconify()
        self.ventana_grafico_funcion.lift()
        self.ventana_grafico_funcion.focus_force()
        if self.current_analisis_funcion:
            self._dibujar_funcion(self.current_analisis_funcion)
        else:
            self._reiniciar_canvas(self.canvas_funcion, "Funcion no disponible")

    def _asegurar_popup_grafico(self, tipo):
        if tipo == "conica" and self.ventana_grafico_conica is not None and self.ventana_grafico_conica.winfo_exists():
            return
        if tipo == "funcion" and self.ventana_grafico_funcion is not None and self.ventana_grafico_funcion.winfo_exists():
            return

        ventana = ctk.CTkToplevel(self.root)
        ventana.geometry("860x620")
        ventana.minsize(720, 520)
        ventana.configure(fg_color=self.colores["fondo"])
        ventana.protocol("WM_DELETE_WINDOW", lambda t=tipo: self._cerrar_popup_grafico(t))

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
            ventana.title("Grafico de la conica")
            titulo = "Grafico de la conica"
            descripcion = "Arrastra para mover la vista y usa la rueda del mouse para acercar o alejar."
            alto = 520
        else:
            ventana.title("Grafico de la funcion")
            titulo = "Grafico de la funcion"
            descripcion = "Observa el comportamiento cerca del punto critico en una ventana separada."
            alto = 460

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
            wraplength=760,
            justify="left",
        ).grid(row=0, column=0, sticky="e", padx=(220, 18), pady=(16, 4))

        canvas = tk.Canvas(
            contenedor,
            width=780,
            height=alto,
            bg="#fffdfa",
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
        )
        canvas.grid(row=1, column=0, sticky="nsew", padx=18, pady=(10, 18))

        canvas.bind("<Configure>", self._on_canvas_conica_resize if tipo == "conica" else self._on_canvas_funcion_resize)
        canvas.bind("<ButtonPress-1>", lambda event, t=tipo: self._inicio_arrastre(event, t))
        canvas.bind("<B1-Motion>", lambda event, t=tipo: self._mover_arrastre(event, t))
        canvas.bind("<ButtonRelease-1>", lambda event, t=tipo: self._finalizar_arrastre(event, t))
        canvas.bind("<MouseWheel>", lambda event, t=tipo: self._zoom(event, t))
        canvas.bind("<Button-4>", lambda event, t=tipo: self._zoom(event, t))
        canvas.bind("<Button-5>", lambda event, t=tipo: self._zoom(event, t))

        if tipo == "conica":
            self.ventana_grafico_conica = ventana
            self.canvas_conica = canvas
        else:
            self.ventana_grafico_funcion = ventana
            self.canvas_funcion = canvas

    def _cerrar_popup_grafico(self, tipo):
        if tipo == "conica":
            if self.ventana_grafico_conica is not None and self.ventana_grafico_conica.winfo_exists():
                self.ventana_grafico_conica.destroy()
            self.ventana_grafico_conica = None
            self.canvas_conica = None
        else:
            if self.ventana_grafico_funcion is not None and self.ventana_grafico_funcion.winfo_exists():
                self.ventana_grafico_funcion.destroy()
            self.ventana_grafico_funcion = None
            self.canvas_funcion = None

    def _pixel_a_coordenada(self, canvas, px, py, limites):
        xmin, xmax, ymin, ymax = limites
        width = int(canvas["width"])
        height = int(canvas["height"])
        padding = 35
        x = xmin + ((px - padding) / (width - 2 * padding)) * (xmax - xmin)
        y = ymax - ((py - padding) / (height - 2 * padding)) * (ymax - ymin)
        return x, y

    def _inicio_arrastre(self, event, tipo):
        canvas = self.canvas_conica if tipo == "conica" else self.canvas_funcion
        if canvas is None:
            return
        limites = self.current_conica_limites if tipo == "conica" else self.current_funcion_limites
        if limites is None:
            return
        self.drag_start[tipo] = {"x": event.x, "y": event.y, "limites": limites}

    def _mover_arrastre(self, event, tipo):
        estado = self.drag_start.get(tipo)
        if not estado:
            return
        canvas = self.canvas_conica if tipo == "conica" else self.canvas_funcion
        if canvas is None:
            return
        limites = estado["limites"]
        dx = event.x - estado["x"]
        dy = event.y - estado["y"]
        width = int(canvas["width"])
        height = int(canvas["height"])
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
        if canvas is None:
            return
        x_click, y_click = self._pixel_a_coordenada(canvas, event.x, event.y, limites)
        x_centro = (limites[0] + limites[1]) / 2
        y_centro = (limites[2] + limites[3]) / 2
        dx = x_click - x_centro
        dy = y_click - y_centro
        nuevos_limites = (limites[0] + dx, limites[1] + dx, limites[2] + dy, limites[3] + dy)
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
        if limites is None or canvas is None:
            return

        if hasattr(event, "delta") and event.delta != 0:
            factor = 0.9 if event.delta > 0 else 1.1
        elif getattr(event, "num", None) == 4:
            factor = 0.9
        else:
            factor = 1.1

        x_centro, y_centro = self._pixel_a_coordenada(canvas, event.x, event.y, limites)
        xmin, xmax, ymin, ymax = limites
        nuevos_limites = (
            x_centro + ((xmin - x_centro) * factor),
            x_centro + ((xmax - x_centro) * factor),
            y_centro + ((ymin - y_centro) * factor),
            y_centro + ((ymax - y_centro) * factor),
        )

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

            label_y = cero_y + 14 if ymin <= 0 <= ymax and cero_y + 14 < height - 12 else height - 12
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

            label_x = cero_x + 12 if xmin <= 0 <= xmax and cero_x + 12 < width - 12 else 12
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
        if canvas is None:
            return
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

    def _dibujar_funcion(self, analisis_funcion):
        if self.canvas_funcion is None:
            return
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
