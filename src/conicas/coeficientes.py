def calcular_coeficientes(digitos , v):
    d1 , d2, d3, d4, d5, d6, d7, d8 = digitos
    
    
    A= (d1+d2) / v
    B= (d3+d4) / v
    C= (d5+d6) / v
    D= (d7+d8) / v
    E= d1+d3+d5+d7
    
    return A, B, C, D, E
