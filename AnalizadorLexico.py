from AFN_File.AFD import AFD
from Constantes import SimbEspecial
from EdoAnalizador import EdoAnalizador


class AnalizadorLexico:
    def __init__(self, sigma='', archivo_afd=None):
        self.token = -1
        self.EdoActual = 0
        self.EdoTransicion = -1
        self.CadenaSigma = sigma
        self.Lexema = ""
        self.PasoPorEdoAcept = False
        self.IniLexema = 0
        self.FinLexema = -1
        self.IndiceCaracterActual = 0
        self.CaracterActual = ''
        self.Pila = []
        self.AutomataAFD = None

        # Si se proporciona un archivo, carga el AFD
        if archivo_afd:
            self.AutomataAFD = AFD()
            self.AutomataAFD.leer_AFD_archivo(archivo_afd)

    def set_estado_analizador(self, estado_analizador):
        self.CaracterActual = estado_analizador.CaracterActual
        self.EdoActual = estado_analizador.EdoActual
        self.EdoTransicion = estado_analizador.EdoTransicion
        self.FinLexema = estado_analizador.FinLexema
        self.IndiceCaracterActual = estado_analizador.IndiceCaracterActual
        self.IniLexema = estado_analizador.IniLexema
        self.Lexema = estado_analizador.Lexema
        self.PasoPorEdoAcept = estado_analizador.PasoPorEdoAcept
        self.token = estado_analizador.token
        self.Pila = estado_analizador.Pila.copy()
        return True

    def GetEdoAnalizador(self):
        """
        Captura el estado actual del analizador y lo devuelve como una instancia de EdoAnalizador.
        """
        return EdoAnalizador(
            self.CaracterActual,
            self.EdoActual,
            self.EdoTransicion,
            self.FinLexema,
            self.IndiceCaracterActual,
            self.IniLexema,
            self.Lexema,
            self.PasoPorEdoAcept,
            self.token,
            self.Pila
        )

    def set_sigma(self, sigma):
        """
        Reinicia el analizador para analizar una nueva cadena de entrada.
        """
        self.CadenaSigma = sigma
        self.PasoPorEdoAcept = False
        self.IniLexema = 0
        self.FinLexema = -1
        self.IndiceCaracterActual = 0
        self.token = -1
        self.Pila.clear()

    def cadena_por_analizar(self):
        """
        Retorna la porción de la cadena que falta por analizar.
        """
        return self.CadenaSigma[self.IndiceCaracterActual:]

    def yylex(self):
        """
        Realiza el análisis léxico, regresando el token identificado o un error.
        """
        while True:
            # Guardar el índice inicial del análisis
            self.Pila.append(self.IndiceCaracterActual)

            # Si el índice supera la longitud de la cadena, termina
            if self.IndiceCaracterActual >= len(self.CadenaSigma):
                self.Lexema = ""
                return 0  # Fin de la cadena de entrada

            # Inicializar el análisis de un nuevo lexema
            self.IniLexema = self.IndiceCaracterActual
            self.EdoActual = 0
            self.PasoPorEdoAcept = False
            self.FinLexema = -1
            self.token = -1

            while self.IndiceCaracterActual < len(self.CadenaSigma):
                # Leer el carácter actual y buscar la transición
                self.CaracterActual = self.CadenaSigma[self.IndiceCaracterActual]
                ascii_val = ord(self.CaracterActual)

                # Obtener la transición en la tabla del AFD
                self.EdoTransicion = self.AutomataAFD.tabla_transiciones[self.EdoActual][ascii_val + 1]

                # Si hay una transición válida
                if self.EdoTransicion != -1:
                    self.EdoActual = self.EdoTransicion
                    self.IndiceCaracterActual += 1

                    # Si el estado actual es de aceptación, registrar el token
                    if self.AutomataAFD.tabla_transiciones[self.EdoActual][-1] != -1:
                        self.PasoPorEdoAcept = True
                        self.token = self.AutomataAFD.tabla_transiciones[self.EdoActual][-1]
                        self.FinLexema = self.IndiceCaracterActual - 1
                    continue

                # Romper si no hay transición válida
                break

            # Si el último estado no fue de aceptación
            if not self.PasoPorEdoAcept:
                self.IndiceCaracterActual = self.IniLexema + 1
                self.Lexema = self.CadenaSigma[self.IniLexema:self.IniLexema + 1]
                self.token = SimbEspecial.ERROR
                return self.token

            # Extraer el lexema válido
            self.Lexema = self.CadenaSigma[self.IniLexema:self.FinLexema + 1]
            self.IndiceCaracterActual = self.FinLexema + 1

            # Si el token es OMITIR, reiniciar el análisis de un nuevo lexema
            if self.token == SimbEspecial.OMITIR:
                continue
            else:
                return self.token

    def undo_token(self):
        """
        Regresa el índice de análisis al estado anterior.
        """
        if not self.Pila:
            return False
        self.IndiceCaracterActual = self.Pila.pop()
        return True
