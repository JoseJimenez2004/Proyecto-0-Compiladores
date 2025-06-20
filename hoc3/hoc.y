%{
#include "hoc.h"
#include <math.h>
#include <stdio.h>

extern int yylex();
void yyerror(char *);  // Declaración del prototipo para evitar warnings

Symbol *sym;
%}

%union {
    double val;
    Symbol *sym;
}

%token <val> NUMBER
%token <sym> NAME
%left '+' '-'
%left '*' '/'
%right '^'
%nonassoc UMINUS

%type <val> expr

%%

list:
    | list '\n'
    | list expr '\n'  { printf("\t%.8g\n", $2); }
    | list NAME '=' expr '\n' { $2->u.val = $4; }
    ;

expr:
      NUMBER             { $$ = $1; }
    | NAME               { $$ = $1->u.val; }
    | NAME '(' expr ')'  { $$ = $1->u.func($3); }
    | expr '+' expr      { $$ = $1 + $3; }
    | expr '-' expr      { $$ = $1 - $3; }
    | expr '*' expr      { $$ = $1 * $3; }
    | expr '/' expr      { $$ = $1 / $3; }
    | expr '^' expr      { $$ = pow($1, $3); }
    | '-' expr %prec UMINUS { $$ = -$2; }
    | '(' expr ')'       { $$ = $2; }
    ;

%%

int main(void) {
    return yyparse();
}

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
