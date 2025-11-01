import asyncio
import pandas as pd
import glob
from collections import Counter
from mpyc.runtime import mpc
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import time

# En esta versión se incluyen mediciones de tiempo, a diferencia de las anteriores.
# Además, cada etapa del proceso se organiza en “Sprints” para estructurar el flujo de ejecución,
# facilitando la supervisión y verificación de que cada paso se realice correctamente.

# Configuración de archivos
CARPETA_DATOS = r"../PrimeraVersion"
ARCHIVOS = glob.glob(f"{CARPETA_DATOS}\\2015_parte_*.xlsx")

# Función para imprimir tabla de shares
def print_shares_table(shares):
    print("\nTabla de shares por nodo:")
    print("Nodo | Share")
    print("-----|------")
    for i, s in enumerate(shares, start=1):
        print(f"  {i}  |  {s}")

# Generación de shares cuánticos usando Shamir
def quantum_shamir_shares(secret: int, n: int, t: int) -> list:
    coef = [secret]
    print(f"\nSprint 2: Generación de coeficientes polinomiales")
    print(f"Secreto inicial: {secret}")
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
    print(f"Coeficientes generados: {coef}")
    shares = [sum(c * (x ** i) for i, c in enumerate(coef)) for x in range(1, n + 1)]
    print("Shares generados con superposición cuántica.")
    print_shares_table(shares)
    return shares

# Reconstrucción usando Lagrange
def lagrange_interpolation(x_vals, y_vals):
    terms = []
    secret_recon = 0
    for i in range(len(y_vals)):
        term_str = f"{y_vals[i]}"
        term_val = y_vals[i]
        for j in range(len(y_vals)):
            if i != j:
                term_str += f"*((x-{x_vals[j]})/({x_vals[i]}-{x_vals[j]}))"
                term_val *= (x_vals[j] / (x_vals[j] - x_vals[i]))
        terms.append(term_str)
        secret_recon += term_val
    return terms, round(secret_recon)

# MPC: procesa datos y reconstruye secreto
async def mpc_shamir_demo():
    start_total = time.time()  # <-- Marca de inicio total

    print("Sprint 1: Listado de archivos encontrados")
    for f in ARCHIVOS:
        print(f)

    print("\nSprint 4: Inicializando entorno MPC")
    await mpc.start()
    secint = mpc.SecInt()

    print("\nSprint 5: Extrayendo datos de Excel y contando delitos...")
    all_delitos = []
    for archivo in ARCHIVOS:
        df = pd.read_excel(archivo)
        delitos_col = df.iloc[:, 6].astype(str).tolist()
        all_delitos.extend(delitos_col)
    conteo = Counter(all_delitos)
    delito_mas_frecuente, cantidad = conteo.most_common(1)[0]
    print(f"Delito más frecuente: {delito_mas_frecuente} ({cantidad} veces)")

    print("\nSprint 2 (continuación): Generando shares cuánticos")
    n_shares = 4
    threshold = 3
    shares = quantum_shamir_shares(cantidad, n_shares, threshold)

    print("\nSprint 7: Simulación MPC y apertura de shares")
    sec_shares = [secint(s) for s in shares]
    opened = [await mpc.output(s) for s in sec_shares]
    print_shares_table(opened)

    print("\nSprint 8: Reconstrucción del secreto")
    x_vals = list(range(1, threshold + 1))
    y_vals = opened[:threshold]
    terms, secret_recon = lagrange_interpolation(x_vals, y_vals)
    print("Ecuación interpolinomial (Lagrange):")
    for t in terms:
        print("  ", t)
    print(f"\n➤ Secreto reconstruido correctamente: {secret_recon} (delito más frecuente: {delito_mas_frecuente})")

    print("\nSprint 9: Cerrando entorno MPC")
    await mpc.shutdown()

    end_total = time.time()  # Marca de fin total
    print(f"\nTiempo total de ejecución del procedimiento: {end_total - start_total:.2f} segundos")

if __name__ == "__main__":
    asyncio.run(mpc_shamir_demo())
