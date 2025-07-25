from logger_config import logger
import csv
import os
from datetime import datetime


# Ruta al archivo CSV
CSV_PATH = os.path.join("data", "ordenes_registradas.csv")

# Encabezados del CSV
ENCABEZADOS = [
    "ID",
    "Fecha",
    "Empresa",
    "Mandante",
    "Descripción del Trabajo",
    "Total USD"
]

def inicializar_registro():
    """Crea el archivo CSV si no existe."""
    if not os.path.exists(CSV_PATH):
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(ENCABEZADOS)
        logger.info("Se creó el archivo de registro de órdenes: %s", CSV_PATH)

def registrar_orden(id_orden, empresa, mandante, descripcion, total_usd):
    """Registra una nueva orden en el archivo CSV."""
    inicializar_registro()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        # --- CORRECCIÓN: Se usa 'descripcion' directamente ---
        escritor.writerow([
            id_orden,
            fecha_actual,
            empresa,
            mandante,
            descripcion,
            total_usd
        ])
    logger.info("Se registró una nueva orden: %s - %s", id_orden, descripcion)