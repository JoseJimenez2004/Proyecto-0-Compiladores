import csv

class AFD:
    def __init__(self):
        self.estados_afd = []  # Lista de estados del AFD
        self.tabla_transiciones = []  # Tabla de transiciones del AFD
        self.estados_aceptacion = {}  # Diccionario de estados de aceptación {estado: token}

    def agregar_estado(self, estado):
        """
        Agrega un nuevo estado al AFD y lo inicializa en la tabla de transiciones.
        Cada fila tendrá 258 columnas: [ID del estado, transiciones (256 columnas), token o -1]
        """
        id_estado = len(self.estados_afd)
        self.estados_afd.append(estado)
        # Agregar una fila con el ID del estado, transiciones (-1 iniciales), y -1 como no aceptación
        self.tabla_transiciones.append([id_estado] + [-1] * 256 + [-1])

    def agregar_transicion(self, id_estado_origen, simbolo, id_estado_destino):
        """
        Agrega una transición en la tabla de transiciones del AFD.
        La transición se agrega en la columna correspondiente al código ASCII del símbolo.
        """
        self.tabla_transiciones[id_estado_origen][
            ord(simbolo) + 1] = id_estado_destino  # La columna +1 es el offset del ID

    def marcar_aceptacion(self, id_estado, token):
        """
        Marca un estado como estado de aceptación y le asigna un token.
        """
        self.tabla_transiciones[id_estado][-1] = token  # Última columna para el estado de aceptación
        self.estados_aceptacion[id_estado] = token  # Almacenar en el diccionario de estados de aceptación

    def convertir_desde_afn(self, afn):
        """
        Convierte un AFN en un AFD utilizando el método de subconjuntos.
        """
        conjunto_inicial = afn.cerradura_epsilon({afn.edo_inicial})
        subconjuntos = [conjunto_inicial]
        mapeo_subconjuntos = {frozenset(conjunto_inicial): 0}  # Mapeo del conjunto al ID del estado del AFD

        # Inicializar el AFD con el conjunto inicial
        self.agregar_estado(conjunto_inicial)

        # Procesar los subconjuntos
        i = 0
        while i < len(subconjuntos):
            conjunto_actual = subconjuntos[i]
            for simbolo in afn.alfabeto:
                nuevo_conjunto = afn.go_to(conjunto_actual, simbolo)

                if nuevo_conjunto:
                    frozenset_nuevo = frozenset(nuevo_conjunto)
                    if frozenset_nuevo not in mapeo_subconjuntos:
                        nuevo_id = len(subconjuntos)
                        mapeo_subconjuntos[frozenset_nuevo] = nuevo_id
                        subconjuntos.append(nuevo_conjunto)
                        self.agregar_estado(nuevo_conjunto)

                    id_nuevo_conjunto = mapeo_subconjuntos[frozenset_nuevo]
                    self.agregar_transicion(i, simbolo, id_nuevo_conjunto)

            i += 1

        # Determinar los estados de aceptación
        for j, subconjunto in enumerate(subconjuntos):
            for estado in subconjunto:
                if estado in afn.edos_acept:
                    # Marcar el estado como de aceptación y asignar el token
                    self.marcar_aceptacion(j, estado.token)
                    break  # Solo necesitamos un token por subconjunto

    def mostrar_afd(self):
        """
        Muestra la tabla de transiciones del AFD, con el ID de estado y el token de aceptación.
        """
        print("| ID | ... | Código ASCII ... | EsAcep |")
        for fila in self.tabla_transiciones:
            print(f"| {fila[0]:>3} | {fila[1:-1]} | {fila[-1]:>6} |")

    def guardar_AFD_archivo(self, nombre_archivo):
        """
        Guarda el AFD en un archivo CSV, incluyendo la columna del ID y la columna de aceptación.
        """
        with open(nombre_archivo, 'w', newline='') as archivo:
            writer = csv.writer(archivo)
            # Guardar cada fila de la tabla AFD
            for fila in self.tabla_transiciones:
                writer.writerow(fila)

    def leer_AFD_archivo(self, nombre_archivo):
        """
        Lee el AFD desde un archivo CSV y reconstruye la tabla de transiciones y los estados de aceptación.
        """
        with open(nombre_archivo, 'r') as archivo:
            reader = csv.reader(archivo)
            self.tabla_transiciones = []
            for row in reader:
                fila = list(map(int, row))  # Convertir la fila en una lista de enteros
                self.tabla_transiciones.append(fila)
                if fila[-1] != -1:  # Si el último valor es un token de aceptación
                    self.estados_aceptacion[fila[0]] = fila[-1]  # Almacenar el token
