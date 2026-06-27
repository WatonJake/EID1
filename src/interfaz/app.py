import customtkinter as ctk

from src.interfaz.analysis_mixin import AnalysisMixin
from src.interfaz.formatting_mixin import FormattingMixin
from src.interfaz.graphing_mixin import GraphingMixin
from src.interfaz.ui_mixin import UiMixin


class App(UiMixin, AnalysisMixin, GraphingMixin, FormattingMixin):
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
        self.ventana_grafico_conica = None
        self.ventana_grafico_funcion = None
        self.ventana_defensa_conica = None
        self.ventana_defensa_funcion = None
        self.ventana_tabla_apoyo = None
        self.canvas_conica = None
        self.canvas_funcion = None
        self.frame_defensa_conica = None
        self.frame_defensa_funcion = None
        self.tabla_popup_valores = None
        self.tabla_apoyo_filas = []
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
