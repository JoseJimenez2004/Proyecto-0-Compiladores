import tkinter as tk
from tkinter import messagebox, ttk
import os

class AFN:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.estado_inicial = 0
        self.estado_final = 1
        self.transiciones = [(0, simbolo, 1)]

    def mostrar(self):
        return f"AFN con símbolo: {self.simbolo}\nEstado inicial: {self.estado_inicial}\nEstado final: {self.estado_final}\nTransiciones: {self.transiciones}"

    def guardar_en_archivo(self, nombre_archivo):
        if not os.path.exists('autbasic'):
            os.makedirs('autbasic')
        with open(f'autbasic/{nombre_archivo}.txt', 'w') as archivo:
            archivo.write(self.mostrar())

def listar_afns():
    if not os.path.exists('autbasic'):
        messagebox.showinfo("Información", "No hay autómatas guardados.")
        return
    archivos = os.listdir('autbasic')
    if not archivos:
        messagebox.showinfo("Información", "No hay autómatas guardados.")
        return
    lista_afns = "\n".join(archivos)
    messagebox.showinfo("Autómatas Guardados", f"Autómatas guardados:\n{lista_afns}")

def crear_afn():
    simbolo = simbolo_entry.get()
    if not simbolo:
        messagebox.showwarning("Entrada inválida", "Por favor, ingrese un símbolo.")
        return
    global afn
    afn = AFN(simbolo)
    resultado_label.config(text=afn.mostrar(), fg="white")

def guardar_afn():
    if not afn:
        messagebox.showwarning("Error", "No hay un AFN creado para guardar.")
        return
    nombre_archivo = archivo_entry.get()
    if not nombre_archivo:
        messagebox.showwarning("Entrada inválida", "Ingrese un nombre para el archivo.")
        return
    afn.guardar_en_archivo(nombre_archivo)
    messagebox.showinfo("Éxito", f"Autómata guardado en autbasic/{nombre_archivo}.txt")

def mostrar_crear_afn():
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    tk.Label(content_frame, text="Crear AFN Básico", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50").pack(pady=10)
    
    tk.Label(content_frame, text="Símbolo:", fg="white", bg="#2C3E50").pack()
    global simbolo_entry
    simbolo_entry = tk.Entry(content_frame, width=25, font=("Arial", 12))
    simbolo_entry.pack(pady=5)
    
    tk.Button(content_frame, text="Crear AFN", command=crear_afn, bg="#3498DB", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(pady=5)
    
    tk.Label(content_frame, text="Nombre del archivo:", fg="white", bg="#2C3E50").pack()
    global archivo_entry
    archivo_entry = tk.Entry(content_frame, width=25, font=("Arial", 12))
    archivo_entry.pack(pady=5)
    
    button_frame = tk.Frame(content_frame, bg="#2C3E50")
    button_frame.pack(pady=5)
    
    tk.Button(button_frame, text="Guardar AFN", command=guardar_afn, bg="#E74C3C", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(side="left", padx=5)
    tk.Button(button_frame, text="Listar AFN's", command=listar_afns, bg="#F39C12", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(side="right", padx=5)
    
    global resultado_label
    resultado_label = tk.Label(content_frame, text="", fg="white", bg="#2C3E50", font=("Arial", 12))
    resultado_label.pack(pady=10)

# Interfaz gráfica principal
root = tk.Tk()
root.title("Gestor de AFN")
root.geometry("700x450")
root.configure(bg="#2C3E50")

# Marco para el menú lateral
menu_frame = tk.Frame(root, bg="#34495E", width=220, height=450)
menu_frame.pack(side="left", fill="y")

# Botones del menú
menu_label = tk.Label(menu_frame, text="Menú", font=("Arial", 18, "bold"), fg="white", bg="#34495E")
menu_label.pack(pady=15)

crear_afn_btn = tk.Button(menu_frame, text="Crear AFN Básico", command=mostrar_crear_afn, bg="#1ABC9C", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5, width=18)
crear_afn_btn.pack(pady=10)

# Marco para el contenido
content_frame = tk.Frame(root, bg="#2C3E50", width=480, height=450)
content_frame.pack(side="right", fill="both", expand=True)

root.mainloop()