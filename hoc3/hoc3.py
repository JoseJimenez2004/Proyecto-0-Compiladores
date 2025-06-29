import tkinter as tk
from tkinter import font as tkfont
import math
import re

class HOCInterpreter:
    def __init__(self):
        self.symbol_table = {}
        self.functions = {}
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
            'int': lambda x: int(x),
            'floor': math.floor,
            'ceil': math.ceil
        }

        self.symbol_table.update(constants)
        self.functions.update(functions)

    def install(self, name, value):
        if callable(value):
            self.functions[name] = value
        else:
            self.symbol_table[name] = value

    def lookup(self, name):
        if name in self.symbol_table:
            return ('VAR', self.symbol_table[name])
        elif name in self.functions:
            return ('FUNC', self.functions[name])
        return None

    def evaluate(self, expr):
        try:
            if '=' in expr:
                var, expr = map(str.strip, expr.split('=', 1))
                result = self._evaluate_math(expr)
                self.install(var, result)
                return result
            return self._evaluate_math(expr)
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")

    def _evaluate_math(self, expr):
        for name, value in self.symbol_table.items():
            expr = re.sub(rf'\b{name}\b', str(value), expr)

        for func_name, func in self.functions.items():
            if func_name in expr:
                expr = re.sub(
                    fr'{func_name}\(([^)]+)\)',
                    lambda m: str(func(float(self._evaluate_math(m.group(1))))),
                    expr
                )

        expr = expr.replace('^', '**')

        allowed_names = {**self.symbol_table, **self.functions}
        code = compile(expr, "<string>", "eval")

        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Nombre '{name}' no definido")

        return eval(code, {"__builtins__": {}}, allowed_names)

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica HOC-Python")
        self.root.geometry("1280x800")
        self.current_theme = "light"
        self.hoc = HOCInterpreter()
        self.setup_ui()

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

        theme = self.themes[self.current_theme]
        self.main_frame = tk.Frame(self.root, bg=theme["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        self.display = tk.Entry(self.main_frame, font=('Consolas', 32), bg=theme["display"],
                                fg=theme["text"], insertbackground=theme["text"],
                                relief=tk.FLAT, bd=8, justify='left')
        self.display.pack(fill=tk.X, pady=(0, 20), ipady=16)
        self.display.bind('<Return>', lambda e: self.calculate())
        self.display.bind('<Escape>', lambda e: self.display.delete(0, tk.END))

        self.button_area = tk.Frame(self.main_frame, bg=theme["bg"])
        self.button_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_frame, bg=theme["sidebar"], width=340)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.vars_label = tk.Label(self.sidebar, text="Variables", font=('Arial', 14, 'bold'),
                                   bg=theme["sidebar"], fg=theme["text"])
        self.vars_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.vars_text = tk.Text(self.sidebar, height=10, font=('Consolas', 11), wrap=tk.NONE,
                                 bg=theme["display"], fg=theme["text"], state='disabled')
        self.vars_text.pack(fill=tk.X, padx=10, pady=5)

        self.history_label = tk.Label(self.sidebar, text="Historial", font=('Arial', 14, 'bold'),
                                      bg=theme["sidebar"], fg=theme["text"])
        self.history_label.pack(anchor="w", padx=10, pady=(20, 0))

        self.history_text = tk.Text(self.sidebar, height=15, font=('Consolas', 11), wrap=tk.NONE,
                                    bg=theme["display"], fg=theme["text"], state='disabled')
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.create_buttons()
        self.update_vars_display()

    def create_buttons(self):
        buttons = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '⌫'],
            ['1', '2', '3', '-', '^'],
            ['0', '.', '=', '+', '±'],
            ['sin', 'cos', 'tan', '(', ')'],
            ['log', 'log10', 'exp', 'sqrt', 'abs'],
            ['x++', 'x--', 'int', 'DEG', 'PHI'],
            ['floor', 'ceil', 'GAMMA', 'theme', '']
        ]
        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                if text:
                    self.create_button(self.button_area, text, r, c)

    def create_button(self, parent, text, row, col):
        theme = self.themes[self.current_theme]
        btn = tk.Button(parent, text=text, font=('Arial', 14, 'bold'), command=lambda t=text: self.on_button_click(t),
                        bg=self.get_button_color(text), fg=theme["text"], bd=0,
                        relief=tk.FLAT, activebackground=theme["highlight"], activeforeground="#ffffff")
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
        current = self.display.get()
        if text == 'C':
            self.display.delete(0, tk.END)
        elif text == '⌫':
            self.display.delete(len(current) - 1, tk.END)
        elif text == '±':
            if current and current[0] == '-':
                self.display.delete(0)
            else:
                self.display.insert(0, '-')
        elif text == '=':
            self.calculate()
        elif text == 'theme':
            self.toggle_theme()
        elif text in {'x++', 'x--'}:
            self.handle_increment_decrement(text)
        else:
            if text in self.hoc.functions or text in self.hoc.symbol_table:
                self.display.insert(tk.END, text + '(' if text in self.hoc.functions else text)
            else:
                self.display.insert(tk.END, text)

    def handle_increment_decrement(self, op):
        current = self.display.get().strip()
        if current:
            try:
                value = self.hoc.evaluate(current)
                increment = 1 if op == 'x++' else -1
                new_expr = f"{current}={value}+{increment}"
                self.display.delete(0, tk.END)
                self.display.insert(0, new_expr)
                self.calculate()
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, f"Error: {str(e)}")

    def calculate(self):
        expr = self.display.get().strip()
        if not expr:
            return
        try:
            results = []
            for part in expr.split(';'):
                part = part.strip()
                if part:
                    result = self.hoc.evaluate(part)
                    results.append(f"{part} = {result}")
            if results:
                last_result = results[-1].split('=')[-1].strip()
                self.display.delete(0, tk.END)
                self.display.insert(0, last_result)
                for entry in results:
                    self.update_history(entry)
                self.update_vars_display()
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, f"Error: {str(e)}")
            self.update_history(f"Error en: {expr} => {str(e)}")

    def update_history(self, entry):
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state="disabled")
        self.history_text.see(tk.END)

    def update_vars_display(self):
        self.vars_text.config(state="normal")
        self.vars_text.delete(1.0, tk.END)
        user_vars = {k: v for k, v in self.hoc.symbol_table.items() if k not in {'PI', 'E', 'GAMMA', 'DEG', 'PHI'}}
        if user_vars:
            for var, value in user_vars.items():
                self.vars_text.insert(tk.END, f"{var} = {value}\n")
        else:
            self.vars_text.insert(tk.END, "No hay variables definidas")
        self.vars_text.config(state="disabled")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.update_theme()

    def update_theme(self):
        theme = self.themes[self.current_theme]
        self.main_frame.config(bg=theme["bg"])
        self.button_area.config(bg=theme["bg"])
        self.sidebar.config(bg=theme["sidebar"])
        self.display.config(bg=theme["display"], fg=theme["text"], insertbackground=theme["text"])
        self.vars_label.config(bg=theme["sidebar"], fg=theme["text"])
        self.vars_text.config(bg=theme["display"], fg=theme["text"])
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
    root.mainloop()
