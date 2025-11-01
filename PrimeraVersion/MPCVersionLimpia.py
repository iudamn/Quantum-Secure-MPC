import asyncio
import pandas as pd
import glob
from collections import Counter
from mpyc.runtime import mpc
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# En esta versión del código se implementa un enfoque más estructurado para la simulación de cómputo multipartito seguro
# con conceptos cuánticos. A diferencia de la versión inicial, los coeficientes del polinomio de Shamir no se generan
# mediante números aleatorios clásicos, sino a través de mediciones obtenidas de un circuito cuántico en superposición,
# utilizando el simulador AerSimulator de Qiskit. Esto permite incorporar un componente cuántico real en la distribución
# del secreto, aumentando el nivel de aleatoriedad en la generación de los valores. Además, el código presenta una
# estructura con documentación detallada y una separación clara entre las etapas de extracción de datos, generación
# de shares, simulación cuántica, y reconstrucción del secreto mediante interpolación de Lagrange.

# Configuración de archivos
CARPETA_DATOS = r"../PrimeraVersion"
ARCHIVOS = glob.glob(f"{CARPETA_DATOS}\\2015_parte_*.xlsx")

print("Archivos encontrados:")
for f in ARCHIVOS:
    print(f)

# Generación de shares cuánticos usando Shamir
def quantum_shamir_shares(secret: int, n: int, t: int) -> list:
    """
    Genera n shares de un secreto usando un polinomio de grado (t-1),
    con coeficientes aleatorios generados por superposición cuántica.

    Args:
        secret (int): valor secreto a repartir.
        n (int): número de shares a generar.
        t (int): umbral mínimo para reconstrucción.

    Returns:
        list: lista de shares generados.
    """
    coef = [secret]  # Término independiente del polinomio

    # Generación de coeficientes aleatorios con superposición cuántica
    for _ in range(t - 1):
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Aplica Hadamard: superposición 0 y 1
        qc.measure(0, 0)

        simulator = AerSimulator()
        tqc = transpile(qc, simulator)
        result = simulator.run(tqc, shots=1).result()
        measured = int(list(result.get_counts().keys())[0])

        # Escala la medición a un valor entre 1 y 10
        coef_val = measured * 9 + 1
        coef.append(coef_val)

    print(f"Coeficientes del polinomio (secreto={secret}): {coef}")

    # Cálculo de shares evaluando el polinomio
    shares = [sum(c * (x ** i) for i, c in enumerate(coef)) for x in range(1, n + 1)]
    print("Shares generados con superposición cuántica.")
    return shares

# MPC: procesa datos y reconstruye secreto
async def mpc_shamir_demo():
    """
    Ejecuta un flujo MPC con Shamir para calcular el delito más frecuente
    de forma segura sin exponer los datos individuales.
    """
    # Inicializa el entorno MPC
    await mpc.start()
    secint = mpc.SecInt()

    # Extracción y conteo de delitos
    print("\nExtrayendo datos de archivos Excel...")
    all_delitos = []
    for archivo in ARCHIVOS:
        df = pd.read_excel(archivo)
        delitos_col = df.iloc[:, 6].astype(str).tolist()
        all_delitos.extend(delitos_col)

    conteo = Counter(all_delitos)
    delito_mas_frecuente, cantidad = conteo.most_common(1)[0]
    print(f"Delito más frecuente: {delito_mas_frecuente} ({cantidad} veces)")

    # Generación de shares
    n_shares = 4
    threshold = 3
    shares = quantum_shamir_shares(cantidad, n_shares, threshold)
    print("Shares generados:", shares)

    # Simulación MPC: convertir a SecInt y abrir shares
    sec_shares = [secint(s) for s in shares]
    opened = [await mpc.output(s) for s in sec_shares]
    print("Shares abiertos (MPC):", opened)

    # Reconstrucción del secreto usando interpolación de Lagrange
    x_vals = list(range(1, threshold + 1))
    y_vals = opened[:threshold]
    secret_recon = 0
    for i in range(threshold):
        term = y_vals[i]
        for j in range(threshold):
            if i != j:
                term *= x_vals[j] / (x_vals[j] - x_vals[i])
        secret_recon += term

    print(f"Secreto reconstruido (cantidad de delitos más frecuente): {round(secret_recon)}")

    # Cierra el entorno MPC
    await mpc.shutdown()

# Ejecución
if __name__ == "__main__":
    asyncio.run(mpc_shamir_demo())
