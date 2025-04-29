import os

class AFN:
    def __init__(self, simbolo, transiciones, estado_inicial, estado_final):
        self.simbolo = simbolo
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
    
    def guardar_en_archivo(self, nombre_archivo, carpeta='opcionalafn'):
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

def cargar_afn_desde_archivo(nombre_archivo, carpeta='autbasic'):
    ruta = f'{carpeta}/{nombre_archivo}.txt'
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

def seleccionar_archivo_de_automatac():
    # Listar los archivos en la carpeta 'autbasic'
    archivos = [f for f in os.listdir('autbasic') if f.endswith('.txt')]
    
    if not archivos:
        print("No hay archivos disponibles en la carpeta 'autbasic'.")
        return None
    
    print("Selecciona un archivo de autómata para trabajar:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")
    
    seleccion = int(input("Ingresa el número del archivo seleccionado: ")) - 1
    if seleccion < 0 or seleccion >= len(archivos):
        print("Selección inválida.")
        return None
    
    return archivos[seleccion].replace('.txt', '')  # Eliminar la extensión '.txt' para solo retornar el nombre

def aplicar_cerradura_opcional(afn):
    nuevo_estado_inicial = max(afn.estado_final, afn.estado_inicial) + 1
    nuevo_estado_final = nuevo_estado_inicial + 1
    
    # Agregar las transiciones para la cerradura opcional
    transiciones = afn.transiciones + [
        # Transición epsilon desde el nuevo estado inicial al estado original inicial
        (nuevo_estado_inicial, 'ε', afn.estado_inicial),
        # Transición epsilon desde el estado final al nuevo estado final
        (afn.estado_final, 'ε', nuevo_estado_final),
        # Transición epsilon al nuevo estado final para permitir la opción de no hacer nada (vacío)
        (nuevo_estado_inicial, 'ε', nuevo_estado_final)
    ]
    
    afn_opcional = AFN(f"{afn.simbolo}? (Opcional)", transiciones, nuevo_estado_inicial, nuevo_estado_final)
    return afn_opcional

def cerradura_opcional_afn():
    nombre_afn = seleccionar_archivo_de_automatac()  # Selecciona el archivo de autómata
    
    if nombre_afn is None:
        return  # Si no se seleccionó un archivo, termina la función
    
    try:
        afn = cargar_afn_desde_archivo(nombre_afn, carpeta='autbasic')
    except FileNotFoundError as e:
        print(e)
        return
    
    # Aplicar la cerradura opcional
    afn_opcional = aplicar_cerradura_opcional(afn)
    
    # Guardar el nuevo AFN con cerradura opcional en la carpeta 'opcionalafn'
    nombre_resultado = f"{nombre_afn}_cerradura_opcional"
    afn_opcional.guardar_en_archivo(nombre_resultado, carpeta='opcionalafn')
    
    print(f"AFN con cerradura opcional guardado en: opcionalafn/{nombre_resultado}.txt")

if __name__ == "__main__":
    cerradura_opcional_afn()
