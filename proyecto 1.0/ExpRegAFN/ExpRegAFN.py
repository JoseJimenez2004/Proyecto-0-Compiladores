from AFN_File.AFN import AFN
from AnalizadorLexico.AnalizadorLexico import AnalizadorLexico

class ExpRegAFN:
    def __init__(self, sigma: str, file_afd: str, id = None):
        self.id = id
        self.expr_regular = sigma
        self.result = None
        self.l = AnalizadorLexico(sigma, file_afd)

    def set_expresion(self, sigma: str):
        self.expr_regular = sigma
        self.l.set_sigma(sigma)

    def ini_conversion(self) -> bool:
        f = AFN()
        if self.e(f):
            token1 = self.l.yylex()
            if token1 == 0:
                self.result = f
                self.result.mostrar_afn()
                return True
        return False

    def e(self, f: AFN) -> bool:
        if self.t(f):
            if self.ep(f):
                return True
        return False

    def ep(self, f: AFN) -> bool:
        token = self.l.yylex()
        f2 = AFN()
        if token == 10:  # OR
            if self.t(f2):
                f.unir(f2)
                if self.ep(f):
                    return True
            return False
        self.l.undo_token()
        return True

    def t(self, f: AFN) -> bool:
        if self.c(f):
            if self.tp(f):
                return True
        return False

    def tp(self, f: AFN) -> bool:
        token = self.l.yylex()
        f2 = AFN()
        if token == 20:  # Concatenación (&)
            if self.c(f2):
                f.concatenar(f2)  # Combina usando concatenación
                if self.tp(f):
                    return True
            return False
        self.l.undo_token()  # Regresar el token si no es concatenación
        return True

    def c(self, f: AFN) -> bool:
        if self.f(f):
            if self.cp(f):
                return True
        return False

    def cp(self, f: AFN) -> bool:
        token = self.l.yylex()
        if token == 30:  # Cerradura Positiva
            f.cerradura()
            if self.cp(f):
                return True
            return False
        elif token == 40:  # Cerradura Kleene
            f.cierre_kleene()
            if self.cp(f):
                return True
            return False
        elif token == 50:  # Opcional
            f.opcional()
            if self.cp(f):
                return True
            return False
        self.l.undo_token()
        return True

    def f(self, f: AFN) -> bool:
        token = self.l.yylex()
        simbolo1 = simbolo2 = None

        if token == 60:  # Paréntesis izquierdo
            # Resolver completamente el contenido del paréntesis
            f_temp = AFN()
            if self.e(f_temp):  # Resuelve la subexpresión dentro del paréntesis
                token = self.l.yylex()
                if token == 70:  # Paréntesis derecho
                    f.edo_inicial = f_temp.edo_inicial
                    f.edos_afn = f_temp.edos_afn
                    f.edos_acept = f_temp.edos_acept
                    f.alfabeto = f_temp.alfabeto
                    return True
            return False

        elif token == 80:  # Corchete izquierdo
            # Crear AFN para un rango de caracteres [a-z]
            token = self.l.yylex()
            if token == 110:  # Símbolo
                simbolo1 = self._procesar_simbolo(self.l.Lexema)
                token = self.l.yylex()
                if token == 100:  # Guion
                    token = self.l.yylex()
                    if token == 110:  # Símbolo
                        simbolo2 = self._procesar_simbolo(self.l.Lexema)
                        token = self.l.yylex()
                        if token == 90:  # Corchete derecho
                            if simbolo1 > simbolo2:  # Rango inválido
                                return False
                            f.afn_basico([simbolo1, simbolo2], token=self.id)
                            return True
            return False

        elif token == 110:  # Símbolo
            # Crear AFN para un único símbolo
            simbolo1 = self._procesar_simbolo(self.l.Lexema)
            f.afn_basico(simbolo1, token=self.id)
            return True

        return False

    def _procesar_simbolo(self, lexema: str) -> str:
        """Procesa el símbolo escapado si es necesario."""
        return lexema[1] if lexema.startswith('\\') else lexema[0]


regex = "([a-z]|[A-Z])"
afn_converter = ExpRegAFN(sigma=regex, file_afd="ExpReg.csv", id=10)
if afn_converter.ini_conversion():
    print("Hola")

