# SCRIPT: GENERACIÓN DE GRÁFICOS DE MODELADO (FORECAST & RESIDUOS)
# -----------------------------------------------------------------------------

# Limpieza preventiva
if (exists("var") && !is.function(var)) rm(var, envir = .GlobalEnv)

suppressPackageStartupMessages({
  library(forecast)
  library(ggplot2)
  library(readr)
  library(dplyr)
  library(gridExtra) # Para organizar paneles si es necesario
})

# Configuración
juegos_config <- list(
  "tf2"            = "Team Fortress 2",
  "cs2"            = "Counter-Strike 2",
  "eve_online"     = "EVE Online",
  "cyberpunk_2077" = "Cyberpunk 2077",
  "dwarf_fortress" = "Dwarf Fortress"
)

# Directorio de salida
output_dir <- "results/figures"
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

# -----------------------------------------------------------------------------
# Función de Graficado
# -----------------------------------------------------------------------------
graficar_modelo <- function(slug, nombre) {
  
  cat(sprintf("\nGenerando gráficos para: %s...\n", nombre))
  
  # 1. Cargar Datos
  archivo_csv <- file.path("data/processed", paste0(slug, "_dataset_unificado.csv"))
  if (!file.exists(archivo_csv)) return(NULL)
  
  df <- read_csv(archivo_csv, show_col_types = FALSE)
  
  # Filtrar (Últimos 4 años para consistencia con el modelo)
  if (nrow(df) > 1460) df <- tail(df, 1460)
  
  # 2. Preparar Series
  ts_jugadores <- ts(df$jugadores, frequency = 7)
  
  # Regresores
  cols_xreg <- c("fin_de_semana", "oferta_steam")
  cols_existentes <- cols_xreg[cols_xreg %in% names(df)]
  
  if (length(cols_existentes) > 0) {
    xreg_matrix <- as.matrix(df[, cols_existentes])
    # Limpiar constantes
    es_constante <- apply(xreg_matrix, 2, function(x) max(x, na.rm=T) == min(x, na.rm=T))
    xreg_matrix <- xreg_matrix[, !es_constante, drop = FALSE]
  } else {
    xreg_matrix <- NULL
  }
  
  usar_xreg <- !is.null(xreg_matrix) && ncol(xreg_matrix) > 0
  
  # 3. Split Train/Test (30 días)
  n_test <- 30
  n_train <- length(ts_jugadores) - n_test
  
  train_ts <- subset(ts_jugadores, end = n_train)
  test_ts  <- subset(ts_jugadores, start = n_train + 1)
  
  if (usar_xreg) {
    xreg_train <- xreg_matrix[1:n_train, , drop = FALSE]
    xreg_test  <- xreg_matrix[(n_train + 1):length(ts_jugadores), , drop = FALSE]
  } else {
    xreg_train <- NULL
    xreg_test  <- NULL
  }
  
  # 4. Ajustar Modelo (Misma especificación robusta)
  tryCatch({
    modelo <- Arima(
      train_ts,
      order = c(1, 1, 1),
      seasonal = list(order = c(1, 0, 0), period = 7),
      xreg = xreg_train,
      method = "CSS-ML"
    )
    
    # 5. Generar Pronóstico
    fc <- forecast(modelo, h = n_test, xreg = xreg_test)
    
    # ---------------------------------------------------------
    # GRÁFICO 1: PRONÓSTICO VS REALIDAD (ZOOM)
    # ---------------------------------------------------------
    file_forecast <- file.path(output_dir, paste0("forecast_", slug, ".png"))
    
    png(file_forecast, width = 1200, height = 600, res = 100)
    
    # Graficamos solo los últimos 4 meses para ver el detalle (Train final + Test)
    plot(fc, include = 120, 
         main = paste("Pronóstico vs Realidad:", nombre),
         ylab = "Jugadores Simultáneos", xlab = "Días (Horizonte Reciente)",
         fcol = "#e74c3c", shadecols = c("#f1c40f", "#f39c12"))
    
    # Añadir línea de datos reales en el periodo de prueba
    lines(test_ts, col = "black", lwd = 2, lty = 1)
    
    legend("topleft", legend = c("Entrenamiento", "Pronóstico (Modelo)", "Datos Reales (Test)"),
           col = c("black", "#e74c3c", "black"), lty = c(1, 1, 1), lwd = c(1, 2, 2), bty = "n")
    
    dev.off()
    cat(sprintf("   -> Guardado: %s\n", file_forecast))
    
    # ---------------------------------------------------------
    # GRÁFICO 2: DIAGNÓSTICO DE RESIDUOS
    # ---------------------------------------------------------
    file_resid <- file.path(output_dir, paste0("residuals_", slug, ".png"))
    
    png(file_resid, width = 1000, height = 800, res = 100)
    checkresiduals(modelo)
    dev.off()
    cat(sprintf("   -> Guardado: %s\n", file_resid))
    
  }, error = function(e) {
    cat(sprintf("❌ Error graficando %s: %s\n", nombre, e$message))
  })
}

# Ejecución
cat("INICIANDO GENERACIÓN DE GRÁFICOS...\n")
for (slug in names(juegos_config)) {
  graficar_modelo(slug, juegos_config[[slug]])
}
cat("\nPROCESO COMPLETADO. Revisa 'results/figures/'.\n")
