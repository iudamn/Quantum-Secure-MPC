import pandas as pd

# Ruta del archivo original (CSV)
archivo_original = r"C:\Users\Camil\PycharmProjects\pythonProject10\Municipal-Delitos-2015-2025_ago2025.csv"

# Leer el CSV con codificación compatible con Windows
df = pd.read_csv(archivo_original, encoding='cp1252')  # o 'latin1' si cp1252 falla

# Número de filas por archivo
filas_por_archivo = 200000

# Crear únicamente 4 archivos con bloques consecutivos de 200.000 filas
for i in range(4):
    inicio = i * filas_por_archivo
    fin = inicio + filas_por_archivo
    df_parte = df.iloc[inicio:fin]
    archivo_salida = f"C:\\Users\\Camil\\PycharmProjects\\pythonProject10\\Municipal_Delitos_200000_{i + 1}.csv"
    df_parte.to_csv(archivo_salida, index=False, encoding='cp1252')
    print(f"Archivo guardado: {archivo_salida}")
