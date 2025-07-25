# Fichero: generador_pdf.py

import traceback
from documentos.orden_trabajo import OrdenTrabajo
from documentos.orden_compra import OrdenCompra
from documentos.factura import Factura

def generar_orden_trabajo(datos):
    print("[DEBUG] Generando Orden de Trabajo...")
    orden = OrdenTrabajo(datos)
    return orden.generar_pdf()

def generar_orden_compra(datos):
    print("[DEBUG] Generando Orden de Compra...")
    orden = OrdenCompra(datos)
    return orden.generar_pdf()

def generar_factura(datos):
    print("[DEBUG] Generando Factura...")
    factura = Factura(datos)
    return factura.generar_pdf()

def generar_documento(tipo, datos):
    print(f"[DEBUG] Generando documento de tipo: {tipo}")
    tipo_normalizado = tipo.lower().replace(" ", "_")
    
    try:
        if tipo_normalizado == "orden_de_trabajo":
            return generar_orden_trabajo(datos)
        elif tipo_normalizado == "orden_de_compra":
            return generar_orden_compra(datos)
        elif tipo_normalizado == "factura":
            return generar_factura(datos)
        else:
            raise ValueError(f"Tipo de documento desconocido: {tipo_normalizado}")
    except Exception as e:
        print(f"[ERROR] Error inesperado al generar documento: {e}")
        traceback.print_exc()
        print("[DEBUG] Datos que causaron el error:", datos)
        raise
