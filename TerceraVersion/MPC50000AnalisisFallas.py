import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer CSV generado por el experimento
df = pd.read_csv("tabla_thresholds.csv")

# --- 1. Tasa de éxito por delito y threshold ---
resumen = df.groupby(["Delito","threshold"])["correcto"].mean().reset_index()
resumen.rename(columns={"correcto":"tasa_exito"}, inplace=True)
resumen["tasa_exito"] = resumen["tasa_exito"] * 100  # porcentaje
resumen.to_csv("resumen_delitos.csv", index=False)
print("Tabla resumida guardada en 'resumen_delitos.csv'")
print(resumen.head())

# --- 2. Tolerancia a fallas: éxito según shares perdidos ---
fallas = df.groupby("shares_perdidos")["correcto"].mean().reset_index()
fallas["correcto"] = fallas["correcto"] * 100
print("\nTasa de éxito según shares perdidos:")
print(fallas)

# --- 3. Visualización: mapa de calor éxito por delito y threshold ---
heatmap_data = df.pivot_table(
    index="Delito",
    columns="threshold",
    values="correcto",
    aggfunc="mean"
) * 100

plt.figure(figsize=(12,8))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title("Tasa de éxito de reconstrucción por delito y threshold (%)")
plt.xlabel("Threshold")
plt.ylabel("Delito")
plt.tight_layout()
plt.savefig("heatmap_delitos.png")
plt.show()
