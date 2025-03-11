#Puedes ingresar un carácter alfabético como "a", "b", "c", etc.

#O puedes ingresar un símbolo especial, como "#", "*", "1", "@", etc.
#Letras: Son los más comunes en AFNs. Ejemplos: a, b, c, etc.
#Números: Puedes usar números como símbolos. Ejemplo: 1, 2, 3.
#Símbolos especiales: Puedes usar caracteres como #, *, &, @ si lo necesitas.

class AFN:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.estado_inicial = 0
        self.estado_final = 1
        self.transiciones = [(0, simbolo, 1)]  # transición: (estado_inicial, símbolo, estado_final)

    def mostrar(self):
        print(f"AFN con símbolo: {self.simbolo}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estado final: {self.estado_final}")
        print(f"Transiciones: {self.transiciones}")

def crear_afn_basico(simbolo):
    return AFN(simbolo)
