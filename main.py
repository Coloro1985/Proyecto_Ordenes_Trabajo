import os
import sys

# Establecer la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Ejecutar la interfaz gráfica
from interfaz_grafica import iniciar_interfaz

if __name__ == "__main__":
    try:
        iniciar_interfaz()
    except Exception as e:
        print(f"[ERROR] No se pudo iniciar la interfaz: {e}")