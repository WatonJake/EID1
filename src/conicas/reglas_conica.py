def aplicar_reglas_especiales(A , B , digitos):
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    
    # si d8 es impar entonces B =-B 
    if d8 % 2 != 0:
        B = -B
    
    
    #si d1 = d2, entonces B = A
    if d1 == d2:
        B = A
    
    
    # si d5 + d6 es multiplo de 3
    if (d5 + d6)% 3 == 0:
        #si d7 es par → B = 0
        if d7 % 2 == 0 :
            B = 0
        #si d7 es impar → A = 0
        else: 
            A = 0
    
    return A , B