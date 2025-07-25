
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

class BaseDocumento:
    def __init__(self, datos):
        self.numero = datos.get('numero_orden', 'N/A')
        self.fecha_emision = datos.get('fecha_emision', 'N/A')
        self.responsable = datos.get('responsable_orden', 'N/A')
        self.proveedor = datos.get('nombre_proveedor', 'N/A')
        self.cliente = datos.get('cliente', 'N/A')
        
        # Corrección para el problema de descripción
        descripcion_obj = datos.get('descripcion_trabajo', {})
        if isinstance(descripcion_obj, dict):
            self.descripcion_trabajo = descripcion_obj.get('texto', '')
        else:
            self.descripcion_trabajo = str(descripcion_obj)

        self.items = datos.get('servicios', [])
        self.total = datos.get('total', '0.00')
        self.empresa = datos.get('empresa', {})
        
        # Datos específicos de Orden de Trabajo
        fechas_importantes = datos.get('fechas_importantes', {})
        self.fecha_inicio = fechas_importantes.get('Fecha de Inicio', 'N/A')
        self.fecha_fin = fechas_importantes.get('Fecha Estimada de Finalización', 'N/A')
        
    def calcular_total(self):
        total = 0.0
        for item in self.items:
            try:
                total += float(item.get('valor', 0.0))
            except (ValueError, TypeError):
                continue
        return total

    def generar_pdf(self):
        """
        Genera el documento PDF con los datos del objeto.
        Este método es heredado por todas las clases de documento.
        """
        doc_type = self.__class__.__name__.replace("Orden", "Orden_de_")
        # Asegurarse de que el directorio de salida exista
        output_dir = "documentos_generados"
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, f"{doc_type}_{self.numero}.pdf")
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # --- CABECERA ---
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, self.empresa.get('Nombre', 'Mi Empresa'))
        c.setFont("Helvetica", 10)
        c.drawString(72, height - 88, self.empresa.get('Dirección', ''))
        c.drawString(72, height - 100, self.empresa.get('Ciudad', ''))
        
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(width - 72, height - 72, f"{doc_type.replace('_', ' ').upper()} Nº: {self.numero}")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 72, height - 88, f"Fecha de Emisión: {self.fecha_emision}")
        
        # --- LÍNEA SEPARADORA ---
        c.line(72, height - 120, width - 72, height - 120)

        # --- INFORMACIÓN DEL DOCUMENTO ---
        y_position = height - 150
        c.setFont("Helvetica-Bold", 11)
        
        if self.__class__.__name__ == "Factura":
            c.drawString(72, y_position, f"Cliente: {self.cliente}")
        else:
            c.drawString(72, y_position, f"Proveedor: {self.proveedor}")
        
        c.drawString(72, y_position - 15, f"Responsable: {self.responsable}")
        
        if self.__class__.__name__ == "OrdenTrabajo":
            c.drawString(width/2, y_position, f"Fecha de Inicio: {self.fecha_inicio}")
            c.drawString(width/2, y_position - 15, f"Fecha de Fin: {self.fecha_fin}")

        # --- DESCRIPCIÓN ---
        y_position -= 50
        c.setFont("Helvetica-Bold", 11)
        c.drawString(72, y_position, "Descripción del Trabajo:")
        c.setFont("Helvetica", 10)
        
        # Manejo de texto largo para la descripción
        text_lines = self.descripcion_trabajo.split('\n')
        for line in text_lines:
            y_position -= 15
            c.drawString(82, y_position, line)
            if y_position < 200: # Salto de página si es necesario
                c.showPage()
                y_position = height - 72


        # --- TABLA DE ITEMS ---
        y_position -= 40
        c.setFont("Helvetica-Bold", 11)
        c.drawString(72, y_position, "Concepto")
        c.drawRightString(width - 72, y_position, "Valor")
        c.line(72, y_position - 5, width - 72, y_position - 5)
        
        c.setFont("Helvetica", 10)
        y_position -= 20
        for item in self.items:
            c.drawString(72, y_position, item.get('nombre', ''))
            valor_str = f"${float(item.get('valor', 0)):,.2f}"
            c.drawRightString(width - 72, y_position, valor_str)
            y_position -= 15

        # --- TOTAL ---
        c.line(width - 200, y_position, width - 72, y_position)
        y_position -= 20
        c.setFont("Helvetica-Bold", 12)
        total_str = f"${self.calcular_total():,.2f}"
        c.drawRightString(width - 72, y_position, f"TOTAL: {total_str}")

        c.save()
        return file_path