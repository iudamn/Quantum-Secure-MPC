import pandas as pd

df = pd.read_csv("../../../CSVCrimenes/Crime_LONDRES.csv")

traduccion = {
    "Burglary": "Robo con allanamiento",
    "Violence Against the Person": "Violencia contra la persona",
    "Robbery": "Robo",
    "Theft and Handling": "Robo y manejo de bienes",
    "Criminal Damage": "Daño criminal",
    "Drugs": "Delitos de drogas",
    "Fraud or Forgery": "Fraude o falsificación",
    "Other Notifiable Offences": "Otros delitos notificables",
    "Sexual Offences": "Delitos sexuales"
}

# Crear nueva columna con la traducción
df['Crimen'] = df['major_category'].map(traduccion)

# Mostrar todas las filas
pd.set_option('display.max_rows', None)

# Mostrar todas las columnas
pd.set_option('display.max_columns', None)

# Evitar que se trunque el contenido de cada celda
pd.set_option('display.max_colwidth', None)

# Mostrar las primeras 100 filas de las columnas deseadas
print(df[['major_category', 'Crimen']].head(100))

