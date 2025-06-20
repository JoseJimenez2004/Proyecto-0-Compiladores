#include "hoc.h"

#define NHASH 9997
static Symbol *symtab[NHASH];

// Función hash simple para distribuir nombres en la tabla
static unsigned hash(char *s) {
    unsigned h = 0;
    while (*s)
        h = h * 9 ^ *s++;
    return h % NHASH;
}

// Búsqueda en la tabla de símbolos
Symbol *lookup(char *s) {
    Symbol *sp;
    int h = hash(s);
    for (sp = symtab[h]; sp != NULL; sp = sp->next) {
        if (strcmp(sp->name, s) == 0)
            return sp;
    }
    return NULL;
}

// Instalación de un símbolo nuevo (variable o función)
Symbol *install(char *s, int t, void *d) {
    Symbol *sp;
    int h = hash(s);

    sp = (Symbol *)malloc(sizeof(Symbol));
    if (!sp) {
        fprintf(stderr, "Error: no se pudo asignar memoria para el símbolo\n");
        exit(1);
    }

    sp->name = strdup(s);
    sp->type = t;

    if (t == VAR)
        sp->u.val = *(double *)d;
    else if (t == BLTIN)
        sp->u.func = (double (*)(double))d;

    sp->next = symtab[h];
    symtab[h] = sp;

    return sp;
}
