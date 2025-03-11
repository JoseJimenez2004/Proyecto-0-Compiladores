from afn import AFN

def unir_afn(afn1, afn2):
    # Crear un nuevo estado inicial y final
    nuevo_estado_inicial = max(afn1.estados + afn2.estados) + 1
    nuevo_estado_final = nuevo_estado_inicial + 1

    # Transiciones epsilon desde el nuevo estado inicial a los iniciales de ambos AFNs
    transiciones = afn1.transiciones + afn2.transiciones
    transiciones.append((nuevo_estado_inicial, 'ε', afn1.estado_inicial))  # Epsilon de nuevo estado inicial a AFN1
    transiciones.append((nuevo_estado_inicial, 'ε', afn2.estado_inicial))  # Epsilon de nuevo estado inicial a AFN2

    # Transiciones epsilon desde los finales de ambos AFNs al nuevo estado final
    transiciones.append((afn1.estado_final, 'ε', nuevo_estado_final))  # Epsilon de estado final AFN1 al nuevo final
    transiciones.append((afn2.estado_final, 'ε', nuevo_estado_final))  # Epsilon de estado final AFN2 al nuevo final

    # Los estados combinados de ambos AFNs, incluyendo los nuevos estados
    estados = afn1.estados + afn2.estados + [nuevo_estado_inicial, nuevo_estado_final]

    # El nuevo estado inicial y final
    estado_inicial = nuevo_estado_inicial
    estado_final = nuevo_estado_final

    # Crear el nuevo AFN con los estados, transiciones, estado inicial y final
    return AFN(estados, transiciones, estado_inicial, estado_final)
