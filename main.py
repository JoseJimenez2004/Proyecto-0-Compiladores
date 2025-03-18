from crear_afn_basico import crear_afn_basico
from unir_afn import unir_afn_desde_archivos
from concatenar import concatenar_afn_desde_archivos
from cerradurapositiva import cerradura_positiva_afn  
from cerradurakleenestar import cerradura_kleene_afn
from cerraduraopcional import cerradura_opcional_afn
def menu():
    while True:
        print("\nMenu:")
        print("1. Crear un AFN Básico")
        print("2. Unir 2 AFN's")
        print("3. Concatenar 2 AFN's")
        print("4. Cerradura + de un AFN")
        print("5. Cerradura * de un AFN")
        print("6. Opcionar ?")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_afn_basico()
        elif opcion == "2":
            unir_afn_desde_archivos()  

        elif opcion == "3":
            concatenar_afn_desde_archivos() 

        elif opcion == "4":
            cerradura_positiva_afn()

        elif opcion == "5":
            cerradura_kleene_afn()

        elif opcion == "6":
            cerradura_opcional_afn()

        elif opcion == "7":
            print("Saliendo...")
            break

if __name__ == "__main__":
    menu()
