import sys
import os

# Añadimos la raíz del proyecto al path
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(root_dir)

from interfaz_grafica import iniciar_interfaz

if __name__ == "__main__":
    iniciar_interfaz()