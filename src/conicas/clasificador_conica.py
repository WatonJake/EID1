def clasificar_conica (A , B):
    
    if A == B and A != 0 : 
        return "Circunferencia"
    
    elif (A * B > 0 ) and (A != B):
        return "Elipse"
    
    elif (A * B < 0) :
        return "Hiperbola"
    
    elif ( A == 0 and B!= 0) or (A!= 0 and B== 0 ):
        return "Parabola"
    
    else :
        return "Indeterminada"