
#include "hoc.h"
#include <math.h>  // para las funciones matemáticas estándar

extern Symbol *install(char *s, int t, void *d);

void init() {
    // Funciones matemáticas incorporadas
    static struct {
        char *name;
        double (*func)(double);
    } builtins[] = {
        {"sin", sin},
        {"cos", cos},
        {"atan", atan},
        {"exp", exp},
        {"log", log},
        {"log10", log10},
        {"sqrt", sqrt},
        {"int", floor},   // redondeo hacia abajo para la función int
        {"abs", fabs},    // valor absoluto para double
        {NULL, NULL}
    };

    for (int i = 0; builtins[i].name != NULL; i++) {
        install(builtins[i].name, BLTIN, builtins[i].func);
    }

    // Constantes predefinidas
    static struct {
        char *name;
        double val;
    } consts[] = {
        {"pi", 3.141592},
        {"e", 2.71828},
        {"gamma", 0.577215},
        {"deg", 57.295779},
        {"phi", 1.618034},
        {NULL, 0}
    };

    for (int i = 0; consts[i].name != NULL; i++) {
        install(consts[i].name, VAR, &consts[i].val);
    }
}
