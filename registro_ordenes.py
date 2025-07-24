import csv
import os
from datetime import datetime

# Ruta al archivo CSV
CSV_PATH = os.path.join("data", "ordenes_registradas.csv")

# Encabezados del CSV (ajústalos según los datos que manejas)
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
        with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(ENCABEZADOS)

def registrar_orden(id_orden, empresa, mandante, descripcion, total_usd):
    """Registra una nueva orden en el archivo CSV."""
    inicializar_registro()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            id_orden,
            fecha_actual,
            empresa,
            mandante,
            descripcion,
            total_usd
        ])