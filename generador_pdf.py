import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_orden_trabajo(datos):
    ruta_pdf = "orden_de_trabajo.pdf"
    ruta_logo = "/Users/claudioesteffansepulveda/Desktop/Programacion/Workspace/Ordenes De Trabajo/ProyectoOT/NuevoLogoGareste.png"

    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Dibujar logo si existe
    if os.path.exists(ruta_logo):
        c.drawImage(ruta_logo, 40, 700, width=80, height=80)
    
    # Información de la empresa
    empresa = datos['empresa']
    c.setFont("Helvetica-Bold", 12)
    c.drawString(150, 750, empresa['Nombre'])
    c.setFont("Helvetica", 10)
    c.drawString(150, 735, f"Dirección: {empresa['Dirección']}")
    c.drawString(150, 720, f"Ciudad: {empresa['Ciudad']}")
    c.drawString(150, 705, f"Teléfono: {empresa['Teléfono']}")
    c.drawString(150, 690, f"Correo: {empresa['Correo Electrónico']}")

    # Información dinámica del formulario
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 650, "Orden de Trabajo")
    c.setFont("Helvetica", 10)
    c.drawString(40, 630, f"Número de Orden: {datos['numero_orden']}")
    c.drawString(40, 615, f"Fecha de Emisión: {datos['fecha_emision']}")
    c.drawString(40, 600, f"Departamento Solicitante: {datos['departamento_solicitante']}")
    c.drawString(40, 585, f"Responsable: {datos['responsable_orden']}")

    # Descripción del trabajo
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, 560, "Descripción del Trabajo:")
    c.setFont("Helvetica", 10)
    c.drawString(40, 545, datos['descripcion_trabajo'][0])

    # Costos estimados
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, 520, "Costos Estimados:")
    c.setFont("Helvetica", 10)
    y_pos = 500  # Posición inicial de la tabla

    # Dibujar encabezados de tabla
    c.drawString(40, y_pos, "Concepto")
    c.drawString(200, y_pos, "Cantidad")
    c.drawString(300, y_pos, "Precio/Unidad")
    c.drawString(400, y_pos, "Valor Total")

    # Dibujar filas de la tabla
    for fila in datos['costos_estimados'][1:]:  # Saltar encabezado
        y_pos -= 20
        c.drawString(40, y_pos, fila[0] if fila[0] else "")  # Concepto
        c.drawString(200, y_pos, fila[1] if fila[1] else "")  # Cantidad
        c.drawString(300, y_pos, fila[2] if fila[2] else "")  # Precio/Unidad
        c.drawString(400, y_pos, fila[3] if fila[3] else "")  # Valor Total

    # Total estimado
    y_pos -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Total Estimado:")
    c.setFont("Helvetica", 10)
    c.drawString(400, y_pos, datos['costos_estimados'][-1][3])

    # Guardar PDF
    c.save()
    return os.path.abspath(ruta_pdf)


# Nueva función para generar orden de compra
def generar_orden_compra(datos):
    ruta_pdf = "orden_de_compra.pdf"
    ruta_logo = "/Users/claudioesteffansepulveda/Desktop/Programacion/Workspace/Ordenes De Trabajo/ProyectoOT/NuevoLogoGareste.png"

    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Información dinámica
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 750, f"Orden de Compra Nº: {datos['numero_orden']}")
    c.setFont("Helvetica", 10)
    c.drawString(40, 730, f"Fecha: {datos['fecha_emision']}")
    c.drawString(40, 715, f"Proveedor: {datos['proveedor']}")

    # Tabla de detalles
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 680, "Detalles del Servicio Contratado:")
    
    # Encabezados de tabla
    y_pos = 660
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Descripción")
    c.drawString(400, y_pos, "Valor (USD)")

    # Filas con datos
    c.setFont("Helvetica", 10)
    for servicio in datos['detalles_servicios']:
        y_pos -= 20
        c.drawString(40, y_pos, servicio['descripcion'])
        c.drawString(400, y_pos, f"{servicio['valor_usd']} USD")

    # Total general
    y_pos -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Total:")
    c.drawString(400, y_pos, f"{datos['total_usd']} USD")

    # Condiciones comerciales
    y_pos -= 50
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Condiciones:")
    c.setFont("Helvetica", 10)
    condiciones = datos['condiciones']
    for condicion in condiciones:
        y_pos -= 15
        c.drawString(40, y_pos, f"- {condicion}")

    # Logo en la parte inferior, reemplazando firma
    if os.path.exists(ruta_logo):
        c.drawImage(ruta_logo, 220, 50, width=160, height=160)

    # Guardar PDF
    c.save()
    return os.path.abspath(ruta_pdf)

