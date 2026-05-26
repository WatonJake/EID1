# src/conicas/procedimiento_conica.py

class ProcedimientoConica:
    def __init__(self, digitos, v, coeficientes, reglas_aplicadas, ecuacion, tipo_conica, justificacion):
        """
        Clase para almacenar y mostrar los resultados del análisis de la cónica.
        """
        self.digitos = digitos
        self.v = v
        self.A = coeficientes.get('A', 0)
        self.B = coeficientes.get('B', 0)
        self.C = coeficientes.get('C', 0)
        self.D = coeficientes.get('D', 0)
        self.E = coeficientes.get('E', 0)
        self.reglas_aplicadas = reglas_aplicadas
        self.ecuacion = ecuacion
        self.tipo_conica = tipo_conica
        self.justificacion = justificacion

    def imprimir_reporte(self):
        """
        Imprime ordenadamente todos los datos de la cónica en la consola.
        """
        print("\n" + "="*60)
        print(" "*15 + "REPORTE DE SECCIÓN CÓNICA")
        print("="*60)
        
        print(f"Dígitos extraídos (d1 a d8): {self.digitos}")
        print(f"Variable auxiliar 'v'      : {self.v}")
        print("-" * 60)
        
        print("Coeficientes calculados:")
        print(f"  A = {self.A}")
        print(f"  B = {self.B}")
        print(f"  C = {self.C}")
        print(f"  D = {self.D}")
        print(f"  E = {self.E}")
        print("-" * 60)
        
        print("Reglas especiales aplicadas:")
        if not self.reglas_aplicadas:
            print("  - Ninguna regla especial fue activada.")
        else:
            for regla in self.reglas_aplicadas:
                print(f"  - {regla}")
        print("-" * 60)
        
        print(f"Ecuación General : {self.ecuacion}")
        print(f"Tipo de Cónica   : {self.tipo_conica}")
        print(f"Justificación    : {self.justificacion}")
        print("="*60 + "\n")