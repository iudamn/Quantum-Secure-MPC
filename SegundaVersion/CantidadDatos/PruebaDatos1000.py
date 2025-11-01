import pandas as pd

# Ruta del archivo original
archivo_original = "IDEFC_NM_ago25.csv" #Este archivo es de México, pero es un archivo mucho más pequeño para poder hacer
# divisiones respecto a los crimenes de México en Agosto del año 2025.

# Leer el CSV con codificación compatible con Windows
df = pd.read_csv(archivo_original, encoding='cp1252')

# Número de filas por archivo
filas_por_archivo = 1000

# Crear archivos con bloques consecutivos de 1000 filas
num_archivos = (len(df) + filas_por_archivo - 1) // filas_por_archivo  # calcular cantidad necesaria
for i in range(num_archivos):
    inicio = i * filas_por_archivo
    fin = inicio + filas_por_archivo
    df_parte = df.iloc[inicio:fin]
    archivo_salida = f"C:\\Users\\Camil\\PycharmProjects\\pythonProject10\\IDEFC_NM_ago25_1000_{i+1}.csv"
    df_parte.to_csv(archivo_salida, index=False, encoding='cp1252')
    print(f"Archivo guardado: {archivo_salida}")
