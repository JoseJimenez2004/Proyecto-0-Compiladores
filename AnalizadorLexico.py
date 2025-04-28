from AFN_File.AFD import AFD
from Constantes import SimbEspecial
from EdoAnalizador import EdoAnalizador
from Constantes.SimbEspecial import SimbEspecial
from Constantes import Tokenizador as Tokenizador

# Diccionario para convertir caracteres a índices
CARACTERES = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
    'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
    'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
    'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25
}

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
        self.CadenaSigma = sigma
        self.PasoPorEdoAcept = False
        self.IniLexema = 0
        self.FinLexema = -1
        self.IndiceCaracterActual = 0
        self.token = -1
        self.Pila.clear()

    def cadena_por_analizar(self):
        return self.CadenaSigma[self.IndiceCaracterActual:]

    def yylex(self):
        while True:
            self.Pila.append(self.IndiceCaracterActual)

            if self.IndiceCaracterActual >= len(self.CadenaSigma):
                self.Lexema = ""
                return 0  # Fin de la cadena de entrada

            self.IniLexema = self.IndiceCaracterActual
            self.EdoActual = 0
            self.PasoPorEdoAcept = False
            self.FinLexema = -1
            self.token = -1

            while self.IndiceCaracterActual < len(self.CadenaSigma):
                self.CaracterActual = self.CadenaSigma[self.IndiceCaracterActual]
                ascii_val = ord(self.CaracterActual)

                # Verificar si el carácter es un símbolo válido
                if 0 <= ascii_val < len(self.AutomataAFD.tabla_transiciones[self.EdoActual]):
                    # Si es un carácter mapeado, obtener la transición
                    if self.CaracterActual in CARACTERES:
                        ascii_val = CARACTERES[self.CaracterActual]
                    self.EdoTransicion = self.AutomataAFD.tabla_transiciones[self.EdoActual][ascii_val]

                    if self.EdoTransicion != -1:
                        self.EdoActual = self.EdoTransicion
                        self.IndiceCaracterActual += 1

                        if self.AutomataAFD.tabla_transiciones[self.EdoActual][-1] != -1:
                            self.PasoPorEdoAcept = True
                            self.token = self.AutomataAFD.tabla_transiciones[self.EdoActual][-1]
                            self.FinLexema = self.IndiceCaracterActual - 1
                        continue

                break

            if not self.PasoPorEdoAcept:
                self.IndiceCaracterActual = self.IniLexema + 1
                self.Lexema = self.CadenaSigma[self.IniLexema:self.IniLexema + 1]
                self.token = SimbEspecial.ERROR
                return self.token

            self.Lexema = self.CadenaSigma[self.IniLexema:self.FinLexema + 1]
            self.IndiceCaracterActual = self.FinLexema + 1

            if self.token == SimbEspecial.OMITIR:
                continue
            else:
                return self.token

    def undo_token(self):
        if not self.Pila:
            return False
        self.IndiceCaracterActual = self.Pila.pop()
        return True

    def pedir_cadena(self):
        self.CadenaSigma = input("Introduce una cadena para analizar: ")
        self.set_sigma(self.CadenaSigma)


class AFD:
    def __init__(self):
        self.tabla_transiciones = []

    def leer_AFD_archivo(self, archivo_afd):
        with open(archivo_afd, 'r') as archivo:
            lineas = archivo.readlines()

        for i, linea in enumerate(lineas):
            linea = linea.strip()

            if not linea:
                continue

            if "->" in linea:
                transicion, estado_destino = linea.split("->")
                estado_destino = int(estado_destino.strip())
                transicion = transicion.strip().split(",")
                transiciones = []
                for item in transicion:
                    if "-" in item:
                        inicio, fin = map(int, item.split("-"))
                        transiciones.extend(range(inicio, fin + 1))
                    elif item in CARACTERES:
                        transiciones.append(CARACTERES[item])
                    else:
                        transiciones.append(int(item))  # Agregar los valores numéricos

                self.tabla_transiciones.append((transiciones, estado_destino))

            else:
                transiciones = list(map(int, linea.split(",")))
                self.tabla_transiciones.append(transiciones)

        print(f"Tabla de transiciones cargada: {self.tabla_transiciones}")


if __name__ == "__main__":
    analizador = AnalizadorLexico(archivo_afd="AFN_File/mi_afd_guardado.afd")
    analizador.pedir_cadena()

    while True:
        token = analizador.yylex()
        if token == 0:
            print("Análisis completado.")
            break
        else:
            print(f"Token: {token}, Lexema: {analizador.Lexema}")
