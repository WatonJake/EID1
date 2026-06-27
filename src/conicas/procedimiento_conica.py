class ProcedimientoConica:
    def __init__(
        self,
        digitos,
        v,
        coef_iniciales,
        coef_finales,
        reglas_aplicadas,
        ecuacion,
        tipo_conica,
        justificacion,
    ):
        self.digitos = digitos
        self.v = v
        self.coef_iniciales = coef_iniciales
        self.coef_finales = coef_finales
        self.reglas_aplicadas = reglas_aplicadas
        self.ecuacion = ecuacion
        self.tipo_conica = tipo_conica
        self.justificacion = justificacion

    def generar_reporte(self):
        lineas = [
            f"Dígitos extraídos (d1 a d8): {self.digitos}",
            f"Variable auxiliar v        : {self.v}",
            "-" * 50,
            "Construcción de coeficientes base:",
        ]

        for letra, valor in self.coef_iniciales.items():
            lineas.append(f"  {letra} = {valor}")

        lineas.extend(
            [
                "-" * 50,
                "Reglas especiales aplicadas:",
            ]
        )

        if not self.reglas_aplicadas:
            lineas.append("  - Ninguna regla especial alteró los coeficientes.")
        else:
            for regla in self.reglas_aplicadas:
                lineas.append(f"  - {regla}")

        lineas.extend(
            [
                "-" * 50,
                "Coeficientes finales:",
            ]
        )

        for letra, valor in self.coef_finales.items():
            lineas.append(f"  {letra} = {valor}")

        lineas.extend(
            [
                "-" * 50,
                f"Ecuación general : {self.ecuacion}",
                f"Tipo de cónica   : {self.tipo_conica}",
                f"Justificación    : {self.justificacion}",
            ]
        )
        return "\n".join(lineas)

    def imprimir_reporte(self):
        print(self.generar_reporte())
