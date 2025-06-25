import tkinter as tk
from tkinter import font as tkfont
import math
import re
from functools import partial

class HOCInterpreter:
    """
    Intérprete HOC (Higher Order Calculator) que implementa:
    - Tabla de símbolos para variables
    - Funciones matemáticas
    - Evaluación de expresiones
    """
    
    def __init__(self):
        """Inicializa el intérprete con tablas de símbolos vacías"""
        self.symbol_table = {}  # Almacena variables y constantes (nombre: valor)
        self.functions = {}    # Almacena funciones (nombre: función)
        self.init_symbols()    # Carga símbolos predefinidos
    
    def init_symbols(self):
        """
        Inicializa constantes y funciones matemáticas predefinidas.
        Se ejecuta automáticamente al crear el intérprete.
        """
        # Constantes matemáticas importantes
        constants = {
            'PI': math.pi,  # π (pi)
            'E': math.e,     # Número de Euler
            'GAMMA': 0.5772156649015328,  # Constante de Euler-Mascheroni
            'DEG': 180 / math.pi,  # Conversión de radianes a grados
            'PHI': (1 + math.sqrt(5)) / 2  # Proporción áurea (φ)
        }
        
        # Funciones matemáticas estándar
        functions = {
            # Trigonometría
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            
            # Logaritmos y exponenciales
            'exp': math.exp,
            'log': math.log,     # Logaritmo natural
            'log10': math.log10, # Logaritmo base 10
            
            # Otras funciones
            'sqrt': math.sqrt,  # Raíz cuadrada
            'abs': abs,         # Valor absoluto
            'int': lambda x: int(x),  # Conversión a entero
            'floor': math.floor,  # Piso
            'ceil': math.ceil    # Techo
        }
        
        # Actualizar las tablas de símbolos
        self.symbol_table.update(constants)
        self.functions.update(functions)
    
    def install(self, name, value):
        """
        Instala una variable o función en la tabla de símbolos.
        
        Args:
            name (str): Nombre del símbolo
            value: Valor (puede ser número o función)
        """
        if callable(value):  # Si es una función
            self.functions[name] = value
        else:  # Si es una variable
            self.symbol_table[name] = value
    
    def lookup(self, name):
        """
        Busca un símbolo en las tablas.
        
        Args:
            name (str): Nombre del símbolo a buscar
            
        Returns:
            tuple: ('VAR', valor) o ('FUNC', función) o None si no existe
        """
        if name in self.symbol_table:
            return ('VAR', self.symbol_table[name])
        elif name in self.functions:
            return ('FUNC', self.functions[name])
        return None
    
    def evaluate(self, expr):
        """
        Evalúa una expresión matemática.
        Maneja asignaciones (x=5) y expresiones puras.
        
        Args:
            expr (str): Expresión a evaluar
            
        Returns:
            float/int: Resultado de la evaluación
            
        Raises:
            ValueError: Si hay error en la expresión
        """
        try:
            # Manejar asignaciones (ej. x=5)
            if '=' in expr:
                var, expr = map(str.strip, expr.split('=', 1))
                result = self._evaluate_math(expr)
                self.install(var, result)  # Guardar en tabla de símbolos
                return result
            
            return self._evaluate_math(expr)
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    def _evaluate_math(self, expr):
        """
        Evalúa una expresión matemática pura (sin asignaciones).
        Realiza sustituciones y transformaciones necesarias.
        
        Args:
            expr (str): Expresión matemática
            
        Returns:
            float/int: Resultado de la evaluación
        """
        # Reemplazar constantes por sus valores
        for name, value in self.symbol_table.items():
            expr = re.sub(rf'\b{name}\b', str(value), expr)
        
        # Reemplazar llamadas a funciones (ej. sin(0.5))
        for func_name, func in self.functions.items():
            if func_name in expr:
                expr = re.sub(
                    fr'{func_name}\(([^)]+)\)',
                    lambda m: str(func(float(self._evaluate_math(m.group(1))))),
                    expr
                )
        
        # Reemplazar ^ con ** para operaciones de potencia
        expr = expr.replace('^', '**')
        
        # Evaluar con seguridad (restringiendo acceso)
        allowed_names = {**self.symbol_table, **self.functions}
        code = compile(expr, "<string>", "eval")
        
        # Verificar que todos los nombres usados estén permitidos
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Nombre '{name}' no definido")
        
        return eval(code, {"__builtins__": {}}, allowed_names)

class ScientificCalculator:
    """
    Interfaz gráfica de la calculadora científica.
    Utiliza tkinter para la UI y HOCInterpreter para los cálculos.
    """
    
    def __init__(self, root):
        """
        Inicializa la calculadora.
        
        Args:
            root: Ventana principal de tkinter
        """
        self.root = root
        self.root.title("Calculadora Científica HOC-Python")
        self.root.geometry("1000x700")  # Tamaño inicial
        self.current_theme = "light"    # Tema inicial
        self.hoc = HOCInterpreter()    # Instancia del intérprete
        self.setup_ui()                # Configura la interfaz
    
    def setup_ui(self):
        """Configura todos los elementos de la interfaz gráfica."""
        # Definición de temas (light/dark mode)
        self.themes = {
            "light": {
                "bg": "#f0f0f0",       # Color de fondo
                "text": "#333333",      # Color de texto
                "button": "#e1e1e1",    # Color de botones normales
                "highlight": "#4CAF50", # Color de botón destacado
                "display": "white",     # Color del display
                "special": "#2196F3",   # Color para funciones especiales
                "constants": "#9C27B0", # Color para constantes
                "error": "#FF5722",     # Color para botones de error/acción
                "sidebar": "#e8e8e8",   # Color del panel lateral
                "border": "#cccccc"     # Color de bordes
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

        # Frame principal (contenedor horizontal)
        self.main_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame para la calculadora (lado izquierdo)
        self.calc_frame = tk.Frame(
            self.main_frame, 
            bg=self.themes[self.current_theme]["bg"],
            padx=10, 
            pady=10
        )
        self.calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para información (lado derecho)
        self.sidebar_frame = tk.Frame(
            self.main_frame, 
            bg=self.themes[self.current_theme]["sidebar"],
            width=300,  # Ancho fijo
            padx=10,
            pady=10,
            relief=tk.RIDGE,  # Borde con relieve
            bd=1  # Grosor del borde
        )
        self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)  # Mantiene el ancho fijo

        # Display (entrada de texto)
        self.display = tk.Entry(
            self.calc_frame, 
            font=('Arial', 28),  # Fuente grande
            bd=2, 
            relief=tk.FLAT,  # Borde plano
            bg=self.themes[self.current_theme]["display"],
            fg=self.themes[self.current_theme]["text"], 
            justify="right",  # Texto alineado a la derecha
            insertbackground="white"  # Color del cursor
        )
        self.display.pack(fill=tk.X, pady=(0, 15), ipady=10)  # Padding interno vertical
        # Bindings de teclado
        self.display.bind('<Return>', lambda e: self.calculate())  # Enter para calcular
        self.display.bind('<Escape>', lambda e: self.display.delete(0, tk.END))  # ESC para borrar

        # Frame para los botones
        self.button_frame = tk.Frame(
            self.calc_frame, 
            bg=self.themes[self.current_theme]["bg"]
        )
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        # Crear los botones
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

        # Área de texto para mostrar variables
        self.vars_text = tk.Text(
            self.vars_frame, 
            height=8, 
            font=('Consolas', 10),  # Fuente monoespaciada
            bg=self.themes[self.current_theme]["display"],
            fg=self.themes[self.current_theme]["text"], 
            state="disabled",  # Solo lectura
            padx=5,
            pady=5,
            wrap=tk.NONE  # Sin wrap de texto
        )
        self.vars_text.pack(fill=tk.BOTH, expand=True)

        # Scrollbar para variables
        scroll_var = tk.Scrollbar(self.vars_text)
        scroll_var.pack(side=tk.RIGHT, fill=tk.Y)
        self.vars_text.config(yscrollcommand=scroll_var.set)
        scroll_var.config(command=self.vars_text.yview)

        # Panel de historial
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

        # Área de texto para historial
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

        # Scrollbar para historial
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
            bd=0  # Sin borde
        )
        clear_btn.pack(fill=tk.X, pady=(5, 0))

        # Actualizar visualización inicial
        self.update_vars_display()

    def create_buttons(self):
        """Crea y organiza todos los botones de la calculadora."""
        # Definición de grupos de botones
        button_groups = [
            # Grupo 1: Botones numéricos y operadores básicos
            [
                ('7', '8', '9', '/', 'C'),  # Fila 1
                ('4', '5', '6', '*', '⌫'),   # Fila 2
                ('1', '2', '3', '-', '^'),   # Fila 3
                ('0', '.', '=', '+', '±')    # Fila 4
            ],
            # Grupo 2: Funciones científicas y constantes
            [
                ('sin', 'cos', 'tan', '(', ')'),          # Fila 1
                ('asin', 'acos', 'atan', 'PI', 'E'),      # Fila 2
                ('log', 'log10', 'exp', 'sqrt', 'abs'),   # Fila 3
                ('x++', 'x--', 'int', 'DEG', 'PHI'),      # Fila 4
                ('floor', 'ceil', 'GAMMA', 'theme', '')   # Fila 5
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
        self.button_frame.grid_columnconfigure(0, weight=3)  # Más ancho para números
        self.button_frame.grid_columnconfigure(1, weight=2)  # Menos ancho para funciones
        self.button_frame.grid_rowconfigure(0, weight=1)     # Solo una fila

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
        """Crea un botón individual con estilo apropiado."""
        # Configurar fuente según el tipo de botón
        if text not in {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                       'log', 'log10', 'exp', 'sqrt', 'abs', 'int', 
                       'floor', 'ceil'}:
            btn_font = ('Arial', 14, 'bold')  # Fuente grande para números
        else:
            btn_font = ('Arial', 12)  # Fuente más pequeña para funciones
            
        # Crear el botón
        btn = tk.Button(
            parent, 
            text=text, 
            font=btn_font,
            command=lambda t=text: self.on_button_click(t),
            bg=self.get_button_color(text),  # Color según tipo
            fg=self.themes[self.current_theme]["text"],
            bd=0,  # Sin borde
            padx=5, 
            pady=5, 
            relief=tk.RAISED,  # Efecto 3D
            activebackground=self.themes[self.current_theme]["highlight"],
            activeforeground="white"  # Color al hacer clic
        )
        # Posicionar el botón
        btn.grid(
            row=row, 
            column=col, 
            sticky="nsew",  # Expandir en todas direcciones
            padx=2, 
            pady=2,
            ipadx=5,  # Padding interno horizontal
            ipady=10  # Padding interno vertical
        )

    def get_button_color(self, text):
        """
        Devuelve el color apropiado para cada tipo de botón.
        
        Args:
            text (str): Texto del botón
            
        Returns:
            str: Código de color hexadecimal
        """
        theme = self.themes[self.current_theme]
        
        # Botones de acción/error (C, borrar, +/-)
        if text in {'C', '⌫', '±'}:
            return theme["error"]
        # Botones de funciones matemáticas
        elif text in {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                     'log', 'log10', 'exp', 'sqrt', 'abs', 'int', 
                     'floor', 'ceil'}:
            return theme["special"]
        # Botones de constantes
        elif text in {'PI', 'E', 'DEG', 'PHI', 'GAMMA'}:
            return theme["constants"]
        # Botón de igual
        elif text == '=':
            return theme["highlight"]
        # Botón de tema
        elif text == 'theme':
            return "#607D8B"  # Color fijo para tema
        # Botones numéricos y operadores básicos
        else:
            return theme["button"]

    def on_button_click(self, text):
        """
        Maneja el evento de clic en cualquier botón.
        
        Args:
            text (str): Texto del botón presionado
        """
        current = self.display.get()  # Contenido actual del display

        # Acciones especiales
        if text == 'C':  # Limpiar
            self.display.delete(0, tk.END)
        elif text == '⌫':  # Borrar último carácter
            self.display.delete(len(current) - 1, tk.END)
        elif text == '±':  # Cambiar signo
            if current and current[0] == '-':
                self.display.delete(0)
            else:
                self.display.insert(0, '-')
        elif text == '=':  # Calcular
            self.calculate()
        elif text == 'theme':  # Cambiar tema
            self.toggle_theme()
        elif text in {'x++', 'x--'}:  # Incremento/decremento
            self.handle_increment_decrement(text)
        else:
            # Insertar el texto del botón
            if text in self.hoc.functions or text in self.hoc.symbol_table:
                # Si es función, agregar paréntesis
                self.display.insert(tk.END, text + '(' if text in self.hoc.functions else text)
            else:
                self.display.insert(tk.END, text)

    def handle_increment_decrement(self, op):
        """
        Maneja las operaciones de incremento (x++) y decremento (x--).
        
        Args:
            op (str): Operación ('x++' o 'x--')
        """
        current = self.display.get().strip()
        if current:
            try:
                value = self.hoc.evaluate(current)
                increment = 1 if op == 'x++' else -1
                new_expr = f"{current}={value}+{increment}"
                self.display.delete(0, tk.END)
                self.display.insert(0, new_expr)
                self.calculate()  # Calcular inmediatamente
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, f"Error: {str(e)}")

    def calculate(self):
        """Evalúa la expresión actual y muestra el resultado."""
        expr = self.display.get().strip()
        if not expr:  # Si está vacío, no hacer nada
            return

        try:
            result = self.hoc.evaluate(expr)
            output = f"{expr} = {result}"  # Formato para historial
            
            # Actualizar pantalla
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            
            # Actualizar historial y variables
            self.update_history(output)
            self.update_vars_display()
        except Exception as e:
            # Mostrar error
            self.display.delete(0, tk.END)
            self.display.insert(0, f"Error: {str(e)}")
            self.update_history(f"Error en: {expr} => {str(e)}")

    def update_history(self, entry):
        """
        Agrega una entrada al historial.
        
        Args:
            entry (str): Texto a agregar al historial
        """
        self.history_text.config(state="normal")  # Habilitar edición
        self.history_text.insert(tk.END, entry + "\n")  # Agregar nueva línea
        self.history_text.config(state="disabled")  # Deshabilitar edición
        self.history_text.see(tk.END)  # Auto-scroll al final

    def clear_history(self):
        """Limpia todo el contenido del historial."""
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)  # Borrar desde inicio hasta fin
        self.history_text.config(state="disabled")

    def update_vars_display(self):
        """Actualiza el panel de variables con las actuales definidas."""
        self.vars_text.config(state="normal")
        self.vars_text.delete(1.0, tk.END)  # Limpiar contenido
        
        # Filtrar solo variables de usuario (excluir constantes predefinidas)
        user_vars = {k: v for k, v in self.hoc.symbol_table.items() 
                    if k not in {'PI', 'E', 'GAMMA', 'DEG', 'PHI'}}
        
        if user_vars:
            for var, value in user_vars.items():
                self.vars_text.insert(tk.END, f"{var} = {value}\n")
        else:
            self.vars_text.insert(tk.END, "No hay variables definidas")
        
        self.vars_text.config(state="disabled")

    def toggle_theme(self):
        """Cambia entre tema claro y oscuro."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.update_theme()

    def update_theme(self):
        """Actualiza todos los elementos de la UI con el tema actual."""
        theme = self.themes[self.current_theme]
        
        # Actualizar frames principales
        self.main_frame.config(bg=theme["bg"])
        self.calc_frame.config(bg=theme["bg"])
        self.sidebar_frame.config(bg=theme["sidebar"])
        
        # Actualizar display
        self.display.config(
            bg=theme["display"], 
            fg=theme["text"],
            insertbackground=theme["text"]  # Color del cursor
        )
        
        # Actualizar frame de botones
        self.button_frame.config(bg=theme["bg"])
        
        # Actualizar panel de variables
        self.vars_frame.config(bg=theme["sidebar"], fg=theme["text"])
        self.vars_text.config(bg=theme["display"], fg=theme["text"])
        
        # Actualizar panel de historial
        self.history_frame.config(bg=theme["sidebar"], fg=theme["text"])
        self.history_text.config(bg=theme["display"], fg=theme["text"])
        
        # Actualizar todos los botones
        for frame in [self.button_frame.winfo_children()[0], 
                     self.button_frame.winfo_children()[1]]:
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
    root = tk.Tk()  # Crear ventana principal
    app = ScientificCalculator(root)  # Iniciar aplicación
    root.mainloop()  # Bucle principal de la interfaz