import os

class AFN:
    def __init__(self, simbolo, transiciones, estado_inicial, estado_final):
        self.simbolo = simbolo
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
    
    def guardar_en_archivo(self, nombre_archivo, carpeta='concaafn'):  # Cambio aquí de 'unirafn' a 'concaafn'
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

def concatenar_afn_desde_archivos():
    if not os.path.exists('concaafn'):  # Cambié la carpeta de salida a 'concaafn'
        os.makedirs('concaafn')
    
    nombre_afn1 = input("Ingrese el nombre del primer AFN (sin .txt): ")
    nombre_afn2 = input("Ingrese el nombre del segundo AFN (sin .txt): ")
    nombre_resultado = input("Ingrese el nombre del AFN resultante (sin .txt): ")
    
    afn1 = cargar_afn_desde_archivo(nombre_afn1)
    afn2 = cargar_afn_desde_archivo(nombre_afn2)
    
    nuevo_estado_inicial = afn1.estado_inicial  # El estado inicial de la concatenación es el mismo que el del primer AFN
    nuevo_estado_final = afn2.estado_final      # El estado final de la concatenación es el mismo que el del segundo AFN
    
    # Renombrar los estados del segundo AFN
    desplazamiento = max(afn1.estado_final, afn2.estado_final) + 1
    afn2_renombrado = [(q1 + desplazamiento, simbolo, q2 + desplazamiento) for (q1, simbolo, q2) in afn2.transiciones]
    
    # Concatenar las transiciones
    transiciones = afn1.transiciones + afn2_renombrado
    
    # Añadir transiciones epsilon para la concatenación
    transiciones.append((afn1.estado_final, 'ε', afn2.estado_inicial + desplazamiento))  # Conectar el final del primero con el inicio del segundo
    
    # Crear el nuevo AFN con el símbolo combinado (concatenación de los símbolos)
    afn_concatenado = AFN(f"{afn1.simbolo}{afn2.simbolo}", transiciones, nuevo_estado_inicial, nuevo_estado_final)
    
    # Guardar el AFN concatenado en un archivo
    afn_concatenado.guardar_en_archivo(nombre_resultado, carpeta='concaafn')
    
    print(f"AFN concatenado guardado en: concaafn/{nombre_resultado}.txt")

if __name__ == "__main__":
    concatenar_afn_desde_archivos()
