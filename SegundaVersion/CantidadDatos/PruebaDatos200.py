import pandas as pd

# Ruta del archivo original
archivo_original = "IDEFC_NM_ago25.csv" #Este archivo es de México, pero es un archivo mucho más pequeño para poder hacer
# divisiones respecto a los crimenes de México en Agosto del año 2025.

# Leer el CSV con codificación compatible con Windows
df = pd.read_csv(archivo_original, encoding='cp1252')

# Número de filas por archivo, que en este caso son 200 ya que anteriormente habíamos intentado con 25 y funcionó sin
# problemas. Para esta ocasión se irá escalando hasta que el procesamiento llegue a tope y hacer comparación de tiempo
# de ejecución.
filas_por_archivo = 200

# Crear 4 archivos con bloques consecutivos de 200 filas
for i in range(4):
    inicio = i * filas_por_archivo
    fin = inicio + filas_por_archivo
    df_parte = df.iloc[inicio:fin]
    archivo_salida = f"C:\\Users\\Camil\\PycharmProjects\\pythonProject10\\IDEFC_NM_ago25_parte{i+1}.csv"
    df_parte.to_csv(archivo_salida, index=False, encoding='cp1252')  # mantener la misma codificación
    print(f"Archivo guardado: {archivo_salida}")
