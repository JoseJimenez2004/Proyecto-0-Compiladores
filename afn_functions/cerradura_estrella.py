from ..afn import AFN

def cerradura_estrella(afn):
    nuevo_afn = AFN()
    estado_inicial = nuevo_afn.agregar_estado()
    estado_final = nuevo_afn.agregar_estado(final=True)
    nuevo_afn.agregar_transicion(estado_inicial, 'ε', afn.inicial)
    nuevo_afn.agregar_transicion(estado_inicial, 'ε', estado_final)
    for estado in afn.estados:
        nuevo_afn.estados.add(estado)
    for (desde, simbolo), hasta in afn.transiciones.items():
        for estado in hasta:
            nuevo_afn.agregar_transicion(desde, simbolo, estado)
    for final in afn.finales:
        nuevo_afn.agregar_transicion(final, 'ε', estado_final)
        nuevo_afn.agregar_transicion(final, 'ε', afn.inicial)
    nuevo_afn.inicial = estado_inicial
    nuevo_afn.finales.add(estado_final)
    return nuevo_afn
