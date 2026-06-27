from src.utilidades.matematica_manual import valor_absoluto


class FormattingMixin:
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
