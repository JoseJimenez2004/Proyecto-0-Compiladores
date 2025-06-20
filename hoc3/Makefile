CC = gcc
LEX = lex
YACC = yacc

CFLAGS = -c
LDFLAGS = -lm

OBJ = y.tab.o lex.yy.o symbol.o init.o math.o

all: hoc3

hoc3: $(OBJ)
	$(CC) -o hoc3 $(OBJ) $(LDFLAGS)

y.tab.o: hoc.y
	$(YACC) -d hoc.y
	$(CC) $(CFLAGS) y.tab.c

lex.yy.o: hoc.l
	$(LEX) hoc.l
	$(CC) $(CFLAGS) lex.yy.c

symbol.o: symbol.c hoc.h
	$(CC) $(CFLAGS) symbol.c

init.o: init.c hoc.h
	$(CC) $(CFLAGS) init.c

math.o: math.c hoc.h
	$(CC) $(CFLAGS) math.c

clean:
	rm -f *.o hoc3 y.tab.c y.tab.h lex.yy.c
