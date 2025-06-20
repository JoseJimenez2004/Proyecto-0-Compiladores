%{
#include "hoc.h"
#include "y.tab.h"

extern Symbol *install(char*, int, void *), *lookup(char*);
static double zero = 0.0;
%}

%%

[ \t]           ; /* ignora espacios y tabulaciones */

[0-9]+(\.[0-9]*)?([eE][-+]?[0-9]+)?    {
                    yylval.val = atof(yytext);
                    return NUMBER;
                }

[a-zA-Z_][a-zA-Z0-9_]*   {
                    Symbol *s;
                    s = lookup(yytext);
                    if (!s)
                        s = install(yytext, VAR, &zero);
                    yylval.sym = s;
                    return NAME;
                }

"="             { return '='; }
"\n"            { return '\n'; }
"+"             { return '+'; }
"-"             { return '-'; }
"*"             { return '*'; }
"/"             { return '/'; }
"^"             { return '^'; }
"("             { return '('; }
")"             { return ')'; }

.               { printf("carácter desconocido: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}
