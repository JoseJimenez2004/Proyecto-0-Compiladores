import os

class AFN:
    def __init__(self, simbolo, transiciones, estado_inicial, estado_final):
        self.simbolo = simbolo
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
    
    def guardar_en_archivo(self, nombre_archivo, carpeta='unirafn'):
        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        ruta = f'{carpeta}/{nombre_archivo}.txt'
        
        # Usar codificación UTF-8 para evitar problemas con caracteres especiales
        with open(ruta, 'w', encoding='utf-8') as archivo:
            archivo.write(f"Simbolo: {self.simbolo}\n")
            archivo.write(f"Estado inicial: {self.estado_inicial}\n")
            archivo.write(f"Estado final: {self.estado_final}\n")
            archivo.write(f"Transiciones: {self.transiciones}\n")

def cargar_afn_desde_archivo(nombre_archivo):
    ruta = f'autbasic/{nombre_archivo}.txt'
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo {ruta} no existe.")
    
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
    
    simbolo = lineas[0].strip().split(': ')[1]
    estado_inicial = int(lineas[1].strip().split(': ')[1])
    estado_final = int(lineas[2].strip().split(': ')[1])
    transiciones = eval(lineas[3].strip().split(': ')[1])  # Convierte la cadena en lista de tuplas
    
    # Asegúrate de que el objeto AFN se inicialice correctamente
    afn = AFN(simbolo, transiciones, estado_inicial, estado_final)
    return afn

def unir_afn_desde_archivos():
    if not os.path.exists('unirafn'):
        os.makedirs('unirafn')
    
    nombre_afn1 = input("Ingrese el nombre del primer AFN (sin .txt): ")
    nombre_afn2 = input("Ingrese el nombre del segundo AFN (sin .txt): ")
    nombre_resultado = input("Ingrese el nombre del AFN resultante (sin .txt): ")
    
    afn1 = cargar_afn_desde_archivo(nombre_afn1)
    afn2 = cargar_afn_desde_archivo(nombre_afn2)
    
    nuevo_estado_inicial = max(afn1.estado_final, afn2.estado_final) + 1
    nuevo_estado_final = nuevo_estado_inicial + 3
    
    # Renombrar los estados del segundo AFN
    desplazamiento = nuevo_estado_inicial + 1
    afn2_renombrado = [(q1 + desplazamiento, simbolo, q2 + desplazamiento) for (q1, simbolo, q2) in afn2.transiciones]
    
    # Unir las transiciones
    transiciones = afn1.transiciones + afn2_renombrado
    transiciones.append((nuevo_estado_inicial, 'ε', afn1.estado_inicial))
    transiciones.append((nuevo_estado_inicial, 'ε', desplazamiento))
    transiciones.append((afn1.estado_final, 'ε', nuevo_estado_final))
    transiciones.append((afn2.estado_final + desplazamiento, 'ε', nuevo_estado_final))
    
    # Crear el nuevo AFN con el símbolo combinado
    afn_unido = AFN(f"{afn1.simbolo}|{afn2.simbolo}", transiciones, nuevo_estado_inicial, nuevo_estado_final)
    
    # Guardar el AFN unido en un archivo
    afn_unido.guardar_en_archivo(nombre_resultado, carpeta='unirafn')
    
    print(f"AFN unido guardado en: unirafn/{nombre_resultado}.txt")

if __name__ == "__main__":
    unir_afn_desde_archivos()
