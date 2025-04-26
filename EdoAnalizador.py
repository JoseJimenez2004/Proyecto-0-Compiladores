class EdoAnalizador:
    def __init__(self, caracter_actual, edo_actual, edo_transicion, fin_lexema, indice_caracter_actual, ini_lexema, lexema, paso_por_edo_acept, token, pila):
        self.CaracterActual = caracter_actual
        self.EdoActual = edo_actual
        self.EdoTransicion = edo_transicion
        self.FinLexema = fin_lexema
        self.IndiceCaracterActual = indice_caracter_actual
        self.IniLexema = ini_lexema
        self.Lexema = lexema
        self.PasoPorEdoAcept = paso_por_edo_acept
        self.token = token
        self.Pila = pila.copy()
