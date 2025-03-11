class AFN:
    def __init__(self, estados, transiciones, estado_inicial, estado_final):
        self.estados = estados
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

    def mostrar(self):
        print("Estados:", self.estados)
        print("Transiciones:", self.transiciones)
        print("Estado Inicial:", self.estado_inicial)
        print("Estado Final:", self.estado_final)

# Función para crear un AFN básico (de un solo símbolo)
def crear_afn_basico(simbolo):
    estado_inicial = 0
    estado_final = 1
    estados = [estado_inicial, estado_final]
    transiciones = [(estado_inicial, simbolo, estado_final)]
    return AFN(estados, transiciones, estado_inicial, estado_final)
