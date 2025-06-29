%{
#include "hoc.h"
#include "y.tab.h"
%}

%%
[ \t]   ;  /* Ignorar espacios */
[0-9]+(\.[0-9]*)? { yylval.val = atof(yytext); return NUMBER; }
"while"  return WHILE;
"if"     return IF;
"else"   return ELSE;
"print"  return PRINT;
">="     return GE;
"<="     return LE;
"=="     return EQ;
"!="     return NE;
">"      return GT;
"<"      return LT;
"&&"     return AND;
"||"     return OR;
[a-zA-Z][a-zA-Z0-9]* {
    yylval.sym = lookup(yytext);
    return VAR;
}
\n      return '\n';
.       return yytext[0];
%%