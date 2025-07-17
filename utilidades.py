import os
from datetime import datetime
from tkinter import messagebox
from generador_pdf import generar_orden_trabajo, generar_orden_compra
import tkinter as tk

# Función principal
def on_submit(entries, datos_empresa, tipo_documento, servicios, item_frames, nombre_proveedor):
    try:
        validar_datos_obligatorios(entries, [
            'Número de Orden',
            'Correo Electrónico',
            'Fecha de Emisión',
            'Responsable de la Orden',
            'Fecha de Inicio',
            'Fecha Estimada de Finalización',
            'Proveedor'
        ])
        
        # Validar que los valores de ítems sean numéricos
        for frame in item_frames:
            if isinstance(frame, dict):
                valor_entry = frame.get('valor')
            elif isinstance(frame, tuple) and len(frame) > 1:
                valor_entry = frame[1]
            else:
                valor_entry = None

            if valor_entry and hasattr(valor_entry, "get"):
                valor = valor_entry.get().strip()
                if valor and not valor.replace('.', '', 1).isdigit():
                    raise ValueError(f"El valor '{valor}' no es numérico.")

        # Validar campos numéricos
        
        # Validar campos de fechas
        validar_datos_fechas(entries, ['Fecha de Emisión', 'Fecha de Inicio', 'Fecha Estimada de Finalización'])

        # Obtener y estructurar los datos
        datos = obtener_datos_formulario(entries, item_frames)
        datos['empresa'] = datos_empresa  # Añadir datos fijos de la empresa

        # Generar PDF según tipo_documento
        if tipo_documento == "orden_compra":
            if not servicios:
                raise ValueError("Debe agregar al menos un servicio a la orden de compra.")
            total_usd = sum(float(s['valor_usd']) for s in servicios)
            datos_oc = {
                "numero_orden": entries['Número de Orden'].get(),
                "fecha_emision": entries['Fecha de Emisión'].get(),
                "proveedor": nombre_proveedor,
                "detalles_servicios": servicios,
                "total_usd": f"{total_usd:.2f}",
                "condiciones": [
                    "Pago dentro de los próximos 30 días posteriores a la emisión.",
                    "Confirmar recepción vía correo electrónico."
                ]
            }
            ruta_pdf = generar_orden_compra(datos_oc)
        else:
            total_valores = 0.0
            for frame in item_frames:
                valor_entry = frame[1] if isinstance(frame, tuple) else frame.get('valor')
                if hasattr(valor_entry, "get"):
                    valor = valor_entry.get().strip()
                else:
                    valor = valor_entry.strip()
                if valor:
                    total_valores += float(valor)
            datos['total'] = f"{total_valores:.2f}"
            ruta_pdf = generar_orden_trabajo(datos)
        messagebox.showinfo("Éxito", f"Archivo PDF generado en: {ruta_pdf}")

        # Actualizar número de orden
        numero_orden = int(entries['Número de Orden'].get()) + 1
        actualizar_numero_orden(numero_orden)
        entries['Número de Orden'].config(state='normal')
        entries['Número de Orden'].delete(0, tk.END)
        entries['Número de Orden'].insert(0, str(numero_orden))
        entries['Número de Orden'].config(state='readonly')

    except ValueError as e:
        messagebox.showerror("Error", str(e))



# Validaciones
def validar_datos_obligatorios(entries, campos_obligatorios):
    for campo in campos_obligatorios:
        if not entries[campo].get().strip():
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")

def validar_datos_numericos(entries, campos_numericos):
    for campo in campos_numericos:
        valor = entries[campo].get().strip()
        if valor and not valor.isdigit():
            raise ValueError(f"El campo '{campo}' debe contener solo números.")

def validar_datos_fechas(entries, fechas_a_validar):
    """
    Valida que los campos de fecha estén en formato DD/MM/AAAA.
    """
    for campo in fechas_a_validar:
        fecha_texto = entries[campo].get().strip()
        if not validar_fecha(fecha_texto):
            raise ValueError(f"El campo '{campo}' no tiene un formato de fecha válido (DD/MM/AAAA).")


def validar_fecha(fecha_texto):
    try:
        datetime.strptime(fecha_texto, "%d/%m/%Y").date()
        return True
    except ValueError:
        return False

def validar_numero(valor):
    """Valida que el valor ingresado sea numérico o esté vacío."""
    return valor.isdigit() or valor == ""

# Manejo del número de orden
def obtener_numero_orden(archivo='numero_orden.txt'):
    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            numero = f.read().strip()
            return int(numero) if numero.isdigit() else 0
    return 0

def actualizar_numero_orden(numero, archivo='numero_orden.txt'):
    with open(archivo, 'w') as f:
        f.write(str(numero))

# Datos fijos
def obtener_datos_empresa_fijos():
    return {
        "Nombre": "Sociedad Gardner y Esteffan LTDA",
        "Dirección": "Van Buren 208",
        "Ciudad": "Copiapó",
        "Teléfono": "77.703.720-k",
        "Correo Electrónico": "claudioesteffan@gmail.com"
    }

# Recopilación de datos
def obtener_datos_formulario(entries, item_frames):
    """
    Recopila y estructura los datos ingresados en el formulario.
    Args:
        entries (dict): Diccionario con los campos del formulario y sus valores.
        item_frames (list): Lista de widgets dinámicos de ítems agregados.
    Returns:
        dict: Datos estructurados listos para ser procesados.
    """
    try:
        # Costos estimados dinámicos desde item_frames
        costos_estimados = [
            ["Concepto", "Cantidad", "Precio/Unidad", "Valor Total"]
        ]
        for frame in item_frames:
            concepto = valor = ""

            if isinstance(frame, dict):
                concepto_widget = frame.get('concepto')
                valor_widget = frame.get('valor')
                concepto = concepto_widget.get().strip() if hasattr(concepto_widget, "get") else str(concepto_widget).strip()
                valor = valor_widget.get().strip() if hasattr(valor_widget, "get") else str(valor_widget).strip()

            elif isinstance(frame, tuple):
                concepto_widget = frame[0]
                valor_widget = frame[1]
                concepto = concepto_widget.get().strip() if hasattr(concepto_widget, "get") else str(concepto_widget).strip()
                valor = valor_widget.get().strip() if hasattr(valor_widget, "get") else str(valor_widget).strip()

            if concepto or valor:
                costos_estimados.append([concepto, "", "", valor])

        # costos_estimados.append(["Total Estimado", "", "", entries["Total Estimado"].get()])

        datos = {
            "empresa": {},  # Se completa en on_submit
            "numero_orden": entries['Número de Orden'].get(),
            "fecha_emision": entries['Fecha de Emisión'].get(),
            "responsable_orden": entries['Responsable de la Orden'].get(),
            "descripcion_trabajo": entries.get('Descripción del Trabajo', tk.Entry()).get().strip(),
            "fechas_importantes": {
                "Fecha de Inicio": entries['Fecha de Inicio'].get(),
                "Fecha Estimada de Finalización": entries['Fecha Estimada de Finalización'].get()
            },
            "costos_estimados": costos_estimados
        }
        return datos
    except KeyError as e:
        messagebox.showerror("Error", f"Falta el campo: {e}")
        return None









# Buscar proveedor por ID en archivo CSV
import csv

def obtener_proveedor_por_id(id_proveedor, archivo='data/datos_proveedores.csv'):
    """
    Busca el nombre del proveedor a partir de un ID en un archivo CSV.

    Args:
        id_proveedor (str): ID del proveedor a buscar.
        archivo (str): Ruta al archivo CSV de proveedores.

    Returns:
        str or None: Nombre del proveedor si se encuentra, o None si no se encuentra.
    """
    if not os.path.exists(archivo):
        return None

    with open(archivo, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get('ID') == id_proveedor:
                return fila.get('Nombre')
    return None