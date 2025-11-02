import time
import asyncio
import pandas as pd
from pathlib import Path
import glob
from collections import Counter
from mpyc.runtime import mpc
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Configuración de archivos
BASE_DIR = Path(__file__).resolve().parent
CARPETA_DATOS = BASE_DIR / "CantidadDatos"

# Buscar automáticamente los archivos generados
ARCHIVOS = glob.glob(str(CARPETA_DATOS / "*.csv"))

ESCALA = 1000  # factor de escalado para el secreto

# Imprimir tabla de shares
def print_shares_table(shares):
    print("\nTabla de shares por nodo:")
    print("Nodo | Share")
    print("-----|------")
    for i, s in enumerate(shares, start=1):
        print(f"  {i}  |  {s}")

# Generar shares con componente cuántico
def quantum_shamir_shares(secret: int, n: int, t: int) -> list:
    coef = [secret]
    for _ in range(t - 1):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        simulator = AerSimulator()
        tqc = transpile(qc, simulator)
        result = simulator.run(tqc, shots=1).result()
        measured = int(list(result.get_counts().keys())[0])
        coef_val = measured * 9 + 1
        coef.append(coef_val)
    shares = [sum(c * (x ** i) for i, c in enumerate(coef)) for x in range(1, n + 1)]
    return shares

# FUNCIÓN: Interpolación de Lagrange para reconstrucción
def lagrange_interpolation(x_vals, y_vals):
    secret_recon = 0
    for i in range(len(y_vals)):
        term_val = y_vals[i]
        for j in range(len(y_vals)):
            if i != j:
                term_val *= x_vals[j] / (x_vals[j] - x_vals[i])
        secret_recon += term_val
    return round(secret_recon)

# FUNCIÓN PRINCIPAL
async def mpc_shamir_demo():
    start_time = time.time()

    print("Listado de archivos CSV encontrados:")
    for f in ARCHIVOS:
        print(f)

    await mpc.start()
    secint = mpc.SecInt()

    all_delitos = []

    # Lectura de todos los archivos
    for archivo in ARCHIVOS:
        df = pd.read_csv(archivo, encoding='cp1252', low_memory=False)

        # Detectar automáticamente qué columna usar
        if "Crm Cd Desc" in df.columns:
            delitos_col = df["Crm Cd Desc"].astype(str).tolist()
        elif "Tipo de delito" in df.columns:
            delitos_col = df["Tipo de delito"].astype(str).tolist()
        else:
            print(f"⚠️ No se encontró la columna esperada en: {archivo}")
            continue

        all_delitos.extend(delitos_col)

    # Conteo de delitos
    conteo = Counter(all_delitos)

    print("\nDelitos encontrados y conteo (muestra):")
    for i, (d, c) in enumerate(conteo.items()):
        print(f"{d}: {c}")
        if i >= 10:  # muestra solo los primeros 10
            break

    # Configuración esquema de shamir
    n_shares = 4
    threshold = 3
    secretos = {}

    # Generación y reconstrucción de shamir
    for delito, cantidad in conteo.items():
        scaled_secret = cantidad * ESCALA
        shares = quantum_shamir_shares(scaled_secret, n_shares, threshold)
        sec_shares = [secint(s) for s in shares]
        opened = [await mpc.output(s) for s in sec_shares]
        x_vals = list(range(1, threshold + 1))
        secret_recon = lagrange_interpolation(x_vals, opened[:threshold]) // ESCALA
        secretos[delito] = secret_recon

    print("\nReconstrucción de secretos (muestra):")
    for i, (d, s) in enumerate(secretos.items()):
        print(f"{d}: secreto reconstruido = {s}")
        if i >= 10:
            break

    # determinar el delito más frecuente
    delito_max = max(secretos, key=secretos.get)
    print(f"\n➤ Delito más frecuente: {delito_max} ({secretos[delito_max]} veces)")

    await mpc.shutdown()

    end_time = time.time()
    print(f"\nTiempo total de ejecución: {end_time - start_time:.2f} segundos")

# ejecución
if __name__ == "__main__":
    asyncio.run(mpc_shamir_demo())
