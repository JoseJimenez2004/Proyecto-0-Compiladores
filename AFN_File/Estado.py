from .Transicion import Transicion

class Estado:
    contEdos = 0  # Variable estática para el conteo de estados

    def __init__(self, es_aceptacion=False, token=None):
        """
        Constructor del estado.
        :param id_estado: Identificador único del estado.
        :param es_aceptacion: Si el estado es de aceptación.
        :param token: El token que acepta este estado si es de aceptación.
        metodo estatico de contador de estados
        """
        self.id_estado = Estado.contEdos
        Estado.contEdos += 1  # Autoincremental
        self.transiciones = set()  # Conjunto de transiciones
        self.es_aceptacion = es_aceptacion  # Si el estado es de aceptación
        self.token = token  # Token asociado al estado de aceptación

    def agregar_transicion(self, simbolo, estado_destino):
        """
        Agrega una transición desde este estado a otro estado.
        :param simbolo: El símbolo de entrada que dispara la transición (puede ser un conjunto).
        :param estado_destino: El estado de destino al cual se llega con el símbolo.
        """
        self.transiciones.add(Transicion(simbolo, estado_destino))

    def __repr__(self):
        estado_str = f"Estado({self.id_estado})"
        if self.es_aceptacion:
            estado_str += f" [Aceptación, Token: {self.token}]"
        return estado_str
