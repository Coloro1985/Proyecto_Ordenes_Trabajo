# 🧾 Generador de Órdenes de Trabajo y Compra - Gareste Ltda.

Sistema automatizado en Python para generar documentos PDF con control de versiones, proveedor y numeración.

---

## 🛠️ Funcionalidades

- Interfaz gráfica amigable (Tkinter).
- Generación automática de documentos:
  - 🧾 Órdenes de Trabajo
  - 💲 Órdenes de Compra (personalizadas en dólares)
  - 🧾 Módulo de Facturas (en desarrollo)
- Manejo de proveedores desde archivo CSV.
- Numeración automática y persistente de órdenes.
- Soporte para múltiples tipos de servicios (ej: movimiento de testigos mineros, pagos de sueldos, servicios administrativos).
- Inclusión del logo de Gareste Ltda. en los documentos.

---

## 📂 Estructura del Proyecto

```
ProyectoOT/
├── assets/                # Recursos estáticos (logo)
├── data/                  # Archivos de datos: proveedores, contador, etc.
│   └── ordenes_trabajo/   # PDFs generados para cada orden
├── documentos/            # Módulo con clases base y derivadas para tipos de documento (incluye módulo de facturas)
├── estilos.py             # Configuración de estilos para los PDFs
├── generador_pdf.py       # Lógica para construir los documentos
├── interfaz_grafica.py    # GUI con Tkinter
├── main.py                # Punto de entrada del programa
├── registro_ordenes.py    # Registro automático de órdenes
├── requirements.txt       # Dependencias del proyecto
├── utilidades.py          # Funciones auxiliares
├── LICENSE                # Licencia MIT
└── README.md              # Este archivo :)
```

---

## 🚀 Instalación

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/TU_USUARIO/ProyectoOT.git
   cd ProyectoOT
   ```

2. **Crea un entorno virtual y actívalo**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Mac/Linux
   .venv\Scripts\activate     # En Windows
   ```

3. **Instala las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación**
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
- Versión 1.1.1: Se consolida el proyecto en una sola raíz funcional. Se añade un módulo en desarrollo para la generación de facturas. Además, se actualiza el archivo README y el control de versiones semánticas.

![Version](https://img.shields.io/badge/version-1.1.1-blue.svg)

---

## 🧑‍💼 Autor

**Claudio Esteffan Sepúlveda**  
Proyecto interno de Gareste Ltda. - 2025

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
