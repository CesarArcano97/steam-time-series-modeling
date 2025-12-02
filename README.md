# Modelado de Series de Tiempo en Steam

Este repositorio contiene el código y la documentación para el análisis y modelado estocástico de la demanda de jugadores simultáneos (CCU) en la plataforma Steam.

## Objetivo
Aislar componentes estacionales (ciclos semanales) y efectos exógenos (ofertas, eventos) mediante técnicas de **Regresión con Errores ARMA**.

## Estructura
* `data/`: Datos crudos (JSON/CSV) y procesados.
* `src/`: Scripts de extracción (Python) y modelado (R).
* `results/`: Gráficos de diagnóstico y validación.

## Stack
* **Python:** Extracción de datos y preprocesamiento.
* **R:** Modelado de series de tiempo (Forecast/Tseries).
