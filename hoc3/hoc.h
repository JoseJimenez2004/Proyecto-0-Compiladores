#ifndef HOC_H
#define HOC_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Tipos de símbolos
enum { VAR, BLTIN };

// Estructura para representar un símbolo (variable o función)
typedef struct Symbol {
    char *name;                // nombre del símbolo
    int type;                  // VAR o BLTIN
    union {
        double val;            // valor para variables
        double (*func)(double); // puntero a función para funciones matemáticas
    } u;
    struct Symbol *next;       // siguiente símbolo en la lista (para manejo por hash)
} Symbol;

// Prototipos de funciones
Symbol *install(char *s, int t, void *d);
Symbol *lookup(char *s);
void init(void); // se usa en init.c para inicializar funciones y constantes

#endif // HOC_H
