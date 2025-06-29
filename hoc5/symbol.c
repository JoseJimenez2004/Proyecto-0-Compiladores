#include "hoc.h"
#include <string.h>

Symbol *symtab = NULL;

Symbol *lookup(char *name) {
    for (Symbol *sp = symtab; sp != NULL; sp = sp->next)
        if (strcmp(sp->name, name) == 0) return sp;
    return NULL;
}

Symbol *install(char *name, int type, double val) {
    Symbol *sp = emalloc(sizeof(Symbol));
    sp->name = strdup(name);
    sp->type = type;
    sp->u.val = val;
    sp->next = symtab;
    symtab = sp;
    return sp;
}  