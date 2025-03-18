from crear_afn_basico import crear_afn_basico
from unir_afn import unir_afn_desde_archivos  # Importamos la función para unir AFNs

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

            # Guardamos el AFN en un archivo con un nombre único
            nombre_archivo = input("Ingrese el nombre para el archivo de este AFN: ")
            afn.guardar_en_archivo(nombre_archivo)  # Guardamos el AFN en un archivo

        elif opcion == "2":
            unir_afn_desde_archivos()  # Llamamos a la función para unir 2 AFNs

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
