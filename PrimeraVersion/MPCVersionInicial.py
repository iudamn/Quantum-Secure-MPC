import asyncio
import pandas as pd
import glob
from mpyc.runtime import mpc
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from random import randint
from collections import Counter

# En esta versión se utilizó el archivo CSV correspondiente a los crímenes ocurridos en México (Crime_Mexico en CSVCrimenes)
# A partir de este archivo, se tomaron las primeras 25 filas para generar el primer archivo,
# las siguientes 25 para el segundo, y así sucesivamente hasta completar un total de cuatro archivos.
# Inicialmente, el análisis se centró en calcular un único valor: el tipo de crimen más frecuente,
# el cual se empleó como secreto dentro del esquema de compartición. En esta etapa, no se generó un
# secreto por cada tipo de delito. Posteriormente, el enfoque fue ampliado para crear un secreto
# individual para cada categoría de delito, aumentando además la cantidad de columnas consideradas
# en cada archivo, con el fin de escalar progresivamente el nivel de cómputo y complejidad del procesamiento.

# ESTA ES UNA VERSIÓN CONCEPTUAL E INICIAL DEL MPC

# Carpeta con los archivos
carpeta = "../PrimeraVersion"
archivos = glob.glob(f"{carpeta}\\2015_parte_*.xlsx")

print("Archivos encontrados:")
for f in archivos:
    print(f)

# Función para simular generación cuántica de shares
def quantum_shamir_shares(secret, n, t):
    coef = [secret] + [randint(1, 10) for _ in range(t-1)]
    print(f"Coeficientes del polinomio (secreto = {secret}): {coef}")

    qc = QuantumCircuit(n)
    qc.h(range(n))

    shares = []
    for x in range(1, n+1):
        val = sum([c*(x**i) for i, c in enumerate(coef)])
        shares.append(val)

    simulator = AerSimulator()
    tqc = transpile(qc, simulator)
    simulator.run(tqc).result()

    print("Simulación cuántica completada (conceptual).")
    return shares


# Función MPC que procesa datos y reconstruye un secreto
async def mpc_shamir_demo():
    await mpc.start()
    secint = mpc.SecInt()

    # 1. Leer archivos y obtener la columna con más delitos
    print("\nExtrayendo datos de archivos Excel...")
    all_delitos = []
    for archivo in archivos:
        df = pd.read_excel(archivo)
        # Suponemos que la columna de delitos está en la posición 7 (como antes)
        delitos_col = df.iloc[:, 6].astype(str).tolist()
        all_delitos.extend(delitos_col)

    # Contar ocurrencias de cada delito
    conteo = Counter(all_delitos)
    delito_mas_frecuente, cantidad = conteo.most_common(1)[0]
    print(f"Delito más frecuente: {delito_mas_frecuente} ({cantidad} veces)")

    # Usamos la cantidad como "secreto"
    secreto = cantidad

    # 2. Generar shares con Qiskit
    n_shares = 5
    threshold = 3
    shares = quantum_shamir_shares(secreto, n_shares, threshold)
    print("Shares generados:", shares)

    # 3. Simular MPC reconstrucción
    sec_shares = [secint(s) for s in shares]
    opened = [await mpc.output(s) for s in sec_shares]
    print("Shares abiertos (MPC):", opened)

    # 4. Reconstrucción clásica (Lagrange)
    x_vals = list(range(1, threshold+1))
    y_vals = opened[:threshold]
    secret_recon = 0
    for i in range(threshold):
        term = y_vals[i]
        for j in range(threshold):
            if i != j:
                term *= x_vals[j] / (x_vals[j] - x_vals[i])
        secret_recon += term

    print(f"Secreto reconstruido (cantidad de delitos más frecuente): {round(secret_recon)}")

    await mpc.shutdown()

# Ejecutar
if __name__ == "__main__":
    asyncio.run(mpc_shamir_demo())
