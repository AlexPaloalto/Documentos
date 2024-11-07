import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import pyodbc
import threading

def log_texto(mensaje):
    texto_log.insert(tk.END, mensaje + "\n")
    texto_log.see(tk.END)

def cargar_datos_excel_a_sql(archivo_excel, tabla_sql, progreso):
    try:
        log_texto("Intentando leer el archivo de Excel...")
        df = pd.read_excel(archivo_excel)  # No especificamos sheet_name para leer la primera hoja por defecto
        if 'Estado de respuesta' in df.columns:
            df['Estado de respuesta'] = df['Estado de respuesta'].replace({'ANSWER': 'Contestada', 'NO ANSWER': 'No Contestada'})
        log_texto("Datos leídos del archivo de Excel con éxito.")

        # Columnas esperadas
        columnas_necesarias = {
            'Número llamado': 'telefono',
            'Estado de respuesta': 'edo_respuesta',
            'Campaña': 'cartera',
            'CLAVE': 'clave',
            'Fecha y hora inicio': 'fecha',
            'Tipo': 'contacto',
            'CARVEN': 'clave',
            'TELEFONO': 'telefono',
            'Resultado de marcacion': 'edo_respuesta'
        }

        # Filtrar columnas presentes en el DataFrame y evitar duplicados
        columnas_presentes = {col: columnas_necesarias[col] for col in columnas_necesarias if col in df.columns}
        
        # Eliminar duplicados en los nombres de columnas SQL
        columnas_sql_unique = list(dict.fromkeys(columnas_presentes.values()))
        
        num_rows = len(df)
        log_texto(f"Columnas presentes: {list(columnas_presentes.keys())}")

        log_texto("Intentando conectar a SQL Server...")
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=192.168.28.35,1433;'
            'DATABASE=dbo.herra;'
            'UID=test;'
            'PWD=test1'
        )
        log_texto("Conexión a SQL Server establecida con éxito.")

        cursor = conn.cursor()

        log_texto("Insertando datos en la base de datos...")
        for index, row in df.iterrows():
            try:
                valores = [str(row[col]) if not pd.isna(row[col]) else None for col in columnas_presentes]
                # Ajustamos los valores y placeholders a las columnas SQL únicas
                placeholders = ', '.join(['?' for _ in columnas_sql_unique])
                columnas_sql = ', '.join([f"[{sql_col}]" for sql_col in columnas_sql_unique])

                cursor.execute(f"INSERT INTO {tabla_sql} ({columnas_sql}) VALUES ({placeholders})", valores[:len(columnas_sql_unique)])
                progreso['value'] = (index + 1) / num_rows * 100
                ventana.update_idletasks()
            except Exception as row_error:
                log_texto(f"Error al insertar la fila {index}: {row_error}")

        conn.commit()
        cursor.close()
        conn.close()
        log_texto("Datos guardados correctamente.")
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo {archivo_excel} no fue encontrado.")
    except pyodbc.Error as ex:
        log_texto(f"Error de conexión a SQL Server: {ex}")
    except Exception as e:
        log_texto(f"Error general: {e}")

def seleccionar_archivo():
    archivo_excel = filedialog.askopenfilename(
        filetypes=[("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
    )
    if archivo_excel:
        confirmar_carga(archivo_excel)

def confirmar_carga(archivo_excel):
    respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas cargar el archivo {archivo_excel}?")
    if respuesta:
        progreso['value'] = 0
        threading.Thread(target=cargar_datos_excel_a_sql, args=(archivo_excel, 'dbo.Blaster', progreso)).start()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Seleccionar Archivo de Excel")

# Crear etiquetas informativas
label_titulo = tk.Label(ventana, text="Carga de Datos desde Excel a SQL Server", font=("Helvetica", 16))
label_titulo.pack(pady=10)

label_instruccion = tk.Label(ventana, text="Selecciona el archivo de Excel que deseas cargar a la base de datos.", font=("Helvetica", 12))
label_instruccion.pack(pady=5)

# Crear botón para seleccionar archivo
boton_seleccionar = ttk.Button(ventana, text="Seleccionar archivo .xlsx", command=seleccionar_archivo)
boton_seleccionar.pack(pady=20)

# Crear barra de progreso
progreso = ttk.Progressbar(ventana, orient="horizontal", length=300, mode="determinate")
progreso.pack(pady=10)

# Crear área de texto para mostrar log de operaciones
texto_log = tk.Text(ventana, height=15, width=50)
texto_log.pack(pady=30)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
