import pandas as pd

# Leer el archivo csv de crimenes en México para limpiarlos antes de usarlos para Computación Multipartita Segura Cuántica
# Se lee con codificación latin-1 a diferencia del archivo de EEUU porque el archivo CSV no está codificado en UTF-8,
# que es lo que pandas intenta usar por defecto

df = pd.read_csv(
    "../../../CSVCrimenes/Crime_MEXICO.csv",
    encoding='latin-1'
)

# Mostrar las primeras 10 filas. En vez de colocar df.head, se debe poner el set_option para que al ejecutarse
# puedan visualizarse todos los datos sin excepción y sin resumen truncado

pd.set_option('display.max_columns', None)
print(df.head(10))

# Tipo de delito es la columna dedicada a los crímenes cometidos. Se deben buscar los valores únicos para poder traducirlos
# y trabajar con ellos antes de fusionarlos con los otros documentos
print(df['Tipo de delito'].unique())

# Contar cuántos tipos distintos de delitos hay
num_delitos_distintos = df['Tipo de delito'].nunique()
print(f"Los tipos de delitos contabilizan en total: {num_delitos_distintos}")
