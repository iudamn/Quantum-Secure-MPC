import pandas as pd

df = pd.read_csv("../../../CSVCrimenes/Crime_PHILADELPHIA.csv")

traduccion = {
    "Other Assaults": "Otras agresiones",
    "All Other Offenses": "Otros delitos",
    "Weapon Violations": "Violaciones con armas",
    "Thefts": "Robos",
    "Burglary Non-Residential": "Robo a propiedad no residencial",
    "Aggravated Assault Firearm": "Agresión agravada con arma de fuego",
    "Theft from Vehicle": "Robo desde vehículo",
    "Disorderly Conduct": "Conducta desordenada",
    "Vandalism/Criminal Mischief": "Vandalismo / Daño criminal",
    "Arson": "Incendio provocado",
    "Fraud": "Fraude",
    "Robbery No Firearm": "Robo sin arma de fuego",
    "Vagrancy/Loitering": "Vagancia / Merodeo",
    "Motor Vehicle Theft": "Robo de vehículo",
    "Recovered Stolen Motor Vehicle": "Vehículo robado recuperado",
    "Robbery Firearm": "Robo con arma de fuego",
    "Embezzlement": "Malversación",
    "Rape": "Violación",
    "DRIVING UNDER THE INFLUENCE": "Conducir bajo influencia",
    "Forgery and Counterfeiting": "Falsificación",
    "Narcotic / Drug Law Violations": "Delitos de drogas",
    "Burglary Residential": "Robo a vivienda",
    "Other Sex Offenses (Not Commercialized)": "Otros delitos sexuales (no comercializados)",
    "Liquor Law Violations": "Violaciones a la ley de alcohol",
    "Aggravated Assault No Firearm": "Agresión agravada sin arma de fuego",
    "Homicide - Criminal": "Homicidio criminal",
    "Gambling Violations": "Delitos de juego",
    "Prostitution and Commercialized Vice": "Prostitución y vicio comercializado",
    "Public Drunkenness": "Intoxicación pública",
    "Receiving Stolen Property": "Receptación de bienes robados",
    "Homicide - Gross Negligence": "Homicidio por negligencia grave",
    "Offenses Against Family and Children": "Delitos contra la familia y niños",
    "Homicide - Justifiable": "Homicidio justificable",
    None: "Desconocido",
    float("nan"): "Desconocido"
}

# Crear nueva columna con la traducción
df['Crimen'] = df['Text_General_Code'].map(traduccion)

# Mostrar todas las filas
pd.set_option('display.max_rows', None)

# Mostrar todas las columnas
pd.set_option('display.max_columns', None)

# Evitar que se trunque el contenido de cada celda
pd.set_option('display.max_colwidth', None)

# Mostrar las primeras 100 filas de las columnas deseadas
print(df[['Text_General_Code', 'Crimen']].head(100))

