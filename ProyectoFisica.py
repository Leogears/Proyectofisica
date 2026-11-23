import os 
import random
import tkinter as tk 
from tkinter import messagebox

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preguntas.txt")

def cargar_preguntas():
    with open(RUTA, encoding="utf-8") as f:
        return [l.strip().split("|") for l in f if l.strip().count("|") == 5]

def cambiar(vista):
    for f in (inicio, juego, resultados):
        f.pack_forget()
    vista.pack(expand=True)

def iniciar():
    global preguntas, i, puntos, vidas
    if not entry.get().strip():
        messagebox.showwarning("Falta el nombre", "Escribe tu nombre.")
        return
 
    try:
        todas = cargar_preguntas()
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo:\n{RUTA}")
        return
    if len(todas) < 5:
        messagebox.showerror("Error", "El archivo necesita al menos 5 preguntas.")
        return
    preguntas = random.sample(todas, 5) 
    i, puntos, vidas = 0, 0, 5
    cambiar(juego)
    mostrar()

def mostrar():
    p = preguntas[i]
    info.config(text=f"{entry.get()} | Puntaje: {puntos} | Vidas: {vidas}")
    pregunta.config(text=f"{i + 1}. {p[0]}")
    opciones.config(text="\n".join(f"{n}) {p[n]}" for n in range(1, 5)))
    escala.set(1)

def confirmar():
    global i, puntos, vidas
    p = preguntas[i]
    if escala.get() == int(p[5]):  
        puntos += 1
    else:
        vidas -= 1
        messagebox.showinfo("Incorrecto", f"La correcta era: {p[int(p[5])]}")
    i += 1
    if vidas == 0 or i == 5:
        final.config(text=f"{entry.get()}, tu puntaje es {puntos} de 5")
        cambiar(resultados)
        messagebox.showinfo("Fin del juego", f"Puntaje final: {puntos}/5")
    else:
        mostrar()

ventana = tk.Tk()
ventana.title("Quiz de Física Básica") #TITULO
ventana.geometry("560x420") 
inicio, juego, resultados = tk.Frame(ventana, bg="PINK"), tk.Frame(ventana, bg="PINK"), tk.Frame(ventana, bg="PINK")
tk.Label(inicio, text="Ingresa tu nombre:", font=("Arial", 14)).grid(row=0, column=0, pady=10) 
entry = tk.Entry(inicio, font=("Arial", 14)) #CREA EL CUADRO
entry.grid(row=1, column=0, pady=5) #SU POSICION
tk.Button(inicio, text="Comenzar", command=iniciar).grid(row=2, column=0, pady=10) #BOTON
info = tk.Label(juego, font=("Arial", 11), bg="blue") #ETIQUETA 0
info.grid(row=0, column=0)
pregunta = tk.Label(juego, font=("Times New Roman", 16), fg="#030303", wraplength=500) #pregunta
pregunta.grid(row=1, column=0, pady=15)
opciones = tk.Label(juego, font=("Arial", 12), justify="left") #RESPUESTAS
opciones.grid(row=2, column=0)
escala = tk.Scale(juego, from_=1, to=4, orient="horizontal", tickinterval=1, length=300) #DESLIZADOR
escala.grid(row=3, column=0, pady=15)
tk.Button(juego, text="Confirmar", command=confirmar).grid(row=4, column=0) #BOTON
final = tk.Label(resultados, font=("Times New Roman", 16)) #ETIQUETA RESULTADOS
final.grid(row=0, column=0, pady=15)
tk.Button(resultados, text="Jugar de nuevo", command=lambda: cambiar(inicio)).grid(row=1, column=0) #BOTON
tk.Button(resultados, text="Salir", command=ventana.destroy).grid(row=2, column=0, pady=10) #BOTON
cambiar(inicio)
ventana.mainloop()