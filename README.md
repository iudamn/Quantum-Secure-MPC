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
     - Mismo caso para 1.000, 50.000 y 200.000 filas.  
   - Carpetas adicionales:  
     - `CantidadDatos`: scripts que generan archivos con la cantidad específica de filas a trabajar a la posterioridad. 
     - `CrimenesAnalisis`: análisis y transformaciones de los CSV, consolidando resultados y considerando distintos idiomas. Mapeos y transformaciones futuras en el ámbito del Análisis de Datos.

3. **Archivos CSV originales:**  
   - La carpeta `CSVCrimenes` con CSV de **EEUU, Londres, México y Philadelphia** no está incluida debido a su tamaño (700.000–1.000.000 filas por archivo), que supera los límites de GitHub y Git LFS.  
   - Se proporciona la lógica para organizar los paths en el repositorio.  
   - Los archivos se pueden descargar desde Kaggle.
