import time
import asyncio
import pandas as pd
import glob
from collections import Counter
from mpyc.runtime import mpc
import random
from pathlib import Path

# Versión clásica del protocolo Shamir sin componente cuántico
# Este script genera un secreto independiente por cada tipo de delito.
# Cada secreto se comparte y reconstruye usando interpolación de Lagrange,
# simulando un entorno de Computación Segura Multiparte (MPC).

# Configuración de archivos
BASE_DIR = Path(__file__).resolve().parent
CARPETA_DATOS = BASE_DIR / "CantidadDatos"
ARCHIVOS = glob.glob(str(CARPETA_DATOS / "IDEFC_NM_ago25_1000_*.csv"))


ESCALA = 1000  # Escalamiento del secreto para evitar pérdidas de precisión

# Función para imprimir tabla de shares
def print_shares_table(shares):
    print("\nTabla de shares por nodo:")
    print("Nodo | Share")
    print("-----|------")
    for i, s in enumerate(shares, start=1):
        print(f"  {i}  |  {s}")

# Shamir clásico (sin componente cuántico)
def shamir_shares(secret: int, n: int, t: int) -> list:
    """Genera n shares de un secreto usando coeficientes aleatorios simples."""
    coef = [secret]
    for _ in range(t - 1):
        coef.append(random.randint(1, 10))
    shares = [sum(c * (x ** i) for i, c in enumerate(coef)) for x in range(1, n + 1)]
    return shares

# Interpolación de Lagrange
def lagrange_interpolation(x_vals, y_vals):
    """Reconstrucción del secreto original a partir de los shares."""
    secret_recon = 0
    for i in range(len(y_vals)):
        term_val = y_vals[i]
        for j in range(len(y_vals)):
            if i != j:
                term_val *= x_vals[j] / (x_vals[j] - x_vals[i])
        secret_recon += term_val
    return round(secret_recon)


# Ejecución principal
async def mpc_shamir_demo():
    start_time = time.time()

    print("Listado de archivos CSV encontrados:")
    if not ARCHIVOS:
        print("⚠️ No se encontraron archivos en la carpeta CantidadDatos.")
        return
    for f in ARCHIVOS:
        print(f)

    await mpc.start()
    secint = mpc.SecInt()

    all_delitos = []
    for archivo in ARCHIVOS:
        df = pd.read_csv(archivo, encoding='cp1252')
        delitos_col = df.iloc[:, 6].astype(str).tolist()  # Columna 7
        all_delitos.extend(delitos_col)

    conteo = Counter(all_delitos)

    print("\nDelitos encontrados y conteo:")
    for d, c in conteo.items():
        print(f"{d}: {c}")

    n_shares = 4
    threshold = 3
    secretos = {}

    for delito, cantidad in conteo.items():
        scaled_secret = cantidad * ESCALA
        shares = shamir_shares(scaled_secret, n_shares, threshold)
        sec_shares = [secint(s) for s in shares]
        opened = [await mpc.output(s) for s in sec_shares]
        x_vals = list(range(1, threshold + 1))
        secret_recon = lagrange_interpolation(x_vals, opened[:threshold]) // ESCALA
        secretos[delito] = secret_recon

    print("\nReconstrucción de secretos con Lagrange:")
    for d, s in secretos.items():
        print(f"{d}: secreto reconstruido = {s}")

    delito_max = max(secretos, key=secretos.get)
    print(f"\n➤ Delito más frecuente: {delito_max} ({secretos[delito_max]} veces)")

    await mpc.shutdown()

    end_time = time.time()
    print(f"\n⏱️ Tiempo total de ejecución: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    asyncio.run(mpc_shamir_demo())
