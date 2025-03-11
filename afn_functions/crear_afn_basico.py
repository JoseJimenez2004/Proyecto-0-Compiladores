from ..afn import AFN

def crear_afn_basico(simbolo):
    afn = AFN()
    inicial = afn.agregar_estado()
    final = afn.agregar_estado(final=True)
    afn.agregar_transicion(inicial, simbolo, final)
    afn.inicial = inicial
    return afn
