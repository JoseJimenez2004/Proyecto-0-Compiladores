# analizador_lexico_opcion.py
from AFN_File.AFD import AFD
from AnalizadorLexico import AnalizadorLexico  # Asegúrate de que este archivo esté accesible

def analizador_lexico_opcion():
    archivo_afd = "afd.txt"  # Cambia esto según el archivo de tu AFD
    cadena = input("Introduce la cadena a analizar: ")

    analizador = AnalizadorLexico(cadena, archivo_afd)

    print("\nTokens encontrados:")
    while True:
        token = analizador.yylex()
        if token == 0:
            break
        print(f"Lexema: '{analizador.Lexema}', Token: {token}")
