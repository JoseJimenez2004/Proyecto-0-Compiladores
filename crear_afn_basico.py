import os

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

    def guardar_en_archivo(self, nombre_archivo):
        # Verifica si la carpeta 'autbasic' existe, si no la crea
        if not os.path.exists('autbasic'):
            os.makedirs('autbasic')

        # Abre el archivo en modo escritura
        with open(f'autbasic/{nombre_archivo}.txt', 'w') as archivo:
            archivo.write(f"AFN con símbolo: {self.simbolo}\n")
            archivo.write(f"Estado inicial: {self.estado_inicial}\n")
            archivo.write(f"Estado final: {self.estado_final}\n")
            archivo.write(f"Transiciones: {self.transiciones}\n")
            print(f"Autómata guardado en: autbasic/{nombre_archivo}.txt")

def crear_afn_basico(simbolo):
    return AFN(simbolo)
