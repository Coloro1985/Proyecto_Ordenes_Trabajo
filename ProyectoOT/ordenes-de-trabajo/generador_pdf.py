import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from documentos.orden_trabajo import OrdenTrabajo
from documentos.orden_compra import OrdenCompra
from documentos.factura import Factura

def generar_orden_trabajo(datos):
    print("[DEBUG] Datos recibidos para generar orden de trabajo:")
    print(datos)
    orden = OrdenTrabajo(datos)
    return orden.generar_pdf()

def generar_orden_compra(datos):
    orden = OrdenCompra(datos)
    return orden.generar_pdf()

def generar_factura(datos):
    factura = Factura(datos)
    return factura.generar_pdf()


# Función para generar un documento según el tipo especificado
def generar_documento(tipo, datos):
    if tipo == "orden_trabajo":
        return generar_orden_trabajo(datos)
    elif tipo == "orden_compra":
        return generar_orden_compra(datos)
    elif tipo == "factura":
        return generar_factura(datos)
    else:
        raise ValueError(f"Tipo de documento desconocido: {tipo}")
