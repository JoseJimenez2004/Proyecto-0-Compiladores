
from crear_afn_basico import crear_afn_basico
def menu():
    while True:
        print("\nMenu:")
        print("1. Crear un AFN Básico")
        print("2. Unir 2 AFN's")
        print("3. Concatenar 2 AFN's")
        print("4. Cerradura * de un AFN")
        print("5. Cerradura + de un AFN")
        print("6. Opcionar ?")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            simbolo = input("Ingrese el símbolo para el AFN Básico: ")
            afn = crear_afn_basico(simbolo)  # Llamamos a la función para crear el AFN
            afn.mostrar()  # Mostramos el AFN creado

        elif opcion == "2":
            simbolo1 = input("Ingrese símbolo para AFN 1: ")
            simbolo2 = input("Ingrese símbolo para AFN 2: ")
            afn1 = crear_afn_basico(simbolo1)
            afn2 = crear_afn_basico(simbolo2)
            afn_unido = unir_afn(afn1, afn2)
            afn_unido.mostrar()

        elif opcion == "3":
            print("Opción 3 seleccionada: Concatenar 2 AFN's")

        elif opcion == "4":
            print("Opción 4 seleccionada: Cerradura * de un AFN")

        elif opcion == "5":
            print("Opción 5 seleccionada: Cerradura + de un AFN")

        elif opcion == "6":
            print("Opción 6 seleccionada: Opcionar ?")

        elif opcion == "7":
            print("Saliendo...")
            break

if __name__ == "__main__":
    menu()
