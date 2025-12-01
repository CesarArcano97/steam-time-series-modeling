import pandas as pd
import numpy as np
import os

# --- CONFIGURACIÓN DE ARCHIVOS ---
# Mapeo: "Nombre del archivo crudo" -> "Nombre de salida deseado"
GAMES_CONFIG = {
    "steamdb_chart_440.csv":        "tf2",             # Team Fortress 2
    "steamdb_chart_730 (2).csv":    "cs2",             # Counter-Strike 2
    "steamdb_chart_8500.csv":       "eve_online",      # EVE Online
    "steamdb_chart_1091500.csv":    "cyberpunk_2077",  # Cyberpunk 2077
    "steamdb_chart_975370.csv":     "dwarf_fortress"   # Dwarf Fortress
}

INPUT_DIR = "data/raw/"
OUTPUT_DIR = "data/processed/"

# --- DICCIONARIO DE OFERTAS (2010 - 2024) ---
STEAM_SALES = [
    # 2024
    ("2024-03-14", "2024-03-21"), ("2024-06-27", "2024-07-11"), ("2024-11-27", "2024-12-04"),
    # 2023
    ("2023-03-16", "2023-03-23"), ("2023-06-29", "2023-07-13"), ("2023-11-21", "2023-11-28"), ("2023-12-21", "2024-01-04"),
    # 2022
    ("2022-06-23", "2022-07-07"), ("2022-11-22", "2022-11-29"), ("2022-12-22", "2023-01-05"),
    # 2021
    ("2021-06-24", "2021-07-08"), ("2021-11-24", "2021-11-30"), ("2021-12-22", "2022-01-05"),
    # 2020
    ("2020-06-25", "2020-07-09"), ("2020-11-25", "2020-12-01"), ("2020-12-22", "2021-01-05"),
    # 2019
    ("2019-06-25", "2019-07-09"), ("2019-11-26", "2019-12-03"), ("2019-12-19", "2020-01-02"),
    # 2018
    ("2018-06-21", "2018-07-05"), ("2018-11-21", "2018-11-27"), ("2018-12-20", "2019-01-03"),
    # 2017
    ("2017-06-22", "2017-07-05"), ("2017-11-22", "2017-11-28"), ("2017-12-21", "2018-01-04"),
    # 2016
    ("2016-06-23", "2016-07-04"), ("2016-11-23", "2016-11-29"), ("2016-12-22", "2017-01-02"),
    # 2015
    ("2015-06-11", "2015-06-21"), ("2015-11-25", "2015-12-01"), ("2015-12-22", "2016-01-04"),
    # Histórico Aproximado (2010-2014)
    ("2014-06-19", "2014-06-30"), ("2014-12-18", "2015-01-02"),
    ("2013-07-11", "2013-07-22"), ("2013-12-19", "2014-01-02"),
    ("2012-07-12", "2012-07-23"), ("2012-12-20", "2013-01-04"),
    ("2011-06-30", "2011-07-10"), ("2011-12-19", "2012-01-01"),
    ("2010-06-24", "2010-07-04"), ("2010-12-20", "2011-01-02")
]

def process_game(raw_file, game_slug):
    """Procesa un solo juego: Limpieza + Feature Engineering"""
    input_path = os.path.join(INPUT_DIR, raw_file)
    output_path = os.path.join(OUTPUT_DIR, f"{game_slug}_dataset_unificado.csv")
    
    print(f"🔄 Procesando: {game_slug} (Fuente: {raw_file})...")
    
    if not os.path.exists(input_path):
        print(f"   ⚠️ ALERTA: No se encuentra {input_path}. Saltando.")
        return

    try:
        # 1. Cargar y Limpiar
        df = pd.read_csv(input_path)
        df = df.rename(columns={"DateTime": "fecha", "Players": "jugadores"})
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.dropna(subset=['jugadores'])
        df['jugadores'] = df['jugadores'].astype(int)
        df = df.sort_values('fecha')

        # 2. Ingeniería: Fin de Semana (Vie, Sab, Dom)
        df['fin_de_semana'] = df['fecha'].dt.dayofweek.apply(lambda x: 1 if x in [4, 5, 6] else 0)

        # 3. Ingeniería: Ofertas Steam
        sale_dates = set()
        for start, end in STEAM_SALES:
            sale_dates.update(pd.date_range(start, end))
        
        df['oferta_steam'] = df['fecha'].apply(lambda x: 1 if x in sale_dates else 0)

        # 4. Guardar
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"   ✅ Guardado en: {output_path}")
        print(f"   📊 Registros: {len(df)}")
    
    except Exception as e:
        print(f"   ❌ Error procesando {game_slug}: {e}")

def main():
    print("🚀 INICIANDO PROCESAMIENTO POR LOTES (BATCH PROCESSING)")
    print("="*50)
    
    for raw_file, game_slug in GAMES_CONFIG.items():
        process_game(raw_file, game_slug)
        
    print("="*50)
    print("🎉 ¡Todos los datasets han sido generados!")
    print(f"📂 Revisa la carpeta: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
