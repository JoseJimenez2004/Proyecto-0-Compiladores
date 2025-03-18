import os

class AFN:
    def __init__(self, simbolo, transiciones, estado_inicial, estado_final):
        self.simbolo = simbolo
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
    
    def guardar_en_archivo(self, nombre_archivo, carpeta='cerradurakleene'):
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

def aplicar_cerradura_kleene(afn):
    nuevo_estado_inicial = max(afn.estado_final, afn.estado_inicial) + 1
    nuevo_estado_final = nuevo_estado_inicial + 1
    
    # Agregar las transiciones para la cerradura de Kleene
    transiciones = afn.transiciones + [
        # Transición epsilon desde el nuevo estado inicial al estado original inicial
        (nuevo_estado_inicial, 'ε', afn.estado_inicial),
        # Transición epsilon desde el estado final al nuevo estado final
        (afn.estado_final, 'ε', nuevo_estado_final),
        # Transición epsilon del nuevo estado final al estado inicial original para permitir la repetición
        (nuevo_estado_final, 'ε', afn.estado_inicial),
        # Transición epsilon al nuevo estado final para permitir la opción de no hacer nada
        (nuevo_estado_inicial, 'ε', nuevo_estado_final)
    ]
    
    afn_cerradura = AFN(f"{afn.simbolo}* (Kleene)", transiciones, nuevo_estado_inicial, nuevo_estado_final)
    return afn_cerradura

def cerradura_kleene_afn():
    nombre_afn = seleccionar_archivo_de_automatac()  # Selecciona el archivo de autómata
    
    if nombre_afn is None:
        return  # Si no se seleccionó un archivo, termina la función
    
    try:
        afn = cargar_afn_desde_archivo(nombre_afn, carpeta='autbasic')
    except FileNotFoundError as e:
        print(e)
        return
    
    # Aplicar la cerradura de Kleene sin importar si el autómata cumple los requisitos
    afn_cerradura = aplicar_cerradura_kleene(afn)
    
    # Guardar el nuevo AFN con cerradura de Kleene en la carpeta 'cerradurakleene'
    nombre_resultado = f"{nombre_afn}_cerradura_kleene"
    afn_cerradura.guardar_en_archivo(nombre_resultado, carpeta='cerradurakleene')
    
    print(f"AFN con cerradura de Kleene guardado en: cerradurakleene/{nombre_resultado}.txt")

if __name__ == "__main__":
    cerradura_kleene_afn()
