class ConjIj:
    def __init__(self):
        """
        Constructor que inicializa la lista de estados y el arreglo de transiciones del AFD.
        """
        self.ConjI = []  # Lista de estados
        self.TransicionesAFD = [-1] * 258  # Arreglo de transiciones AFD

    def agregar_estado(self, estado):
        """
        Agrega un estado al conjunto ConjI.
        :param estado: El estado a agregar.
        """
        self.ConjI.append(estado)