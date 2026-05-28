def formatear_num(n):
    """
    Muestra un número como entero si no tiene decimales,
    o como decimal con 4 cifras si las tiene.

    Ejemplos:
        3.0  → "3"
        3.5  → "3.5"
        3.14159 → "3.1416"
    """
    if n == int(n):
        return str(int(n))
    return str(round(n, 4))


def formatear_termino_x(h):
    """
    Formatea el término (x - h) correctamente según el signo de h.

    Ejemplos:
        h =  3  → "(x - 3)"
        h = -3  → "(x + 3)"
        h =  0  → "x"
    """
    if h == 0:
        return "x"
    elif h > 0:
        return f"(x - {formatear_num(h)})"
    else:
        return f"(x + {formatear_num(abs(h))})"


def formatear_termino_y(k):
    """
    Formatea el término (y - k) correctamente según el signo de k.

    Ejemplos:
        k =  3  → "(y - 3)"
        k = -3  → "(y + 3)"
        k =  0  → "y"
    """
    if k == 0:
        return "y"
    elif k > 0:
        return f"(y - {formatear_num(k)})"
    else:
        return f"(y + {formatear_num(abs(k))})"


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def transformar_a_canonica(coeficientes, tipo_conica):
    """
    Transforma la ecuación general de una cónica a su forma canónica.

    La ecuación general es: Ax² + By² + Cx + Dy + E = 0

    Parámetros:
        coeficientes: tupla (A, B, C, D, E)
        tipo_conica:  string con el tipo ("Circunferencia", "Elipse", etc.)

    Retorna:
        diccionario con:
            forma_canonica : string con la ecuación canónica final
            pasos          : string con el procedimiento paso a paso
    """

    A, B, C, D, E = coeficientes

    if tipo_conica == "Circunferencia":
        return _canonica_circunferencia(A, C, D, E)

    elif tipo_conica == "Elipse":
        return _canonica_elipse(A, B, C, D, E)

    elif tipo_conica == "Hiperbola":
        return _canonica_hiperbola(A, B, C, D, E)

    elif tipo_conica == "Parabola":
        return _canonica_parabola(A, B, C, D, E)

    else:
        return {
            "forma_canonica": "Tipo de cónica no implementado aún.",
            "pasos": ""
        }


# =============================================================================
# CIRCUNFERENCIA
# =============================================================================

def _canonica_circunferencia(A, C, D, E):
    """
    Transforma Ax² + Ay² + Cx + Dy + E = 0 a la forma canónica:
        (x - h)² + (y - k)² = r²

    Fórmulas:
        h  = -C / (2A)
        k  = -D / (2A)
        r² = h² + k² - E/A
    """

    pasos = []

    pasos.append("=== Transformación a forma canónica: Circunferencia ===")
    pasos.append("")
    pasos.append("Ecuación general:")
    pasos.append(f"  {formatear_num(A)}x² + {formatear_num(A)}y² + {formatear_num(C)}x + {formatear_num(D)}y + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 1: Agrupar términos en x y en y
    # ------------------------------------------------------------------
    pasos.append("Paso 1: Agrupar términos en x e y")
    pasos.append(f"  ({formatear_num(A)}x² + {formatear_num(C)}x) + ({formatear_num(A)}y² + {formatear_num(D)}y) + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 2: Factorizar A en cada grupo
    # ------------------------------------------------------------------
    C_sobre_A = C / A
    D_sobre_A = D / A

    pasos.append("Paso 2: Factorizar el coeficiente A de cada grupo")
    pasos.append(f"  {formatear_num(A)}(x² + {formatear_num(C_sobre_A)}x) + {formatear_num(A)}(y² + {formatear_num(D_sobre_A)}y) + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 3: Completar el cuadrado en x
    # x² + (C/A)x → (x + C/(2A))² - (C/(2A))²
    # ------------------------------------------------------------------
    mitad_x = C / (2 * A)          # C / (2A)
    mitad_x_cuad = mitad_x ** 2    # (C / (2A))²

    pasos.append("Paso 3: Completar el cuadrado en x")
    pasos.append(f"  Se toma la mitad del coeficiente de x: {formatear_num(C_sobre_A)} / 2 = {formatear_num(mitad_x)}")
    pasos.append(f"  Se eleva al cuadrado: {formatear_num(mitad_x)}² = {formatear_num(mitad_x_cuad)}")
    pasos.append(f"  x² + {formatear_num(C_sobre_A)}x = (x + {formatear_num(mitad_x)})² - {formatear_num(mitad_x_cuad)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 4: Completar el cuadrado en y
    # y² + (D/A)y → (y + D/(2A))² - (D/(2A))²
    # ------------------------------------------------------------------
    mitad_y = D / (2 * A)
    mitad_y_cuad = mitad_y ** 2

    pasos.append("Paso 4: Completar el cuadrado en y")
    pasos.append(f"  Se toma la mitad del coeficiente de y: {formatear_num(D_sobre_A)} / 2 = {formatear_num(mitad_y)}")
    pasos.append(f"  Se eleva al cuadrado: {formatear_num(mitad_y)}² = {formatear_num(mitad_y_cuad)}")
    pasos.append(f"  y² + {formatear_num(D_sobre_A)}y = (y + {formatear_num(mitad_y)})² - {formatear_num(mitad_y_cuad)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 5: Sustituir en la ecuación
    # ------------------------------------------------------------------
    pasos.append("Paso 5: Sustituir los cuadrados completados en la ecuación")
    pasos.append(f"  {formatear_num(A)}[(x + {formatear_num(mitad_x)})² - {formatear_num(mitad_x_cuad)}]")
    pasos.append(f"  + {formatear_num(A)}[(y + {formatear_num(mitad_y)})² - {formatear_num(mitad_y_cuad)}]")
    pasos.append(f"  + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 6: Distribuir A y expandir constantes
    # ------------------------------------------------------------------
    constante_x = A * mitad_x_cuad    # A * (C/(2A))² = C² / (4A)
    constante_y = A * mitad_y_cuad    # A * (D/(2A))² = D² / (4A)

    pasos.append("Paso 6: Distribuir A y separar las constantes")
    pasos.append(f"  {formatear_num(A)}(x + {formatear_num(mitad_x)})² - {formatear_num(constante_x)}")
    pasos.append(f"  + {formatear_num(A)}(y + {formatear_num(mitad_y)})² - {formatear_num(constante_y)}")
    pasos.append(f"  + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 7: Pasar constantes al lado derecho
    # ------------------------------------------------------------------
    lado_derecho = constante_x + constante_y - E

    pasos.append("Paso 7: Pasar las constantes al lado derecho")
    pasos.append(f"  {formatear_num(A)}(x + {formatear_num(mitad_x)})² + {formatear_num(A)}(y + {formatear_num(mitad_y)})²")
    pasos.append(f"  = {formatear_num(constante_x)} + {formatear_num(constante_y)} - {formatear_num(E)}")
    pasos.append(f"  = {formatear_num(lado_derecho)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 8: Dividir por A
    # ------------------------------------------------------------------
    r2 = lado_derecho / A

    pasos.append("Paso 8: Dividir toda la ecuación por A")
    pasos.append(f"  (x + {formatear_num(mitad_x)})² + (y + {formatear_num(mitad_y)})² = {formatear_num(lado_derecho)} / {formatear_num(A)}")
    pasos.append(f"  (x + {formatear_num(mitad_x)})² + (y + {formatear_num(mitad_y)})² = {formatear_num(r2)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Resultado final
    # ------------------------------------------------------------------
    h = -mitad_x    # Centro en x
    k = -mitad_y    # Centro en y
    r = r2 ** 0.5   # Radio

    termino_x = formatear_termino_x(h)
    termino_y = formatear_termino_y(k)

    forma_canonica = f"{termino_x}² + {termino_y}² = {formatear_num(r2)}"

    pasos.append("Forma canónica final:")
    pasos.append(f"  {forma_canonica}")
    pasos.append("")
    pasos.append(f"  Centro : ({formatear_num(h)}, {formatear_num(k)})")
    pasos.append(f"  Radio² : {formatear_num(r2)}")
    pasos.append(f"  Radio  : {formatear_num(r)}")

    return {
        "forma_canonica": forma_canonica,
        "centro": (h, k),
        "radio_cuadrado": r2,
        "radio": r,
        "pasos": "\n".join(pasos)
    }


# =============================================================================
# ELIPSE
# =============================================================================

def _canonica_elipse(A, B, C, D, E):
    """
    Transforma Ax² + By² + Cx + Dy + E = 0 a la forma canónica:
        (x - h)²/a² + (y - k)²/b² = 1

    Fórmulas:
        h  = -C / (2A)
        k  = -D / (2B)
        K  = C²/(4A) + D²/(4B) - E      (constante del lado derecho)
        a² = K / A
        b² = K / B
    """

    pasos = []

    pasos.append("=== Transformación a forma canónica: Elipse ===")
    pasos.append("")
    pasos.append("Ecuación general:")
    pasos.append(f"  {formatear_num(A)}x² + {formatear_num(B)}y² + {formatear_num(C)}x + {formatear_num(D)}y + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 1: Agrupar términos en x y en y
    # ------------------------------------------------------------------
    pasos.append("Paso 1: Agrupar términos en x e y")
    pasos.append(f"  ({formatear_num(A)}x² + {formatear_num(C)}x) + ({formatear_num(B)}y² + {formatear_num(D)}y) + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 2: Factorizar A del grupo en x y B del grupo en y
    # ------------------------------------------------------------------
    C_sobre_A = C / A
    D_sobre_B = D / B

    pasos.append("Paso 2: Factorizar A del grupo en x, y B del grupo en y")
    pasos.append(f"  {formatear_num(A)}(x² + {formatear_num(C_sobre_A)}x) + {formatear_num(B)}(y² + {formatear_num(D_sobre_B)}y) + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 3: Completar el cuadrado en x
    # ------------------------------------------------------------------
    mitad_x = C / (2 * A)
    mitad_x_cuad = mitad_x ** 2

    pasos.append("Paso 3: Completar el cuadrado en x")
    pasos.append(f"  Se toma la mitad del coeficiente de x: {formatear_num(C_sobre_A)} / 2 = {formatear_num(mitad_x)}")
    pasos.append(f"  Se eleva al cuadrado: {formatear_num(mitad_x)}² = {formatear_num(mitad_x_cuad)}")
    pasos.append(f"  x² + {formatear_num(C_sobre_A)}x = (x + {formatear_num(mitad_x)})² - {formatear_num(mitad_x_cuad)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 4: Completar el cuadrado en y
    # ------------------------------------------------------------------
    mitad_y = D / (2 * B)
    mitad_y_cuad = mitad_y ** 2

    pasos.append("Paso 4: Completar el cuadrado en y")
    pasos.append(f"  Se toma la mitad del coeficiente de y: {formatear_num(D_sobre_B)} / 2 = {formatear_num(mitad_y)}")
    pasos.append(f"  Se eleva al cuadrado: {formatear_num(mitad_y)}² = {formatear_num(mitad_y_cuad)}")
    pasos.append(f"  y² + {formatear_num(D_sobre_B)}y = (y + {formatear_num(mitad_y)})² - {formatear_num(mitad_y_cuad)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 5: Sustituir en la ecuación
    # ------------------------------------------------------------------
    pasos.append("Paso 5: Sustituir los cuadrados completados en la ecuación")
    pasos.append(f"  {formatear_num(A)}[(x + {formatear_num(mitad_x)})² - {formatear_num(mitad_x_cuad)}]")
    pasos.append(f"  + {formatear_num(B)}[(y + {formatear_num(mitad_y)})² - {formatear_num(mitad_y_cuad)}]")
    pasos.append(f"  + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 6: Distribuir y separar constantes
    # A * mitad_x_cuad = A * (C/(2A))² = C²/(4A)
    # B * mitad_y_cuad = B * (D/(2B))² = D²/(4B)
    # ------------------------------------------------------------------
    constante_x = A * mitad_x_cuad
    constante_y = B * mitad_y_cuad

    pasos.append("Paso 6: Distribuir A y B, y separar las constantes")
    pasos.append(f"  {formatear_num(A)}(x + {formatear_num(mitad_x)})² - {formatear_num(constante_x)}")
    pasos.append(f"  + {formatear_num(B)}(y + {formatear_num(mitad_y)})² - {formatear_num(constante_y)}")
    pasos.append(f"  + {formatear_num(E)} = 0")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 7: Pasar constantes al lado derecho
    # K = C²/(4A) + D²/(4B) - E
    # ------------------------------------------------------------------
    K = constante_x + constante_y - E

    pasos.append("Paso 7: Pasar las constantes al lado derecho")
    pasos.append(f"  {formatear_num(A)}(x + {formatear_num(mitad_x)})² + {formatear_num(B)}(y + {formatear_num(mitad_y)})²")
    pasos.append(f"  = {formatear_num(constante_x)} + {formatear_num(constante_y)} - {formatear_num(E)}")
    pasos.append(f"  = {formatear_num(K)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Paso 8: Dividir por K para obtener la forma = 1
    # ------------------------------------------------------------------
    a2 = K / A    # a² = K/A
    b2 = K / B    # b² = K/B

    pasos.append("Paso 8: Dividir toda la ecuación por K para llegar a la forma = 1")
    pasos.append(f"  {formatear_num(A)}(x + {formatear_num(mitad_x)})² / {formatear_num(K)}")
    pasos.append(f"  + {formatear_num(B)}(y + {formatear_num(mitad_y)})² / {formatear_num(K)} = 1")
    pasos.append("")
    pasos.append(f"  (x + {formatear_num(mitad_x)})² / ({formatear_num(K)}/{formatear_num(A)})")
    pasos.append(f"  + (y + {formatear_num(mitad_y)})² / ({formatear_num(K)}/{formatear_num(B)}) = 1")
    pasos.append("")
    pasos.append(f"  a² = {formatear_num(K)} / {formatear_num(A)} = {formatear_num(a2)}")
    pasos.append(f"  b² = {formatear_num(K)} / {formatear_num(B)} = {formatear_num(b2)}")
    pasos.append("")

    # ------------------------------------------------------------------
    # Resultado final
    # ------------------------------------------------------------------
    h = -mitad_x
    k = -mitad_y

    termino_x = formatear_termino_x(h)
    termino_y = formatear_termino_y(k)

    forma_canonica = f"{termino_x}² / {formatear_num(a2)} + {termino_y}² / {formatear_num(b2)} = 1"

    pasos.append("Forma canónica final:")
    pasos.append(f"  {forma_canonica}")
    pasos.append("")
    pasos.append(f"  Centro : ({formatear_num(h)}, {formatear_num(k)})")
    pasos.append(f"  a²     : {formatear_num(a2)}")
    pasos.append(f"  b²     : {formatear_num(b2)}")

    return {
        "forma_canonica": forma_canonica,
        "centro": (h, k),
        "a_cuadrado": a2,
        "b_cuadrado": b2,
        "pasos": "\n".join(pasos)
    }
