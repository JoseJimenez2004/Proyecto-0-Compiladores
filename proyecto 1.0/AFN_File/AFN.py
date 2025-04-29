from .Estado import Estado

class AFN:
    contId = 0  # Variable estática para el conteo de estados

    def __init__(self):
        """
        Constructor de un AFN.
        :param id_afn: Identificador único del AFN.
        :param estado_inicial: Estado inicial del AFN.
        :param estado_final: Estado final del AFN.
        """
        self.id_afn = AFN.contId  # ID único del AFN hacerlo auto incremental
        AFN.contId += 1
        self.edo_inicial = None  # Estado inicial
        self.edos_afn = set()  # Conjunto de estados
        self.alfabeto = set()  # Alfabeto del AFN
        self.edos_acept = set()  # Conjunto de estados de aceptación

    def agregar_estado(self, estado):
        """
        Agrega un estado al conjunto de estados del AFN.
        :param estado: Estado a agregar.
        """
        self.edos_afn.add(estado)

    @staticmethod
    def afn_basico(simbolo, token=None):
        """
        Crea un AFN básico que reconoce un solo símbolo o un rango de símbolos.
        :param simbolo: El símbolo o rango de símbolos reconocido por el AFN.
        :param token: Token asociado al estado de aceptación (si es necesario).
        :return: Un AFN básico.
        """
        afn = AFN()  # Crea un nuevo AFN

        # Crear estado inicial y estado de aceptación
        estado_inicial = Estado()
        estado_aceptacion = Estado(es_aceptacion=True, token=token)

        # Crear la transición desde el estado inicial al de aceptación
        if isinstance(simbolo, list) and len(simbolo) == 2:
            # Si es un rango de símbolos, crear una transición para cada símbolo del rango
            for c in range(ord(simbolo[0]), ord(simbolo[1]) + 1):
                estado_inicial.agregar_transicion(chr(c), estado_aceptacion)
                afn.alfabeto.add(chr(c))  # Agregar al alfabeto
        else:
            # Si es un solo símbolo
            estado_inicial.agregar_transicion(simbolo, estado_aceptacion)
            afn.alfabeto.add(simbolo)

        # Asignar el estado inicial y el conjunto de estados de aceptación
        afn.edo_inicial = estado_inicial
        afn.edos_acept.add(estado_aceptacion)

        # Agregar los estados al conjunto de estados del AFN
        afn.agregar_estado(estado_inicial)
        afn.agregar_estado(estado_aceptacion)

        return afn

    def concatenar(self, afn2):
        """
        Concatenación de dos AFNs.
        :param afn2: Otro AFN a concatenar.
        :return: El AFN modificado tras la operación.
        """
        # Crear un nuevo estado intermedio e1
        e1 = Estado()
        e2 = Estado()
        #Hace de haceptacion el estado e2
        e2.es_aceptacion = True

        # Desde cada estado de aceptación de afn1, crear una transición epsilon hacia e1
        for e in self.edos_acept:
            e.agregar_transicion('ε', afn2.edo_inicial)
            e.es_aceptacion = False  # Los estados de aceptación de afn1 ya no serán de aceptación

        for e in afn2.edos_acept:
            e.agregar_transicion('ε', e2)
            e.es_aceptacion = False  # Los estados de aceptación de afn1 ya no serán de aceptación

        # Desde el estado intermedio e1, crear una transición epsilon hacia el estado inicial de afn2
        e1.agregar_transicion('ε', self.edo_inicial)
        self.edo_inicial = e1

        self.edos_afn.add(e1)
        self.edos_afn.add(e2)

        # Unir los conjuntos de estados de ambos AFNs
        self.edos_afn.update(afn2.edos_afn)

        # Eliminar la referencia al estado inicial de afn2, no lo conservamos como tal
        afn2.edo_inicial = None

        # Actualizar los estados de aceptación: ahora son los estados de aceptación de afn2
        self.edos_acept.clear()
        afn2.edos_acept.clear()
        self.edos_acept.add(e2)

        # Actualizar el alfabeto uniendo los alfabetos de ambos AFNs
        self.alfabeto.update(afn2.alfabeto)

        return self

    def unir(self, afn2):
        """
        Unión de dos AFNs (OR).
        :param afn2: Otro AFN con el cual se realizará la unión.
        :return: El AFN modificado tras la operación.
        """
        #Crear nuevos estados e1 y e2
        e1 = Estado() #Nuevo edo inicial
        e2 = Estado(es_aceptacion=True) # Nuevo edo de aceptacion

        #Crear transiciones vacias desde e1 a los estados iniciales de ambos afn's
        e1.agregar_transicion('ε', self.edo_inicial)
        e1.agregar_transicion('ε', afn2.edo_inicial)

        #Reasignar transiciones desde los estados de aceptacion a ambos AFN's hacia el nuevo estado e2
        for e in self.edos_acept:
            e.agregar_transicion('ε', e2)
            e.es_aceptacion = False
        for e in afn2.edos_acept:
            e.agregar_transicion('ε', e2)
            e.es_aceptacion = False

        #Actualizar estado inicial y conjunto de esatdos de aceptacion
        self.edo_inicial = e1
        self.edos_acept.clear()
        self.edos_acept.add(e2)

        # Unir los conjuntos de estados y alfabeto
        self.edos_afn.update(afn2.edos_afn)
        self.edos_afn.add(e1)
        self.edos_afn.add(e2)
        self.alfabeto.update(afn2.alfabeto)

        return self

    def unir2(self, afn2):
        """
        Unión de dos AFNs (OR).
        :param afn2: Otro AFN con el cual se realizará la unión.
        :return: El AFN modificado tras la operación.
        """
        #Crear nuevos estados e1 y e2
        e1 = Estado() #Nuevo edo inicial

        #Crear transiciones vacias desde e1 a los estados iniciales de ambos afn's
        e1.agregar_transicion('ε', self.edo_inicial)
        e1.agregar_transicion('ε', afn2.edo_inicial)

        #Actualizar estado inicial y conjunto de esatdos de aceptacion
        self.edo_inicial = None
        afn2.edo_inicial = None
        self.edo_inicial = e1

        # Unir los conjuntos de estados y alfabeto
        self.edos_afn.update(afn2.edos_afn)
        self.edos_acept.update(afn2.edos_acept)
        self.edos_afn.add(e1)
        self.alfabeto.update(afn2.alfabeto)

        return self

    def cerradura(self):
        """
        Aplicación de la cerradura positiva.
        :return: El AFN modificado tras la operación.
        """
        e1 = Estado()  # Nuevo estado inicial
        e2 = Estado(es_aceptacion=True)  # Nuevo estado de aceptación

        # Agregar transiciones desde e1 hacia el estado inicial actual y el nuevo estado de aceptación
        e1.agregar_transicion('ε', self.edo_inicial)

        # Agregar transiciones desde los estados de aceptación actuales hacia el nuevo estado de aceptación y el inicial
        for e in self.edos_acept:
            e.agregar_transicion('ε', e2)
            e.agregar_transicion('ε', self.edo_inicial)
            e.es_aceptacion = False

        # Actualizar el estado inicial y el conjunto de estados de aceptación
        self.edo_inicial = e1
        self.edos_acept.clear()
        self.edos_acept.add(e2)

        # Agregar los nuevos estados al conjunto de estados
        self.edos_afn.add(e1)
        self.edos_afn.add(e2)

        return self

    def cierre_kleene(self):
        """
        Aplicación de la cerradura (cierre de Kleene).
        :return: El AFN modificado tras la operación.
        """
        e1 = Estado()  # Nuevo estado inicial
        e2 = Estado(es_aceptacion=True)  # Nuevo estado de aceptación

        # Agregar transiciones desde e1 hacia el estado inicial actual y el nuevo estado de aceptación
        e1.agregar_transicion('ε', self.edo_inicial)
        e1.agregar_transicion('ε', e2)

        # Agregar transiciones desde los estados de aceptación actuales hacia el nuevo estado de aceptación y el inicial
        for e in self.edos_acept:
            e.agregar_transicion('ε', e2)
            e.agregar_transicion('ε', self.edo_inicial)
            e.es_aceptacion = False

        # Actualizar el estado inicial y el conjunto de estados de aceptación
        self.edo_inicial = e1
        self.edos_acept.clear()
        self.edos_acept.add(e2)

        # Agregar los nuevos estados al conjunto de estados
        self.edos_afn.add(e1)
        self.edos_afn.add(e2)

        return self

    def opcional(self):
        """
        Aplicación de la operación opcional (a|ε).
        :return: El AFN modificado tras la operación.
        """
        e1 = Estado()  # Nuevo estado inicial
        e2 = Estado(es_aceptacion=True)  # Nuevo estado de aceptación

        # Agregar transiciones desde e1 al estado inicial actual y al nuevo estado de aceptación
        e1.agregar_transicion('ε', self.edo_inicial)
        e1.agregar_transicion('ε', e2)

        # Agregar transiciones vacías desde los estados de aceptación actuales al nuevo estado de aceptación
        for e in self.edos_acept:
            e.agregar_transicion('ε', e2)
            e.es_aceptacion = False

        # Actualizar estado inicial y conjunto de estados de aceptación
        self.edo_inicial = e1
        self.edos_acept.clear()
        self.edos_acept.add(e2)

        # Agregar nuevos estados al conjunto de estados
        self.edos_afn.add(e1)
        self.edos_afn.add(e2)

        return self

    def cerradura_epsilon(self, conjunto_estados):
        # Inicializar el resultado con los estados de entrada
        resultado = set(conjunto_estados)

        # Pila para procesar los estados (inicialmente con los estados dados)
        pila = list(conjunto_estados)

        # Mientras haya estados en la pila
        while pila:
            # Tomar un estado de la pila
            estado_actual = pila.pop()
            # Revisar las transiciones desde el estado actual
            for transicion in estado_actual.transiciones:
                # Si la transición es por ε
                if 'ε' in transicion.simbolo and transicion.estado_destino not in resultado:
                    # Agregar el estado destino al resultado
                    resultado.add(transicion.estado_destino)
                    # Agregar el estado destino a la pila para seguir procesando
                    pila.append(transicion.estado_destino)

        return resultado

    def mover(self, conjunto_estados, simbolo):
        """
        Calcula el conjunto de estados alcanzables desde un conjunto de estados dado mediante una transición con el símbolo proporcionado.
        :param conjunto_estados: El conjunto de estados desde los cuales se desea mover.
        :param simbolo: El símbolo de la transición.
        :return: Un conjunto de estados alcanzables mediante el símbolo.
        """
        resultado = set()

        # Para cada estado en el conjunto de entrada
        for estado in conjunto_estados:
            # Revisar cada transición del estado
            for transicion in estado.transiciones:
                # Si la transición tiene el símbolo dado, agregar el estado destino al resultado
                if simbolo in transicion.simbolo:
                    resultado.add(transicion.estado_destino)

        return resultado

    def go_to(self, conjunto_estados, simbolo):
        return self.cerradura_epsilon(self.mover(conjunto_estados,simbolo))

    def mostrar_afn(self):
        """
        Muestra los estados, transiciones y símbolos del AFN.
        """
        print(f"AFN ID: {self.id_afn}")
        print("Estados del AFN:")

        for estado in self.edos_afn:
            # Indicar si el estado es de aceptación y mostrar el token
            aceptacion_str = "Sí" if estado.es_aceptacion else "No"
            token_str = f"Token: {estado.token}" if estado.token else "No Token"

            print(f"Estado {estado.id_estado}: Aceptación: {aceptacion_str}, {token_str}")

            # Mostrar todas las transiciones del estado
            for transicion in estado.transiciones:
                print(
                    f"  - Transición con símbolo '{transicion.simbolo}' hacia Estado {transicion.estado_destino.id_estado}")

        print("\nAlfabeto:", self.alfabeto)
        print("Estados de aceptación:", [estado.id_estado for estado in self.edos_acept])
        print("Estado inicial:", self.edo_inicial.id_estado)
        print("----------\n")
