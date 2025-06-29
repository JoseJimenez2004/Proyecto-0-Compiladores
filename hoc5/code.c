#include "hoc.h"

int pc = 0;  // Contador de programa
int code[1000];  // Código intermedio

void gen(int op) {
    code[pc++] = op;
}

void execute(int start) {
    for (int i = start; i < pc; i++) {
        switch (code[i]) {
            case '+': push(pop() + pop()); break;
            case '*': push(pop() * pop()); break;
            // ... otros operadores
        }
    }
}