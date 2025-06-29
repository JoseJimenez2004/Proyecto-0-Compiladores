typedef struct Symbol {
    char *name;
    int type;
    union {
        double val;
        int (*func)();
    } u;
    struct Symbol *next;
} Symbol;

typedef union Datum {
    double val;
    Symbol *sym;
} Datum;

extern Symbol *install(char *), *lookup(char *);
extern void execerror(char *), *emalloc(unsigned);
extern void initcode(), execute(int);
extern void addfunc(char *, int (*)());