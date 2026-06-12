PI = 3.141592653589793


def valor_absoluto(numero):
    return -numero if numero < 0 else numero


def factorial(numero):
    resultado = 1
    for valor in range(2, numero + 1):
        resultado *= valor
    return resultado


def potencia(base, exponente):
    if exponente == 0:
        return 1.0

    if exponente < 0:
        return 1.0 / potencia(base, -exponente)

    resultado = 1.0
    for _ in range(exponente):
        resultado *= base
    return resultado


def raiz_cuadrada(numero, tolerancia=1e-10, max_iteraciones=100):
    if numero < 0:
        raise ValueError("No existe raíz cuadrada real para números negativos.")

    if numero == 0:
        return 0.0

    aproximacion = numero if numero >= 1 else 1.0
    for _ in range(max_iteraciones):
        nueva = 0.5 * (aproximacion + (numero / aproximacion))
        if valor_absoluto(nueva - aproximacion) < tolerancia:
            return nueva
        aproximacion = nueva
    return aproximacion


def reducir_angulo(angulo):
    dos_pi = 2 * PI
    while angulo > PI:
        angulo -= dos_pi
    while angulo < -PI:
        angulo += dos_pi
    return angulo


def seno(angulo, terminos=10):
    angulo = reducir_angulo(angulo)
    acumulado = 0.0
    for indice in range(terminos):
        exponente = (2 * indice) + 1
        signo = -1.0 if indice % 2 else 1.0
        acumulado += signo * (potencia(angulo, exponente) / factorial(exponente))
    return acumulado


def coseno(angulo, terminos=10):
    angulo = reducir_angulo(angulo)
    acumulado = 0.0
    for indice in range(terminos):
        exponente = 2 * indice
        signo = -1.0 if indice % 2 else 1.0
        acumulado += signo * (potencia(angulo, exponente) / factorial(exponente))
    return acumulado


def seno_hiperbolico(valor, terminos=12):
    acumulado = 0.0
    for indice in range(terminos):
        exponente = (2 * indice) + 1
        acumulado += potencia(valor, exponente) / factorial(exponente)
    return acumulado


def coseno_hiperbolico(valor, terminos=12):
    acumulado = 0.0
    for indice in range(terminos):
        exponente = 2 * indice
        acumulado += potencia(valor, exponente) / factorial(exponente)
    return acumulado
