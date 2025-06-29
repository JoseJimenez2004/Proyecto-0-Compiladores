#include "hoc.h"
#include <math.h>

static double mathfunc(double (*f)(double), double arg) {
    return (*f)(arg);
}

double Pow(double x, double y) { return pow(x, y); }
double Sqrt(double x) { return sqrt(x); }

void initmath() {
    addfunc("sqrt", Sqrt);
    addfunc("pow", Pow);
}