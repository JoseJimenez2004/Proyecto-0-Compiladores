import tkinter as tk
from tkinter import font as tkfont
import math
import re
from functools import partial

class HOCInterpreter:
    """Implementación del intérprete HOC en Python"""
    def __init__(self):
        self.symbol_table = {}
        self.functions = {}
        self.init_symbols()
    
    def init_symbols(self):
        # Constantes predefinidas
        constants = {
            'PI': math.pi,
            'E': math.e,
            'GAMMA': 0.5772156649015328,
            'DEG': 180 / math.pi,
            'PHI': (1 + math.sqrt(5)) / 2
        }
        
        # Funciones matemáticas
        functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
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
        """Instala una variable o función en la tabla de símbolos"""
        if callable(value):
            self.functions[name] = value
        else:
            self.symbol_table[name] = value
    
    def lookup(self, name):
        """Busca un símbolo en la tabla"""
        if name in self.symbol_table:
            return ('VAR', self.symbol_table[name])
        elif name in self.functions:
            return ('FUNC', self.functions[name])
        return None
    
    def evaluate(self, expr):
        """Evalúa una expresión matemática"""
        try:
            # Manejar asignaciones (ej. x=5)
            if '=' in expr:
                var, expr = map(str.strip, expr.split('=', 1))
                result = self._evaluate_math(expr)
                self.install(var, result)
                return result
            
            return self._evaluate_math(expr)
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    def _evaluate_math(self, expr):
        """Evalúa una expresión matemática pura"""
        # Reemplazar constantes
        for name, value in self.symbol_table.items():
            expr = re.sub(rf'\b{name}\b', str(value), expr)
        
        # Reemplazar funciones (ej. sin(0.5))
        for func_name, func in self.functions.items():
            if func_name in expr:
                expr = re.sub(
                    fr'{func_name}\(([^)]+)\)',
                    lambda m: str(func(float(self._evaluate_math(m.group(1))))),
                    expr
                )
        
        # Reemplazar ^ con ** para potencia
        expr = expr.replace('^', '**')
        
        # Evaluar con seguridad
        allowed_names = {**self.symbol_table, **self.functions}
        code = compile(expr, "<string>", "eval")
        
        # Verificar nombres permitidos
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Nombre '{name}' no definido")
        
        return eval(code, {"__builtins__": {}}, allowed_names)

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica HOC-Python")
        self.root.geometry("1000x700")
        self.current_theme = "light"
        self.hoc = HOCInterpreter()
        self.setup_ui()
    
    def setup_ui(self):
        # Configuración de temas
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "text": "#333333",
                "button": "#e1e1e1",
                "highlight": "#4CAF50",
                "display": "white",
                "special": "#2196F3",
                "constants": "#9C27B0",
                "error": "#FF5722",
                "sidebar": "#e8e8e8",
                "border": "#cccccc"
            },
            "dark": {
                "bg": "#2d2d2d",
                "text": "#ffffff",
                "button": "#424242",
                "highlight": "#8BC34A",
                "display": "#1e1e1e",
                "special": "#1976D2",
                "constants": "#BA68C8",
                "error": "#FF7043",
                "sidebar": "#3d3d3d",
                "border": "#555555"
            }
        }

        # Frame principal con diseño horizontal
        self.main_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame para la calculadora (izquierda)
        self.calc_frame = tk.Frame(
            self.main_frame, 
            bg=self.themes[self.current_theme]["bg"],
            padx=10, 
            pady=10
        )
        self.calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para la información (derecha)
        self.sidebar_frame = tk.Frame(
            self.main_frame, 
            bg=self.themes[self.current_theme]["sidebar"],
            width=300,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=1
        )
        self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)  # Mantener el ancho fijo

        # Pantalla de resultados
        self.display = tk.Entry(
            self.calc_frame, 
            font=('Arial', 28), 
            bd=2, 
            relief=tk.FLAT,
            bg=self.themes[self.current_theme]["display"],
            fg=self.themes[self.current_theme]["text"], 
            justify="right", 
            insertbackground="white"
        )
        self.display.pack(fill=tk.X, pady=(0, 15), ipady=10)
        self.display.bind('<Return>', lambda e: self.calculate())
        self.display.bind('<Escape>', lambda e: self.display.delete(0, tk.END))

        # Frame para botones
        self.button_frame = tk.Frame(
            self.calc_frame, 
            bg=self.themes[self.current_theme]["bg"]
        )
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        # Botones
        self.create_buttons()

        # Panel de variables en el sidebar
        self.vars_frame = tk.LabelFrame(
            self.sidebar_frame,
            text=" Variables ",
            font=('Arial', 10, 'bold'),
            bg=self.themes[self.current_theme]["sidebar"],
            fg=self.themes[self.current_theme]["text"],
            relief=tk.RIDGE,
            bd=1
        )
        self.vars_frame.pack(fill=tk.X, pady=(0, 10))

        self.vars_text = tk.Text(
            self.vars_frame, 
            height=8, 
            font=('Consolas', 10), 
            bg=self.themes[self.current_theme]["display"],
            fg=self.themes[self.current_theme]["text"], 
            state="disabled",
            padx=5,
            pady=5,
            wrap=tk.NONE
        )
        self.vars_text.pack(fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para variables
        scroll_var = tk.Scrollbar(self.vars_text)
        scroll_var.pack(side=tk.RIGHT, fill=tk.Y)
        self.vars_text.config(yscrollcommand=scroll_var.set)
        scroll_var.config(command=self.vars_text.yview)

        # Historial en el sidebar
        self.history_frame = tk.LabelFrame(
            self.sidebar_frame,
            text=" Historial ",
            font=('Arial', 10, 'bold'),
            bg=self.themes[self.current_theme]["sidebar"],
            fg=self.themes[self.current_theme]["text"],
            relief=tk.RIDGE,
            bd=1
        )
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        self.history_text = tk.Text(
            self.history_frame, 
            height=15, 
            font=('Consolas', 10), 
            bg=self.themes[self.current_theme]["display"],
            fg=self.themes[self.current_theme]["text"], 
            state="disabled",
            padx=5,
            pady=5,
            wrap=tk.NONE
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para historial
        scroll_hist = tk.Scrollbar(self.history_text)
        scroll_hist.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scroll_hist.set)
        scroll_hist.config(command=self.history_text.yview)

        # Botón para limpiar historial
        clear_btn = tk.Button(
            self.sidebar_frame,
            text="Limpiar Historial",
            command=self.clear_history,
            bg=self.themes[self.current_theme]["error"],
            fg="white",
            font=('Arial', 10),
            bd=0
        )
        clear_btn.pack(fill=tk.X, pady=(5, 0))

        # Actualizar visualización inicial
        self.update_vars_display()

    def create_buttons(self):
        # Definición de botones organizados en grupos
        button_groups = [
            [
                ('7', '8', '9', '/', 'C'),
                ('4', '5', '6', '*', '⌫'),
                ('1', '2', '3', '-', '^'),
                ('0', '.', '=', '+', '±')
            ],
            [
                ('sin', 'cos', 'tan', '(', ')'),
                ('asin', 'acos', 'atan', 'PI', 'E'),
                ('log', 'log10', 'exp', 'sqrt', 'abs'),
                ('x++', 'x--', 'int', 'DEG', 'PHI'),
                ('floor', 'ceil', 'GAMMA', 'theme', '')
            ]
        ]

        # Crear frames para los grupos de botones
        num_frame = tk.Frame(
            self.button_frame, 
            bg=self.themes[self.current_theme]["bg"]
        )
        num_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        func_frame = tk.Frame(
            self.button_frame, 
            bg=self.themes[self.current_theme]["bg"]
        )
        func_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

        # Configurar pesos de las columnas
        self.button_frame.grid_columnconfigure(0, weight=3)
        self.button_frame.grid_columnconfigure(1, weight=2)
        self.button_frame.grid_rowconfigure(0, weight=1)

        # Crear botones numéricos
        for row_idx, row in enumerate(button_groups[0]):
            num_frame.grid_rowconfigure(row_idx, weight=1)
            for col_idx, text in enumerate(row):
                num_frame.grid_columnconfigure(col_idx, weight=1)
                self.create_button(num_frame, text, row_idx, col_idx)

        # Crear botones de funciones
        for row_idx, row in enumerate(button_groups[1]):
            func_frame.grid_rowconfigure(row_idx, weight=1)
            for col_idx, text in enumerate(row):
                if text:  # Saltar botones vacíos
                    func_frame.grid_columnconfigure(col_idx, weight=1)
                    self.create_button(func_frame, text, row_idx, col_idx)

    def create_button(self, parent, text, row, col):
        btn_font = ('Arial', 14, 'bold') if text not in {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'log10', 'exp', 'sqrt', 'abs', 'int', 'floor', 'ceil'} else ('Arial', 12)
        
        btn = tk.Button(
            parent, 
            text=text, 
            font=btn_font,
            command=lambda t=text: self.on_button_click(t),
            bg=self.get_button_color(text),
            fg=self.themes[self.current_theme]["text"],
            bd=0, 
            padx=5, 
            pady=5, 
            relief=tk.RAISED,
            activebackground=self.themes[self.current_theme]["highlight"],
            activeforeground="white"
        )
        btn.grid(
            row=row, 
            column=col, 
            sticky="nsew", 
            padx=2, 
            pady=2,
            ipadx=5,
            ipady=10
        )

    def get_button_color(self, text):
        theme = self.themes[self.current_theme]
        if text in {'C', '⌫', '±'}:
            return theme["error"]  # Rojo/naranja para acciones
        elif text in {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                     'log', 'log10', 'exp', 'sqrt', 'abs', 'int', 
                     'floor', 'ceil'}:
            return theme["special"]  # Azul para funciones
        elif text in {'PI', 'E', 'DEG', 'PHI', 'GAMMA'}:
            return theme["constants"]  # Púrpura para constantes
        elif text == '=':
            return theme["highlight"]  # Verde para igual
        elif text == 'theme':
            return "#607D8B"  # Gris azulado para tema
        else:
            return theme["button"]  # Gris para números/operadores

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
            # Insertar el texto al final con un espacio si es una función o constante
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
            result = self.hoc.evaluate(expr)
            output = f"{expr} = {result}"
            
            # Actualizar pantalla e historial
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.update_history(output)
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

    def clear_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state="disabled")

    def update_vars_display(self):
        self.vars_text.config(state="normal")
        self.vars_text.delete(1.0, tk.END)
        
        # Mostrar solo variables definidas por el usuario (excluyendo constantes predefinidas)
        user_vars = {k: v for k, v in self.hoc.symbol_table.items() 
                    if k not in {'PI', 'E', 'GAMMA', 'DEG', 'PHI'}}
        
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
        
        # Actualizar colores de todos los widgets
        self.main_frame.config(bg=theme["bg"])
        self.calc_frame.config(bg=theme["bg"])
        self.sidebar_frame.config(bg=theme["sidebar"])
        
        self.display.config(
            bg=theme["display"], 
            fg=theme["text"],
            insertbackground=theme["text"]
        )
        
        self.button_frame.config(bg=theme["bg"])
        
        self.vars_frame.config(
            bg=theme["sidebar"], 
            fg=theme["text"]
        )
        
        self.vars_text.config(
            bg=theme["display"], 
            fg=theme["text"]
        )
        
        self.history_frame.config(
            bg=theme["sidebar"], 
            fg=theme["text"]
        )
        
        self.history_text.config(
            bg=theme["display"], 
            fg=theme["text"]
        )
        
        # Actualizar botones
        for frame in [self.button_frame.winfo_children()[0], self.button_frame.winfo_children()[1]]:
            for button in frame.winfo_children():
                if isinstance(button, tk.Button):
                    text = button.cget("text")
                    button.config(
                        bg=self.get_button_color(text),
                        fg=theme["text"],
                        activebackground=theme["highlight"],
                        activeforeground="white"
                    )

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()