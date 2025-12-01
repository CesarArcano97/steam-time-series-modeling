import pandas as pd
import os

# --- CONFIGURACIÓN ---
# Entrada: El archivo crudo de SteamDB para TF2
INPUT_FILE = "data/raw/steamdb_chart_440.csv"
# Salida: El archivo limpio que usará R
OUTPUT_FILE = "data/raw/tf2_daily_players.csv"

def process_tf2_data():
    print(f"🛠️  Procesando datos de Team Fortress 2 (AppID: 440)...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No encuentro '{INPUT_FILE}' en data/raw/")
        return

    try:
        # 1. Cargar CSV
        df = pd.read_csv(INPUT_FILE)
        
        # 2. Renombrar columnas (SteamDB -> Formato Tesis)
        df = df.rename(columns={"DateTime": "fecha", "Players": "jugadores"})
        
        # 3. Limpieza de Fechas
        # Convertir a datetime y quitar la hora (quedarnos con YYYY-MM-DD)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.date
        
        # 4. Limpieza de Nulos
        # SteamDB a veces trae filas vacías al inicio o final
        initial_count = len(df)
        df = df.dropna(subset=['jugadores'])
        df['jugadores'] = df['jugadores'].astype(int)
        
        # 5. Ordenar cronológicamente (Vital para series de tiempo)
        df = df.sort_values('fecha')
        
        # Guardar
        df[['fecha', 'jugadores']].to_csv(OUTPUT_FILE, index=False)
        
        print("\n✅ DATOS DE TF2 LISTOS:")
        print(f"   - Archivo generado: {OUTPUT_FILE}")
        print(f"   - Rango: {df['fecha'].min()} al {df['fecha'].max()}")
        print(f"   - Total Días: {len(df)}")
        print(f"   - Filas eliminadas (vacías): {initial_count - len(df)}")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    process_tf2_data()
