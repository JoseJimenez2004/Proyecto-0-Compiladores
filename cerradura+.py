import os

class AFN:
    def __init__(self, simbolo, transiciones, estado_inicial, estado_final):
        self.simbolo = simbolo
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
    
    def guardar_en_archivo(self, nombre_archivo, carpeta='cerradurapositiva'):
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

def aplicar_cerradura_positiva(afn):
    nuevo_estado_inicial = afn.estado_inicial
    nuevo_estado_final = max(afn.estado_final, afn.estado_inicial) + 1
    
    # Agregar la transición epsilon entre el estado final y el estado inicial
    transiciones = afn.transiciones + [
        (afn.estado_final, 'ε', nuevo_estado_inicial),  # Añadir la cerradura positiva
        (nuevo_estado_final, 'ε', afn.estado_inicial)   # Conectar el nuevo estado final al inicial
    ]
    
    afn_cerradura = AFN(f"{afn.simbolo}^+", transiciones, nuevo_estado_inicial, nuevo_estado_final)
    return afn_cerradura

def cerradura_positiva_afn():
    nombre_afn = seleccionar_archivo_de_automatac()  # Selecciona el archivo de autómata
    
    if nombre_afn is None:
        return  # Si no se seleccionó un archivo, termina la función
    
    try:
        afn = cargar_afn_desde_archivo(nombre_afn, carpeta='autbasic')
    except FileNotFoundError as e:
        print(e)
        return
    
    # Aplicar la cerradura positiva sin importar si el autómata cumple los requisitos
    afn_cerradura = aplicar_cerradura_positiva(afn)
    
    # Guardar el nuevo AFN con cerradura positiva en la carpeta 'cerradurapositiva'
    nombre_resultado = f"{nombre_afn}_cerradura_positiva"
    afn_cerradura.guardar_en_archivo(nombre_resultado, carpeta='cerradurapositiva')
    
    print(f"AFN con cerradura positiva guardado en: cerradurapositiva/{nombre_resultado}.txt")

if __name__ == "__main__":
    cerradura_positiva_afn()
