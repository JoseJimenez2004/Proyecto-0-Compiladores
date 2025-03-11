from ..afn import AFN

def concatenar_afn(afn1, afn2):
    afn = AFN()
    estado_inicial = afn.agregar_estado()
    for estado in afn1.estados:
        afn.estados.add(estado)
    for estado in afn2.estados:
        afn.estados.add(estado)
    for (desde, simbolo), hasta in afn1.transiciones.items():
        for estado in hasta:
            afn.agregar_transicion(desde, simbolo, estado)
    for (desde, simbolo), hasta in afn2.transiciones.items():
        for estado in hasta:
            afn.agregar_transicion(desde, simbolo, estado)
    for final in afn1.finales:
        afn.agregar_transicion(final, 'ε', afn2.inicial)
    afn.inicial = afn1.inicial
    afn.finales = afn2.finales
    return afn
