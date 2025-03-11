from ..afn import AFN

def unir_afn(afn1, afn2):
    afn = AFN()
    estado_inicial = afn.agregar_estado()
    estado_final = afn.agregar_estado(final=True)
    afn.agregar_transicion(estado_inicial, 'ε', afn1.inicial)
    afn.agregar_transicion(estado_inicial, 'ε', afn2.inicial)
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
    afn.finales.update(afn1.finales)
    afn.finales.update(afn2.finales)
    afn.inicial = estado_inicial
    return afn
