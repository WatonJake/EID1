# src/conicas/procedimiento_conica.py

class ProcedimientoConica:
    def __init__(self, digitos, v, coef_iniciales, coef_finales, reglas_aplicadas, ecuacion, tipo_conica, justificacion):
        self.digitos = digitos
        self.v = v
        self.coef_iniciales = coef_iniciales
        self.coef_finales = coef_finales
        self.reglas_aplicadas = reglas_aplicadas
        self.ecuacion = ecuacion
        self.tipo_conica = tipo_conica
        self.justificacion = justificacion

    def imprimir_reporte(self):
        print(f"Dígitos extraídos (d1 a d8): {self.digitos}")
        print(f"Variable auxiliar 'v'      : {self.v}")
        print("-" * 50)
        
        print("Coeficientes Iniciales (Fórmula base):")
        for letra, valor in self.coef_iniciales.items():
            print(f"  {letra} = {valor}")
        print("-" * 50)
        
        print("Reglas especiales aplicadas:")
        if not self.reglas_aplicadas:
            print("  - Ninguna regla especial alteró los coeficientes.")
        else:
            for regla in self.reglas_aplicadas:
                print(f"  - {regla}")
        print("-" * 50)

        print("Coeficientes Finales:")
        for letra, valor in self.coef_finales.items():
            print(f"  {letra} = {valor}")
        print("-" * 50)
        
        print(f"Ecuación General : {self.ecuacion}")
        print(f"Tipo de Cónica   : {self.tipo_conica}")
        print(f"Justificación    : {self.justificacion}")