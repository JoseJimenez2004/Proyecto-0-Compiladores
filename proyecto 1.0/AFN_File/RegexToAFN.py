from .AFN import AFN

class RegexToAFN:
    def __init__(self, regex):
        self.regex = regex
        self.output_stack = []
        self.operator_stack = []
        self.operators = {'*', '+', '?', '|', '&'}
        self.precedence = {'*': 3, '+': 3, '?': 3, '&': 2, '|': 1}

    def afn_from_regex(self, token_id=None):
        tokens = self.tokenize(self.regex)
        for token in tokens:
            if token.startswith("[") and token.endswith("]"):  # Es un rango de caracteres
                char_range = token[1:-1].split('-')
                if len(char_range) == 2:
                    self.output_stack.append(AFN.afn_basico(char_range))  # Rango como ['0', '9']
                else:
                    raise ValueError(f"Rango de caracteres no válido: {token}")
            elif token.startswith('_'):  # Si el token es un símbolo escapado
                self.output_stack.append(AFN.afn_basico(token[1:]))  # Agrega sin el prefijo '_'
            elif token.isalnum() or token == '.':  # Es un símbolo o punto literal
                self.output_stack.append(AFN.afn_basico(token))
            elif token == '(':
                self.operator_stack.append(token)
            elif token == ')':
                while self.operator_stack and self.operator_stack[-1] != '(':
                    self.process_operator()
                if not self.operator_stack:
                    raise ValueError("Expresión inválida: falta un paréntesis de apertura.")
                self.operator_stack.pop()  # Quita '('
            elif token in self.operators:
                # Verifica la precedencia antes de agregar el operador a la pila
                while (self.operator_stack and
                       self.operator_stack[-1] in self.operators and
                       self.precedence[self.operator_stack[-1]] >= self.precedence[token]):
                    self.process_operator()
                self.operator_stack.append(token)

        # Procesa los operadores restantes
        while self.operator_stack:
            self.process_operator()

        # La pila final debe contener un solo AFN
        if len(self.output_stack) != 1:
            raise ValueError("Expresión inválida: falta un operando.")

        # AFN final y asignación del token al estado de aceptación
        afn_resultante = self.output_stack.pop()
        if token_id is not None:
            for estado in afn_resultante.edos_acept:
                if estado.es_aceptacion:
                    estado.token = token_id

        return afn_resultante

    def process_operator(self):
        if not self.operator_stack:
            raise ValueError("Error: falta operador en la expresión.")

        op = self.operator_stack.pop()

        # Operadores unarios
        if op in {'*', '+', '?'}:
            if not self.output_stack:
                raise ValueError(f"Error en la expresión: operador '{op}' sin operando previo.")
            afn = self.output_stack.pop()
            if op == '*':
                self.output_stack.append(afn.cerradura())
            elif op == '+':
                self.output_stack.append(afn.cerradura())  # Aplica cerradura positiva
            elif op == '?':
                self.output_stack.append(afn.opcional())
        # Operadores binarios
        elif op in {'|', '&'}:
            if len(self.output_stack) < 2:
                raise ValueError(f"Error en la expresión: operador '{op}' necesita dos operandos.")
            afn2 = self.output_stack.pop()
            afn1 = self.output_stack.pop()
            if op == '|':
                self.output_stack.append(afn1.unir(afn2))
            elif op == '&':
                self.output_stack.append(afn1.concatenar(afn2))

    def tokenize(self, regex):
        tokens = []
        i = 0
        while i < len(regex):
            if regex[i] == '!':  # Detecta el carácter de escape
                if i + 1 < len(regex):  # Verifica que haya un siguiente carácter
                    tokens.append('_' + regex[i + 1])  # Agrega el siguiente carácter como literal, con prefijo '_'
                    i += 2  # Salta al siguiente después del carácter escapado
                else:
                    raise ValueError("Secuencia de escape incompleta en la expresión regular.")
            elif regex[i] == '[':  # Detecta rangos de caracteres
                end = regex.index(']', i)
                tokens.append(regex[i:end + 1])  # Rango completo como un solo token
                i = end + 1
            elif regex[i] == ' ':  # Detecta espacios vacíos explícitamente
                tokens.append('_SPACE_')  # Representa el espacio con un token especial
                i += 1
            elif regex[i:i + 2] == 'ε':  # Detecta el símbolo ε explícitamente
                tokens.append('_EPSILON_')  # Representa ε con un token especial
                i += 2
            elif regex[i] in self.operators or regex[i] in '()':
                tokens.append(regex[i])
                i += 1
            else:
                tokens.append(regex[i])
                i += 1
        return self.insert_concat(tokens)

    def insert_concat(self, tokens):
        output = []
        for i, token in enumerate(tokens):
            output.append(token)
            # Inserta '&' cuando es necesario entre operandos y operadores
            if i + 1 < len(tokens):
                if (token not in '(|' and tokens[i + 1] not in ')|*+?'):
                    output.append('&')
        return output
