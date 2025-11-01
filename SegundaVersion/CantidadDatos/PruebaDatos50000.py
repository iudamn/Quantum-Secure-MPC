import pandas as pd

# Ruta del archivo original (Excel)
archivo_original = r"C:\Users\Camil\PycharmProjects\pythonProject10\2017.xlsx"

# Leer el Excel
df = pd.read_excel(archivo_original)

# Número de filas por archivo
filas_por_archivo = 50000

# Crear únicamente 4 archivos con bloques consecutivos de 50.000 filas
for i in range(4):
    inicio = i * filas_por_archivo
    fin = inicio + filas_por_archivo
    df_parte = df.iloc[inicio:fin]
    archivo_salida = f"C:\\Users\\Camil\\PycharmProjects\\pythonProject10\\2017_50000_{i + 1}.csv"
    df_parte.to_csv(archivo_salida, index=False, encoding='cp1252')
    print(f"Archivo guardado: {archivo_salida}")
