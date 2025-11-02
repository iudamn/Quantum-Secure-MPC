# Estructura del repositorio

1. **Versión inicial:**  
   - Define la estructura base del MPC.  
   - Incluye tres códigos variantes:  
     - MPCVersionInicial: estructura básica.    
     - Limpia: más específica, enfocada en la lógica central.
     - MPC3VersionExplicativa: última versión para este caso, incluye contador de tiempo.
   - Archivos de datos pequeños: 25 filas por CSV. Ejemplo: 2015_parte_*.xlsx, se refiere a crimenes cometidos en México en el año 2015. Se escogió este dataset por la facilidad del lenguaje y la no-barrera del idioma.

2. **Segunda versión orientada a Pruebas de Rendimiento:**  
   - Scripts nombrados según la cantidad de filas y tipo de ejecución:  
     - Ejemplo: `MPC200Clasico.py` → 200 filas, ejecución clásica. Asimismo, se repite para caso Cuántico. Esta práctica se repite en diferentes archivos según cantidad de datos, y no se hizo todo en un único archivo porque permite un control más claro de la ejecución y facilita comparar resultados entre las distintas versiones.
     - Mismo caso para 1.000, 50.000 y 200.000 filas. Hay un caso en particular que es 500.000 y es la versión cuántica, con una mezcla de dos archivos EEUU y dos archivos México. Es un poco diferente de las anteriores, pero la lógica es la misma; demora más que todas. 
   - Carpetas adicionales:  
     - `CantidadDatos`: scripts que generan archivos con la cantidad específica de filas a trabajar a la posterioridad. 
     - `CrimenesAnalisis`: análisis y transformaciones de los CSV, consolidando resultados y considerando distintos idiomas. Mapeos y transformaciones futuras en el ámbito del Análisis de Datos.

3. **Tercera versión orientada a Tolerancia a Fallos y Thresholds:**
   - Scripts de implementación MPC versión Cuántica orientados al Análisis de Thresholds y el análisis de la cantidad de shares-secretos, y los participantes necesarios para descifrar los secretos.
   - Heatmap, tabla CSV, resumen tipos de delitos.

5. **Archivos CSV originales:**  
   - La carpeta `CSVCrimenes` con CSV de **EEUU, Londres, México y Philadelphia** no está incluida debido a su tamaño (700.000–1.000.000 filas por archivo), que supera los límites de GitHub y Git LFS.  
   - Se proporciona la lógica para organizar la carpeta y archivos en el repositorio.
     ![Archivos](image.png)
   - Los archivos se pueden descargar desde Kaggle.
     Philadelphia: https://www.kaggle.com/datasets/mchirico/philadelphiacrimedata
     EEEUU: https://catalog.data.gov/dataset/crime-data-from-2020-to-present
     Londres: https://www.kaggle.com/datasets/jboysen/london-crime
     México: https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva
