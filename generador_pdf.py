import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generar_orden_trabajo(datos):
    carpeta_base = os.path.abspath("data")
    carpeta_trabajo = os.path.join(carpeta_base, "ordenes_trabajo", f"OT-{datos['numero_orden']}")
    os.makedirs(carpeta_trabajo, exist_ok=True)
    nombre_archivo = f"orden_trabajo_{datos['numero_orden']}.pdf"
    ruta_pdf = os.path.join(carpeta_trabajo, nombre_archivo)
    ruta_logo = "/Users/claudioesteffansepulveda/Desktop/Programacion/Workspace/Ordenes De Trabajo/ProyectoOT/assets/NuevoLogoGareste.png"

    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Dibujar logo si existe
    if os.path.exists(ruta_logo):
        c.drawImage(ruta_logo, 40, 700, width=80, height=80)
    
    # Título grande y centrado con fondo azul oscuro y texto blanco
    c.setFillColor(colors.darkblue)
    c.rect(40, 765, 520, 25, fill=1)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.white)
    c.drawCentredString(300, 770, "ORDEN DE TRABAJO")
    c.setFillColor(colors.black)

    # Información de la empresa
    empresa = datos['empresa']
    c.setFont("Helvetica-Bold", 12)
    c.drawString(150, 740, empresa['Nombre'])
    c.setFont("Helvetica", 10)
    c.drawString(150, 725, f"Dirección: {empresa['Dirección']}")
    c.drawString(150, 710, f"Ciudad: {empresa['Ciudad']}")
    c.drawString(150, 695, f"Teléfono: {empresa['Teléfono']}")
    c.drawString(150, 680, f"Correo: {empresa['Correo Electrónico']}")

    # Línea divisoria después de datos de la empresa
    c.line(40, 670, 560, 670)
    y_pos = 655

    # Información dinámica del formulario
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_pos, "Orden de Trabajo")
    y_pos -= 20
    c.setFont("Helvetica", 10)
    c.drawString(40, y_pos, f"Número de Orden: {datos['numero_orden']}")
    y_pos -= 15
    c.drawString(40, y_pos, f"Fecha de Emisión: {datos['fecha_emision']}")
    y_pos -= 15
    # c.drawString(40, 590, f"Departamento Solicitante: {datos['departamento_solicitante']}")
    c.drawString(40, y_pos, f"Responsable de la Orden: {datos['responsable_orden']}")
    y_pos -= 20

    # Línea divisoria después de datos de la orden
    c.line(40, y_pos, 560, y_pos)
    y_pos -= 15

    # Información del mandante
    mandante = datos.get('mandante', {})
    if mandante:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(300, y_pos + 65, mandante.get('Nombre', ''))
        c.setFont("Helvetica", 10)
        c.drawString(300, y_pos + 50, f"ID: {mandante.get('ID', '')}")
        c.drawString(300, y_pos + 35, f"Dirección: {mandante.get('Dirección', '')}")
        c.drawString(300, y_pos + 20, f"Correo: {mandante.get('Correo Electrónico', '')}")
        c.drawString(300, y_pos + 5, f"Teléfono: {mandante.get('Teléfono', '')}")

    y_pos -= 100  # Espacio después del bloque del mandante

    if 'mandante_nombre' in datos and 'mandante_id' in datos:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y_pos, "Mandante del Servicio:")
        y_pos -= 15
        c.setFont("Helvetica", 10)
        c.drawString(40, y_pos, f"Nombre: {datos['mandante_nombre']}")
        y_pos -= 15
        c.drawString(40, y_pos, f"ID: {datos['mandante_id']}")
        y_pos -= 15

    # Descripción del trabajo
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Frame

    estilo_parrafo = getSampleStyleSheet()["Normal"]
    estilo_parrafo.fontName = "Helvetica"
    estilo_parrafo.fontSize = 10
    estilo_parrafo.leading = 12

    descripcion_texto = datos.get('descripcion_trabajo', '').strip()
    if descripcion_texto:
        parrafo = Paragraph(descripcion_texto.replace('\n', '<br/>'), estilo_parrafo)
        frame = Frame(40, y_pos - 150, 500, 130, showBoundary=0)
        frame.addFromList([parrafo], c)
    else:
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(40, y_pos - 20, "No se proporcionó descripción del trabajo.")
    y_pos -= 160  # Ajustar la posición para lo que sigue

    # Línea divisoria después de descripción del trabajo
    c.line(40, y_pos, 560, y_pos)
    y_pos -= 15

    # Costos estimados
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Costos Estimados:")
    y_pos -= 20  # Posición inicial de la tabla

    # Dibujar encabezados de tabla con fondo azul claro y texto blanco
    c.setFillColor(colors.HexColor("#4472C4"))
    c.rect(40, y_pos - 2, 460, 22, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(45, y_pos, "Concepto")
    c.drawString(200, y_pos, "Cantidad")
    c.drawString(300, y_pos, "Precio/Unidad")
    c.drawString(400, y_pos, "Valor Total")
    c.setFillColor(colors.black)

    estilos = getSampleStyleSheet()
    estilo_celda = estilos["Normal"]
    estilo_celda.fontName = "Helvetica"
    estilo_celda.fontSize = 10
    estilo_celda.leading = 12

    total_estimado = 0  # Inicializa el total

    # Dibujar filas de la tabla
    for fila in datos['costos_estimados'][1:]:  # Saltar encabezado
        y_pos -= 20
        concepto = str(fila[0]) if fila[0] else ""
        cantidad = str(fila[1]) if fila[1] else ""
        precio_unitario = str(fila[2]) if fila[2] else ""
        valor_total_raw = fila[3] if fila[3] else ""
        try:
            valor_total_float = float(str(valor_total_raw).replace(".", "").replace(",", ".").replace("$", "").strip())
            valor_total_formatted = f"${valor_total_float:,.2f}"
            total_estimado += valor_total_float
        except:
            valor_total_formatted = str(valor_total_raw)

        # Dibujo del concepto con salto de línea (ajuste manual de longitud)
        concepto_lines = concepto.split('\n')
        for i, line in enumerate(concepto_lines):
            c.drawString(45, y_pos - (i * 12), line)
        c.drawString(200, y_pos, cantidad)
        c.drawString(300, y_pos, precio_unitario)
        c.drawRightString(500, y_pos, valor_total_formatted)

        # Ajustar y_pos si hay múltiples líneas en concepto
        y_pos -= (len(concepto_lines) - 1) * 12

    # Total estimado con fondo gris claro
    y_pos -= 30
    c.setFillColor(colors.whitesmoke)
    c.rect(40, y_pos - 2, 460, 18, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Total Estimado:")
    c.setFont("Helvetica", 10)
    total_formatted = f"${total_estimado:,.2f}"
    c.drawRightString(500, y_pos, total_formatted)

    # Logo Gareste al pie
    if os.path.exists(ruta_logo):
        c.drawImage(ruta_logo, 450, 20, width=100, height=100)

    # Guardar PDF
    c.save()
    return os.path.abspath(ruta_pdf)


# Nueva función para generar orden de compra
def generar_orden_compra(datos):
    carpeta_base = os.path.abspath("data")
    carpeta_compra = os.path.join(carpeta_base, "ordenes_compra", f"OC-{datos['numero_orden']}")
    os.makedirs(carpeta_compra, exist_ok=True)
    nombre_archivo = f"orden_compra_{datos['numero_orden']}.pdf"
    ruta_pdf = os.path.join(carpeta_compra, nombre_archivo)
    ruta_logo = "/Users/claudioesteffansepulveda/Desktop/Programacion/Workspace/Ordenes De Trabajo/ProyectoOT/assets/NuevoLogoGareste.png"

    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Información dinámica
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 750, f"Orden de Compra Nº: {datos['numero_orden']}")
    c.setFont("Helvetica", 10)
    c.drawString(40, 730, f"Fecha: {datos['fecha_emision']}")
    c.drawString(40, 715, f"Proveedor: {datos['proveedor']['nombre']} (ID: {datos['proveedor']['id']})")

    # Tabla de detalles
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 680, "Detalles del Servicio Contratado:")
    
    # Encabezados de tabla
    y_pos = 660
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Descripción")
    c.drawString(400, y_pos, "Valor (USD)")

    margen_inferior = 100  # Límite para evitar escribir fuera de la página

    # Filas con datos
    c.setFont("Helvetica", 10)
    for servicio in datos['detalles_servicios']:
        for linea in servicio['descripcion'].split('\n'):
            if y_pos < margen_inferior:
                c.showPage()
                y_pos = 750
                c.setFont("Helvetica-Bold", 10)
                c.drawString(40, y_pos, "Descripción")
                c.drawString(400, y_pos, "Valor (USD)")
                y_pos -= 20
                c.setFont("Helvetica", 10)
            c.drawString(40, y_pos, linea)
            y_pos -= 15
        if y_pos < margen_inferior:
            c.showPage()
            y_pos = 750
            c.setFont("Helvetica-Bold", 10)
            c.drawString(40, y_pos, "Descripción")
            c.drawString(400, y_pos, "Valor (USD)")
            y_pos -= 20
            c.setFont("Helvetica", 10)
        c.drawString(400, y_pos + 15, f"{servicio['valor_usd']} USD")
        y_pos -= 5

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
        if y_pos < margen_inferior:
            c.showPage()
            y_pos = 750
            c.setFont("Helvetica", 10)
        y_pos -= 15
        c.drawString(40, y_pos, f"- {condicion}")

    # Logo en la parte inferior, reemplazando firma
    if os.path.exists(ruta_logo):
        c.drawImage(ruta_logo, 220, 50, width=160, height=160)

    # Guardar PDF
    c.save()
    return os.path.abspath(ruta_pdf)

# Nueva función para generar factura
def generar_factura(datos):
    carpeta_base = os.path.abspath("data")
    carpeta_factura = os.path.join(carpeta_base, "facturas", f"FAC-{datos['numero_orden']}")
    os.makedirs(carpeta_factura, exist_ok=True)
    nombre_archivo = f"factura_{datos['numero_orden']}.pdf"
    ruta_pdf = os.path.join(carpeta_factura, nombre_archivo)
    ruta_logo = "/Users/claudioesteffansepulveda/Desktop/Programacion/Workspace/Ordenes De Trabajo/ProyectoOT/assets/NuevoLogoGareste.png"

    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Información dinámica
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 750, f"Factura Nº: {datos['numero_orden']}")
    c.setFont("Helvetica", 10)
    c.drawString(40, 730, f"Fecha: {datos['fecha_emision']}")
    c.drawString(40, 715, f"Proveedor: {datos['proveedor']['nombre']} (ID: {datos['proveedor']['id']})")

    # Tabla de servicios facturados
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 680, "Servicios Facturados:")
    
    y_pos = 660
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Descripción")
    c.drawString(400, y_pos, "Valor (USD)")

    margen_inferior = 100

    c.setFont("Helvetica", 10)
    for servicio in datos['detalles_servicios']:
        for linea in servicio['descripcion'].split('\n'):
            if y_pos < margen_inferior:
                c.showPage()
                y_pos = 750
                c.setFont("Helvetica-Bold", 10)
                c.drawString(40, y_pos, "Descripción")
                c.drawString(400, y_pos, "Valor (USD)")
                y_pos -= 20
                c.setFont("Helvetica", 10)
            c.drawString(40, y_pos, linea)
            y_pos -= 15
        if y_pos < margen_inferior:
            c.showPage()
            y_pos = 750
            c.setFont("Helvetica-Bold", 10)
            c.drawString(40, y_pos, "Descripción")
            c.drawString(400, y_pos, "Valor (USD)")
            y_pos -= 20
            c.setFont("Helvetica", 10)
        c.drawString(400, y_pos + 15, f"{servicio['valor_usd']} USD")
        y_pos -= 5

    # Total
    y_pos -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Total a Pagar:")
    c.drawString(400, y_pos, f"{datos['total_usd']} USD")

    # Instrucciones de pago
    y_pos -= 50
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_pos, "Instrucciones de Pago:")
    c.setFont("Helvetica", 10)
    instrucciones = datos['instrucciones_pago']
    for instruccion in instrucciones:
        if y_pos < margen_inferior:
            c.showPage()
            y_pos = 750
            c.setFont("Helvetica", 10)
        y_pos -= 15
        c.drawString(40, y_pos, f"- {instruccion}")

    # Logo en la parte inferior
    if os.path.exists(ruta_logo):
        c.drawImage(ruta_logo, 220, 50, width=160, height=160)

    c.save()
    return os.path.abspath(ruta_pdf)
