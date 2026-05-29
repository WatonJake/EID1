"""
Ejemplo de uso del módulo funciones_tramos.

Este archivo demuestra cómo usar las funciones para generar y analizar
funciones por tramos con diferentes tipos de discontinuidades.
"""

from src.funciones_tramos import (
    generar_funcion_por_tramos,
    generar_puntos_cercanos,
    generar_procedimiento_funcion,
    generar_tabla_procedimiento
)


def ejemplo_basico():
    """Ejemplo básico de uso de las funciones."""
    
    print("=" * 80)
    print("EJEMPLO DE USO: MÓDULO FUNCIONES_TRAMOS")
    print("=" * 80)
    
    # Crear datos de RUT de ejemplo
    # Supongamos RUT: 12.345.678-9
    datos_rut = {
        'd3': 3,    # Tercer dígito
        'd8': 8     # Octavo dígito
    }
    
    print(f"\nDatos del RUT: d3={datos_rut['d3']}, d8={datos_rut['d8']}")
    print(f"Residuo: {datos_rut['d8']} % 3 = {datos_rut['d8'] % 3}\n")
    
    # PASO 1: Generar la función
    print("┌─ PASO 1: GENERAR FUNCIÓN ─────────────────────┐")
    funcion_info = generar_funcion_por_tramos(datos_rut)
    
    print(f"\nTipo de discontinuidad: {funcion_info['tipo_discontinuidad']}")
    print(f"Punto crítico (a): {funcion_info['punto_critico']}")
    print(f"Regla usada: {funcion_info['regla_usada']}")
    print(funcion_info['descripcion'])
    
    # PASO 2: Generar tabla de valores cercanos
    print("┌─ PASO 2: GENERAR TABLA DE PUNTOS CERCANOS ────┐")
    puntos_info = generar_puntos_cercanos(funcion_info['punto_critico'])
    
    print(f"\nPuntos por izquierda: {puntos_info['puntos_izquierda']}")
    print(f"Puntos por derecha: {puntos_info['puntos_derecha']}")
    print(f"\nTabla de estructura:")
    print(f"{'Posición':<20} {'x':<10} {'Distancia a a':<15}")
    print("-" * 45)
    for punto in puntos_info['tabla']:
        print(f"{punto['posicion']:<20} {punto['x']:<10.3f} {punto['distancia_a_a']:<15}")
    
    # PASO 3: Generar procedimiento completo
    print("\n┌─ PASO 3: GENERAR PROCEDIMIENTO ──────────────────┐")
    procedimiento = generar_procedimiento_funcion(datos_rut, funcion_info)
    print(procedimiento)
    
    # PASO 4: Generar tabla resumen
    print("┌─ PASO 4: TABLA RESUMEN ──────────────────────────┐")
    tabla_resumen = generar_tabla_procedimiento(datos_rut, funcion_info, puntos_info)
    print(tabla_resumen)


def ejemplo_con_evaluacion():
    """Ejemplo con evaluación de función en puntos específicos."""
    
    from src.funciones_tramos import evaluar_en_tabla
    
    print("\n" + "=" * 80)
    print("EJEMPLO CON EVALUACIÓN DE FUNCIÓN")
    print("=" * 80)
    
    # Datos del RUT
    datos_rut = {
        'd3': 2,
        'd8': 5
    }
    
    print(f"\nDatos del RUT: d3={datos_rut['d3']}, d8={datos_rut['d8']}")
    
    # Generar función
    funcion_info = generar_funcion_por_tramos(datos_rut)
    print(f"Tipo de discontinuidad: {funcion_info['tipo_discontinuidad']}")
    
    # Generar puntos
    a = funcion_info['punto_critico']
    puntos_info = generar_puntos_cercanos(a)
    
    # Definir una función evaluadora según el tipo
    residuo = datos_rut['d8'] % 3
    
    if residuo == 0:
        # Discontinuidad removible: f(x) = x² + 1
        def f(x):
            if x == a:
                return None  # No definida en a
            return x**2 + 1
    
    elif residuo == 1:
        # Discontinuidad de salto
        def f(x):
            if x <= a:
                return 2*x + 1
            else:
                return x + 5
    
    else:  # residuo == 2
        # Discontinuidad infinita
        def f(x):
            if x == a:
                return None
            return 1 / (x - a)
    
    # Evaluar en tabla
    tabla_evaluada = evaluar_en_tabla(puntos_info, f)
    
    # Mostrar tabla
    print(f"\nTabla de valores con evaluación f(x):")
    print(f"{'x':<12} {'Posición':<20} {'f(x)':<15} {'Obs.':<20}")
    print("-" * 67)
    
    for punto in tabla_evaluada:
        x = punto['x']
        posicion = punto['posicion']
        fx = punto.get('f(x)', 'N/A')
        error = punto.get('error', '')
        
        if fx is not None:
            fx_str = f"{fx:.4f}"
        else:
            fx_str = "NO DEF."
        
        obs = "Salto" if punto['tipo'] == 'critico' else ""
        
        print(f"{x:<12.4f} {posicion:<20} {fx_str:<15} {obs:<20}")


if __name__ == "__main__":
    try:
        # Ejecutar ejemplo básico
        ejemplo_basico()
        
        # Ejecutar ejemplo con evaluación
        ejemplo_con_evaluacion()
        
        print("\n" + "=" * 80)
        print("✓ Ejemplos ejecutados exitosamente")
        print("=" * 80)
    
    except Exception as e:
        print(f"\n✗ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
