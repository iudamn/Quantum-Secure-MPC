import pandas as pd

# Leer el archivo csv de crimenes en EEUU para limpiarlos antes de usarlos para Computación Multipartita Segura Cuántica
df = pd.read_csv(r"..\..\..\CSVCrimenes\Crime_EEUU.csv")

# Mostrar las primeras 10 filas. En vez de colocar df.head, se debe poner el set_option para que al ejecutarse
# puedan visualizarse todos los datos sin excepción y sin resumen truncado

pd.set_option('display.max_columns', None)
print(df.head(10))
print(df.info())

# Crm Cd Desc es la columna dedicada a los crímenes cometidos. Se deben buscar los valores únicos para poder traducirlos
# y trabajar con ellos antes de fusionarlos con los otros documentos
print(df['Crm Cd Desc'].unique())

# Contar cuántos tipos distintos de delitos hay
num_delitos_distintos = df['Crm Cd Desc'].nunique()
print(f"Los tipos de delitos contabilizan en total: {num_delitos_distintos}")
