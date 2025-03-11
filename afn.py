class AFN:
    def __init__(self):
        self.estados = set()  # Conjunto de estados
        self.alphabet = set()  # Alfabeto
        self.transiciones = {}  # Transiciones
        self.inicial = None  # Estado inicial
        self.finales = set()  # Estados finales
        self.estado_contador = 0  # Contador para generar nuevos estados

    def agregar_estado(self, final=False):
        estado = self.estado_contador
        self.estado_contador += 1
        self.estados.add(estado)
        if final:
            self.finales.add(estado)
        return estado

    def agregar_transicion(self, desde, simbolo, hasta):
        if (desde, simbolo) not in self.transiciones:
            self.transiciones[(desde, simbolo)] = set()
        self.transiciones[(desde, simbolo)].add(hasta)

    def mostrar(self):
        print("Estados:", self.estados)
        print("Alfabeto:", self.alphabet)
        print("Transiciones:")
        for (desde, simbolo), hasta in self.transiciones.items():
            print(f"  {desde} --{simbolo}--> {hasta}")
        print("Estado inicial:", self.inicial)
        print("Estados finales:", self.finales)
