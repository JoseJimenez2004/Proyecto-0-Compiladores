class Transicion:
    def __init__(self, simbolo, estado_destino):
        """
        Constructor de la transición.
        :param simbolo: Puede ser un solo carácter o un par de caracteres que representen un rango (e.g. ['a', 'z']).
        :param estado_destino: Estado destino de la transición.
        """
        if isinstance(simbolo, list) and len(simbolo) == 2:
            # Si es una lista con dos caracteres, generar el rango de caracteres
            self.simbolo = {chr(c) for c in range(ord(simbolo[0]), ord(simbolo[1]) + 1)}
        else:
            # Si es un solo carácter, lo dejamos como un conjunto de un solo elemento
            self.simbolo = {simbolo}

        self.estado_destino = estado_destino

    def __repr__(self):
        simbolos = ''.join(self.simbolo)  # Mostrar todos los caracteres de la transición
        return f"Transicion({simbolos}, {self.estado_destino.id_estado})"