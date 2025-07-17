# 🧾 Generador de Órdenes de Trabajo y Compra - Gareste Ltda.

Este proyecto es una herramienta interactiva creada en Python para **generar Órdenes de Trabajo y Órdenes de Compra en formato PDF**, orientado a facilitar la gestión documental de servicios realizados por Gareste Ltda., especialmente en el contexto de actividades mineras.

---

## 🛠️ Funcionalidades

- Interfaz gráfica amigable (Tkinter).
- Generación automática de:
  - Órdenes de Trabajo
  - Órdenes de Compra (personalizadas en dólares)
- Manejo de proveedores desde archivo CSV.
- Numeración automática y persistente de órdenes.
- Soporte para múltiples tipos de servicios (ej: movimiento de testigos mineros, pagos de sueldos, servicios administrativos).
- Inclusión del logo de Gareste Ltda. en los documentos.

---

## 📂 Estructura del Proyecto

```
ordenes-de-trabajo/
├── assets/                # Recursos estáticos (logo)
├── data/                  # Archivos de datos: proveedores, contador, etc.
├── estilos.py             # Configuración de estilos para los PDFs
├── generador_pdf.py       # Lógica para construir los documentos
├── interfaz_grafica.py    # GUI con Tkinter
├── main.py                # Punto de entrada del programa
├── utilidades.py          # Funciones auxiliares
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Este archivo :)
```

---

## 🚀 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/TU_USUARIO/ordenes-de-trabajo.git
   cd ordenes-de-trabajo
   ```

2. Crea un entorno virtual y actívalo:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Mac/Linux
   .venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el programa:
   ```bash
   python main.py
   ```

---

## 📄 Versionado (SemVer)

Este proyecto utiliza el esquema de versionado **[Semantic Versioning (SemVer)](https://semver.org/)** en el formato:

```
MAJOR.MINOR.PATCH (ejemplo: 1.0.2)
```

- **MAJOR**: Cambios incompatibles con versiones anteriores. Ej: reestructuración completa.
- **MINOR**: Nuevas funcionalidades compatibles. Ej: agregar un tipo de orden nuevo.
- **PATCH**: Correcciones de errores menores o mejoras sin romper nada. Ej: solucionar un bug en el PDF.

---

## 🧑‍💼 Autor

**Claudio Esteffan Sepúlveda**  
Proyecto interno de Gareste Ltda. - 2025

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
