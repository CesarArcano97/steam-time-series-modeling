import pandas as pd
import numpy as np
import os

# --- CONFIGURACIÓN ---
INPUT_FILE = "data/raw/tf2_daily_players.csv"
OUTPUT_FILE = "data/processed/tf2_dataset_unificado.csv"

# --- DICCIONARIO DE OFERTAS (2010 - 2024) ---
# Formato: (Fecha Inicio, Fecha Fin)
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

def check_sale(date, sales_list):
    """Verifica si una fecha cae dentro de algún rango de ofertas."""
    # Convertimos a string YYYY-MM-DD para comparar fácil
    s_date = str(date.date())
    for start, end in sales_list:
        if start <= s_date <= end:
            return 1
    return 0

def main():
    print("⚙️  Construyendo Dataset Unificado para Team Fortress 2...")
    
    # 1. Cargar Datos Crudos
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: No se encuentra {INPUT_FILE}")
        return
        
    df = pd.read_csv(INPUT_FILE)
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # 2. Ingeniería de Variable: Fin de Semana (TF2 Special)
    # En TF2 el pico empieza el viernes.
    # Python weekday: 0=Lun, 4=Vie, 5=Sab, 6=Dom
    print("📆 Calculando fines de semana (Vie-Sab-Dom)...")
    df['fin_de_semana'] = df['fecha'].dt.dayofweek.apply(lambda x: 1 if x in [4, 5, 6] else 0)
    
    # 3. Ingeniería de Variable: Ofertas Steam (Histórico)
    print("💰 Mapeando histórico de Steam Sales (2010-2024)...")
    # Optimizamos creando un índice de fechas de oferta primero
    sale_dates = set()
    for start, end in STEAM_SALES:
        rango = pd.date_range(start, end)
        sale_dates.update(rango)
    
    # Aplicar mapeo rápido
    df['oferta_steam'] = df['fecha'].apply(lambda x: 1 if x in sale_dates else 0)
    
    # 4. Guardar
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    
    print("\n" + "="*40)
    print(f"✅ DATASET UNIFICADO GUARDADO: {OUTPUT_FILE}")
    print(f"📊 Total Filas: {len(df)}")
    print(f"🛒 Días de Oferta detectados: {df['oferta_steam'].sum()}")
    print(f"🎉 Días de Finde detectados: {df['fin_de_semana'].sum()}")
    print("="*40)
    print("👉 Ahora usa este archivo en tu RNotebook: 'data/processed/tf2_dataset_unificado.csv'")

if __name__ == "__main__":
    main()
