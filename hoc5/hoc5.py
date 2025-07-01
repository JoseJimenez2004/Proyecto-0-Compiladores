import tkinter as tk
from tkinter import font as tkfont
import math
import re

class HOCInterpreter:
    def __init__(self):
        self.symbol_table = {}
        self.functions = {}
        self.stack = []
        self.print_output = []  # Para almacenar los resultados de print
        self.init_symbols()

    def init_symbols(self):
        constants = {
            'PI': math.pi,
            'E': math.e,
            'GAMMA': 0.5772156649015328,
            'DEG': 180 / math.pi,
            'PHI': (1 + math.sqrt(5)) / 2
        }

        functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'log': math.log,
            'log10': math.log10,
            'sqrt': math.sqrt,
            'abs': abs,
            'int': int,
            'floor': math.floor,
            'ceil': math.ceil
        }

        self.symbol_table.update(constants)
        self.functions.update(functions)

    def parse_and_compile(self, expr):
        # Tokenizador mejorado que maneja bloques anidados
        tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*\+\+|'
                          r'[A-Za-z_][A-Za-z0-9_]*|'
                          r'[0-9]+(?:\.[0-9]*)?|'
                          r'==|!=|<=|>=|&&|\|\||[(){};=<>+\-*/%^]|\S+', 
                          expr.replace('\n', ' '))
        code = []
        i = 0
        n = len(tokens)

        def parse_expr():
            nonlocal i
            if i >= n:
                return
                
            token = tokens[i]
            if re.fullmatch(r'[0-9]+(?:\.[0-9]*)?', token):
                code.append(('PUSH', float(token)))
                i += 1
            elif token in self.symbol_table:
                code.append(('LOAD', token))
                i += 1
            elif token in self.functions:
                func = token
                i += 1
                if i < n and tokens[i] == '(':
                    i += 1
                    parse_expr()
                    if i < n and tokens[i] == ')':
                        i += 1
                    code.append(('CALL', func))
            elif token.endswith('++'):
                var = token[:-2]
                code.append(('LOAD', var))
                code.append(('PUSH', 1))
                code.append(('+',))
                code.append(('STORE', var))
                i += 1
            elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token):
                code.append(('LOAD', token))
                i += 1
            elif token == '(':
                i += 1
                parse_expr()
                if i < n and tokens[i] == ')':
                    i += 1

        def parse_comparison():
            nonlocal i
            parse_expr()
            if i < n:
                op = tokens[i]
                if op in ('>', '<', '==', '!=', '>=', '<='):
                    i += 1
                    parse_expr()
                    code.append((op.upper(),))

        while i < n:
            token = tokens[i]

            if token == 'if':
                i += 1
                parse_comparison()
                jz_index = len(code)
                code.append(('JZ', None))
                if i < n and tokens[i] == '{':
                    i += 1
                    brace_count = 1
                    body_tokens = []
                    while i < n and brace_count > 0:
                        if tokens[i] == '{':
                            brace_count += 1
                        elif tokens[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                break
                        body_tokens.append(tokens[i])
                        i += 1
                    i += 1
                    body_code = self.parse_and_compile(' '.join(body_tokens))
                    code.extend(body_code)
                jmp_index = len(code)
                code.append(('JMP', None))
                code[jz_index] = ('JZ', len(code))
                if i < n and tokens[i] == 'else':
                    i += 1
                    if i < n and tokens[i] == '{':
                        i += 1
                        brace_count = 1
                        else_body_tokens = []
                        while i < n and brace_count > 0:
                            if tokens[i] == '{':
                                brace_count += 1
                            elif tokens[i] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    break
                            else_body_tokens.append(tokens[i])
                            i += 1
                        i += 1
                        code.extend(self.parse_and_compile(' '.join(else_body_tokens)))
                code[jmp_index] = ('JMP', len(code))

            elif token == 'while':
                i += 1
                cond_start = len(code)
                parse_comparison()
                jz_index = len(code)
                code.append(('JZ', None))
                if i < n and tokens[i] == '{':
                    i += 1
                    brace_count = 1
                    body_tokens = []
                    while i < n and brace_count > 0:
                        if tokens[i] == '{':
                            brace_count += 1
                        elif tokens[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                break
                        body_tokens.append(tokens[i])
                        i += 1
                    i += 1
                    code.extend(self.parse_and_compile(' '.join(body_tokens)))
                code.append(('JMP', cond_start))
                code[jz_index] = ('JZ', len(code))

            elif token == 'print':
                i += 1
                parse_expr()
                code.append(('PRINT',))
            elif token == '=':
                var = tokens[i - 1]
                i += 1
                parse_expr()
                code.append(('STORE', var))
            elif token == ';':
                i += 1
            else:
                parse_expr()

        return code

    def run(self, code):
        self.stack = []
        self.print_output = []  # Reiniciar la salida de print
        pc = 0
        max_iterations = 100000
        iteration_count = 0
        
        while pc < len(code) and iteration_count < max_iterations:
            iteration_count += 1
            instr = code[pc]
            op = instr[0]

            if op == 'PUSH':
                self.stack.append(instr[1])

            elif op == 'LOAD':
                self.stack.append(self.symbol_table.get(instr[1], 0))

            elif op == 'STORE':
                self.symbol_table[instr[1]] = self.stack.pop()

            elif op == 'PRINT':
                self.print_output.append(str(self.stack[-1] if self.stack else ''))

            elif op == 'JZ':
                if not self.stack.pop():
                    pc = instr[1]
                    continue

            elif op == 'JMP':
                pc = instr[1]
                continue

            elif op == '+':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a + b)

            elif op == '-':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a - b)

            elif op == '*':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a * b)

            elif op == '/':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a / b)

            elif op == '>':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(float(a > b))

            elif op == '<':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(float(a < b))

            elif op == '==':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(float(a == b))

            elif op == '!=':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(float(a != b))

            elif op == '>=':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(float(a >= b))

            elif op == '<=':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(float(a <= b))

            elif op == 'CALL':
                val = self.stack.pop()
                self.stack.append(self.functions[instr[1]](val))

            pc += 1

        if iteration_count >= max_iterations:
            raise RuntimeError("Se excedió el límite de iteraciones (posible bucle infinito)")

        return self.stack[-1] if self.stack else None


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica HOC5")
        self.current_theme = "light"
        self.hoc = HOCInterpreter()
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.themes = {
            "light": {
                "bg": "#f4f6f8",
                "text": "#202124",
                "button": "#e0e0e0",
                "highlight": "#1e88e5",
                "display": "#ffffff",
                "special": "#42a5f5",
                "constants": "#ab47bc",
                "error": "#ef5350",
                "sidebar": "#fafafa",
                "border": "#dcdcdc"
            },
            "dark": {
                "bg": "#263238",
                "text": "#eceff1",
                "button": "#37474f",
                "highlight": "#26c6da",
                "display": "#1c1c1c",
                "special": "#4dd0e1",
                "constants": "#ce93d8",
                "error": "#ef9a9a",
                "sidebar": "#37474f",
                "border": "#546e7a"
            }
        }

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        self.display = tk.Text(self.main_frame, font=('Consolas', 16), relief=tk.FLAT, bd=8, height=5)
        self.display.pack(fill=tk.X, pady=(0, 20))
        self.display.bind('<Return>', lambda e: self.calculate())
        self.display.bind('<Escape>', lambda e: self.display.delete('1.0', tk.END))

        self.eval_button = tk.Button(self.main_frame, text="Evaluar", font=('Arial', 14, 'bold'),
                                    command=self.calculate, bg=self.themes["light"]["highlight"], 
                                    fg="white", bd=0, relief=tk.FLAT)
        self.eval_button.pack(fill=tk.X, pady=(0, 10))

        self.button_area = tk.Frame(self.main_frame)
        self.button_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_frame, width=340)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.vars_label = tk.Label(self.sidebar, text="Variables", font=('Arial', 14, 'bold'))
        self.vars_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.vars_text = tk.Text(self.sidebar, height=8, font=('Consolas', 11), wrap=tk.NONE, state='disabled')
        self.vars_text.pack(fill=tk.X, padx=10, pady=5)

        self.stack_label = tk.Label(self.sidebar, text="Pila (stack)", font=('Arial', 14, 'bold'))
        self.stack_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.stack_text = tk.Text(self.sidebar, height=8, font=('Consolas', 11), wrap=tk.NONE, state='disabled')
        self.stack_text.pack(fill=tk.X, padx=10, pady=5)

        self.history_label = tk.Label(self.sidebar, text="Historial", font=('Arial', 14, 'bold'))
        self.history_label.pack(anchor="w", padx=10, pady=(20, 0))

        self.history_text = tk.Text(self.sidebar, height=15, font=('Consolas', 11), wrap=tk.NONE, state='disabled')
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '⌫'],
            ['1', '2', '3', '-', '^'],
            ['0', '.', '=', '+', '±'],
            ['sin', 'cos', 'tan', '(', ')'],
            ['log', 'log10', 'exp', 'sqrt', 'abs'],
            ['int', 'floor', 'ceil', 'DEG', 'PHI'],
            ['theme', '', '', '', '']
        ]
        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                if text:
                    self.create_button(self.button_area, text, r, c)

    def create_button(self, parent, text, row, col):
        theme = self.themes[self.current_theme]
        btn = tk.Button(parent, text=text, font=('Arial', 14, 'bold'),
                        command=lambda t=text: self.on_button_click(t),
                        bg=self.get_button_color(text), fg=theme["text"],
                        bd=0, relief=tk.FLAT,
                        activebackground=theme["highlight"], activeforeground="#ffffff")
        btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6, ipadx=10, ipady=12)
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)

    def get_button_color(self, text):
        theme = self.themes[self.current_theme]
        if text in {'C', '⌫', '±'}:
            return theme["error"]
        elif text in {'sin', 'cos', 'tan', 'log', 'log10', 'exp', 'sqrt', 'abs', 'int', 'floor', 'ceil'}:
            return theme["special"]
        elif text in {'PI', 'E', 'DEG', 'PHI', 'GAMMA'}:
            return theme["constants"]
        elif text == '=':
            return theme["highlight"]
        elif text == 'theme':
            return "#607D8B"
        else:
            return theme["button"]

    def on_button_click(self, text):
        if text == 'C':
            self.display.delete('1.0', tk.END)
        elif text == '⌫':
            self.display.delete('insert-1c', tk.END)
        elif text == '±':
            self.display.insert(tk.END, '-')
        elif text == '=':
            self.calculate()
        elif text == 'theme':
            self.toggle_theme()
        else:
            if text in self.hoc.functions:
                self.display.insert(tk.END, text + '(')
            else:
                self.display.insert(tk.END, text)

    def calculate(self):
        expr = self.display.get('1.0', tk.END).strip()
        if not expr:
            return
        
        try:
            # Procesar todo el código como un solo bloque
            code = self.hoc.parse_and_compile(expr)
            final_result = self.hoc.run(code)
            
            # Mostrar los prints en el display
            self.display.delete('1.0', tk.END)
            if hasattr(self.hoc, 'print_output') and self.hoc.print_output:
                output = "\n".join(self.hoc.print_output)
                self.display.insert('1.0', output)
            elif final_result is not None:
                self.display.insert('1.0', str(final_result))
            
            self.update_history(expr)
            self.update_vars_display()
            self.update_stack_display()
            
        except Exception as e:
            self.display.delete('1.0', tk.END)
            self.display.insert('1.0', f"Error: {str(e)}")
            self.update_history(f"Error en: {expr} => {str(e)}")

    def update_history(self, entry):
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state="disabled")
        self.history_text.see(tk.END)

    def update_vars_display(self):
        self.vars_text.config(state="normal")
        self.vars_text.delete(1.0, tk.END)
        user_vars = {k: v for k, v in self.hoc.symbol_table.items()
                     if k not in {'PI', 'E', 'GAMMA', 'DEG', 'PHI'}}
        if user_vars:
            for var, value in user_vars.items():
                self.vars_text.insert(tk.END, f"{var} = {value}\n")
        else:
            self.vars_text.insert(tk.END, "No hay variables definidas\n")
        self.vars_text.config(state="disabled")

    def update_stack_display(self):
        self.stack_text.config(state="normal")
        self.stack_text.delete(1.0, tk.END)
        if self.hoc.stack:
            for val in reversed(self.hoc.stack):
                self.stack_text.insert(tk.END, f"{val}\n")
        else:
            self.stack_text.insert(tk.END, "(vacía)\n")
        self.stack_text.config(state="disabled")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.main_frame.config(bg=theme["bg"])
        self.button_area.config(bg=theme["bg"])
        self.sidebar.config(bg=theme["sidebar"])
        self.eval_button.config(bg=theme["highlight"])

        self.display.config(bg=theme["display"], fg=theme["text"], insertbackground=theme["text"])

        self.vars_label.config(bg=theme["sidebar"], fg=theme["text"])
        self.vars_text.config(bg=theme["display"], fg=theme["text"])

        self.stack_label.config(bg=theme["sidebar"], fg=theme["text"])
        self.stack_text.config(bg=theme["display"], fg=theme["text"])

        self.history_label.config(bg=theme["sidebar"], fg=theme["text"])
        self.history_text.config(bg=theme["display"], fg=theme["text"])

        for widget in self.button_area.winfo_children():
            if isinstance(widget, tk.Button):
                text = widget.cget("text")
                widget.config(bg=self.get_button_color(text), fg=theme["text"],
                              activebackground=theme["highlight"], activeforeground="#ffffff")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.geometry("1280x800")
    root.mainloop()