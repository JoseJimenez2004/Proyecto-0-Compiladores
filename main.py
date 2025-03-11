from afn_functions.crear_afn_basico import crear_afn_basico
from afn_functions.unir_afn import unir_afn
from afn_functions.concatenar_afn import concatenar_afn
from afn_functions.cerradura_estrella import cerradura_estrella
from afn_functions.cerradura_estrella_plus import cerradura_estrella_plus
from afn_functions.opcional import opcional

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
            afn = crear_afn_basico(simbolo)
            afn.mostrar()

        elif opcion == "2":
            afn1 = crear_afn_basico(input("Ingrese símbolo para AFN 1: "))
            afn2 = crear_afn_basico(input("Ingrese símbolo para AFN 2: "))
            afn = unir_afn(afn1, afn2)
            afn.mostrar()

        elif opcion == "3":
            afn1 = crear_afn_basico(input("Ingrese símbolo para AFN 1: "))
            afn2 = crear_afn_basico(input("Ingrese símbolo para AFN 2: "))
            afn = concatenar_afn(afn1, afn2)
            afn.mostrar()

        elif opcion == "4":
            afn = crear_afn_basico(input("Ingrese símbolo para el AFN: "))
            afn_cerradura = cerradura_estrella(afn)
            afn_cerradura.mostrar()

        elif opcion == "5":
            afn = crear_afn_basico(input("Ingrese símbolo para el AFN: "))
            afn_cerradura_plus = cerradura_estrella_plus(afn)
            afn_cerradura_plus.mostrar()

        elif opcion == "6":
            afn = crear_afn_basico(input("Ingrese símbolo para el AFN: "))
            afn_opcional = opcional(afn)
            afn_opcional.mostrar()

        elif opcion == "7":
            print("Saliendo...")
            break

if __name__ == "__main__":
    menu()
