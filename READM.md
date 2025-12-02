## 📂 Datos

Este repositorio no contiene los archivos de datos por razones de almacenamiento.

**Instrucciones para reproducir:**

1. Descarga los históricos diarios desde SteamDB para los juegos deseados (formato CSV).
2. Coloca los archivos en la carpeta `data/raw/` con los siguientes nombres:
   - `steamdb_chart_440.csv` (Team Fortress 2)
   - `steamdb_chart_730 (2).csv` (Counter-Strike 2)
   - `steamdb_chart_1091500.csv` (Cyberpunk 2077)
   - ...
3. Ejecuta el script de procesamiento para generar los datasets limpios:
   ```bash
   python3 src/03_batch_process_all.py
