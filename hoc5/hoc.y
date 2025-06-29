%{
#include "hoc.h"
#include <math.h>
%}

%union {
    double val;
    Symbol *sym;
}

%token <val> NUMBER
%token <sym> VAR
%token WHILE IF ELSE PRINT
%token GE LE EQ NE GT LT AND OR

%type <val> expr cond

%right '='
%left AND OR
%left GE LE EQ NE GT LT
%left '+' '-'
%left '*' '/' '%'
%right UNARYMINUS

%%

prog:   /* vacío */
    | prog stmt '\n'
    ;

stmt:   expr          { printf("\t%.8g\n", $1); }
    | PRINT expr     { printf("\t%.8g\n", $2); }
    | VAR '=' expr   { $1->u.val = $3; }
    | WHILE '(' cond ')' stmt { /* Generar código para while */ }
    | IF '(' cond ')' stmt %prec IF
    | IF '(' cond ')' stmt ELSE stmt
    | '{' stmtlist '}'
    ;

cond:   expr          { $$ = $1 != 0.0; }
    | cond AND cond   { $$ = $1 && $3; }
    | cond OR cond    { $$ = $1 || $3; }
    | expr GT expr    { $$ = $1 > $3; }
    | expr GE expr    { $$ = $1 >= $3; }
    | expr LT expr    { $$ = $1 < $3; }
    | expr LE expr    { $$ = $1 <= $3; }
    | expr EQ expr    { $$ = $1 == $3; }
    | expr NE expr    { $$ = $1 != $3; }
    ;

expr:   NUMBER        { $$ = $1; }
    | VAR            { $$ = $1->u.val; }
    | expr '+' expr   { $$ = $1 + $3; }
    | expr '-' expr   { $$ = $1 - $3; }
    | expr '*' expr   { $$ = $1 * $3; }
    | expr '/' expr   { $$ = $1 / $3; }
    | '-' expr %prec UNARYMINUS { $$ = -$2; }
    | '(' expr ')'    { $$ = $2; }
    ;