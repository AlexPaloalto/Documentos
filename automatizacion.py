import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

def guardar_datos():
    opcion1 = combobox1.get()
    opcion2 = combobox2.get()
    entrada_texto = entrada.get()
    
    if opcion1 and opcion2 and entrada_texto:
        try:
            # Conectar a la base de datos usando tu dirección IP
            conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=192.168.28.35, 1433;'
                'DATABASE=dbo.herra;'
                'UID=test;'
                'PWD=test1'
            )
            cursor = conn.cursor()
            
            # Insertar los datos
            cursor.execute("INSERT INTO dbo.testaut (Contacto, Cartera, Cantidad) VALUES (?, ?, ?)", (opcion1, opcion2, entrada_texto))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Datos")

# Crear etiquetas y campos de entrada
ttk.Label(ventana, text="Medio de contacto:").grid(column=0, row=0, padx=10, pady=10)
opciones1 = ["BLASTER", "SMS", "MAIL"]
combobox1 = ttk.Combobox(ventana, values=opciones1)
combobox1.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(ventana, text="Cartera:").grid(column=0, row=1, padx=10, pady=10)
opciones2 = ["ATT", "BBVA", "GMF", "SCOT", "INFO","TYT"]
combobox2 = ttk.Combobox(ventana, values=opciones2)
combobox2.grid(column=1, row=1, padx=10, pady=10)

ttk.Label(ventana, text="Cantidad:").grid(column=0, row=2, padx=10, pady=10)
entrada = ttk.Entry(ventana)
entrada.grid(column=1, row=2, padx=10, pady=10)

# Crear el botón para guardar
boton_guardar = ttk.Button(ventana, text="Guardar", command=guardar_datos)
boton_guardar.grid(column=0, row=3, columnspan=2, padx=10, pady=20)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
