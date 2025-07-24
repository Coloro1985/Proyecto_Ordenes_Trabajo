import os
from datetime import datetime
from tkinter import messagebox
from generador_pdf import generar_orden_trabajo, generar_orden_compra
import tkinter as tk
import csv
from registro_ordenes import registrar_orden

# --- LÓGICA PRINCIPAL ---

# Función principal
def on_submit(entries, datos_empresa, tipo_documento, servicios, item_frames, proveedor, cliente, descripcion_trabajo):
    try:
        validar_datos_obligatorios(entries, [
            'Número de Orden',
            'Correo Electrónico',
            'Fecha de Emisión',
            'Responsable de la Orden',
            'Fecha de Inicio',
            'Fecha Estimada de Finalización',
            'Proveedor',
            'ID Cliente'
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
                if valor:
                    valor_normalizado = valor.replace(".", "").replace(",", ".")
                    if not valor_normalizado.replace('.', '', 1).isdigit():
                        raise ValueError(f"El valor '{valor}' no es numérico.")

        # Validar campos numéricos
        
        # Validar campos de fechas
        validar_datos_fechas(entries, ['Fecha de Emisión', 'Fecha de Inicio', 'Fecha Estimada de Finalización'])

        # Obtener y estructurar los datos
        datos = obtener_datos_formulario(entries, item_frames)
        if datos is None:
            return  # Detener la ejecución si falló la recolección de datos
        datos['empresa'] = datos_empresa  # Añadir datos fijos de la empresa

        from generador_pdf import generar_documento

        datos["tipo_documento"] = tipo_documento
        datos["servicios"] = servicios
        datos["nombre_proveedor"] = proveedor
        datos["cliente"] = cliente
        datos["descripcion_trabajo"] = descripcion_trabajo

        ruta_pdf = generar_documento(tipo_documento, datos)

        registrar_orden(
            datos["numero_orden"],
            datos["fecha_emision"],
            datos.get("responsable_orden", proveedor),
            datos["empresa"]["Nombre"],
            descripcion_trabajo if descripcion_trabajo else datos.get("descripcion_trabajo", "Orden generada"),
            datos.get("total", "0.00")
        )
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


# --- VALIDACIONES ---

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


# --- MANEJO DE ARCHIVOS ---

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


# --- DATOS FIJOS ---

def obtener_datos_empresa_fijos():
    return {
        "Nombre": "Sociedad Gardner y Esteffan LTDA",
        "Dirección": "Van Buren 208",
        "Ciudad": "Copiapó",
        "Teléfono": "77.703.720-k",
        "Correo Electrónico": "claudioesteffan@gmail.com"
    }


# --- RECOLECCIÓN DE DATOS ---

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
                valor = valor.replace(".", "").replace(",", ".")
            elif isinstance(frame, tuple):
                concepto_widget = frame[0]
                valor_widget = frame[1]
                concepto = concepto_widget.get().strip() if hasattr(concepto_widget, "get") else str(concepto_widget).strip()
                valor = valor_widget.get().strip() if hasattr(valor_widget, "get") else str(valor_widget).strip()
                valor = valor.replace(".", "").replace(",", ".")

            if concepto or valor:
                costos_estimados.append([concepto, "", "", valor])

        # costos_estimados.append(["Total Estimado", "", "", entries["Total Estimado"].get()])

        if 'Descripción del Trabajo' not in entries:
            raise KeyError('Descripción del Trabajo')
        descripcion = entries['Descripción del Trabajo'].get("1.0", tk.END).strip()

        datos = {
            "empresa": {},  # Se completa en on_submit
            "numero_orden": entries['Número de Orden'].get(),
            "id_cliente": entries['ID Cliente'].get(),
            "fecha_emision": entries['Fecha de Emisión'].get(),
            "responsable_orden": entries['Responsable de la Orden'].get(),
            "descripcion_trabajo": descripcion,
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


# --- GESTIÓN DE PROVEEDORES ---

def obtener_proveedor_por_id(id_proveedor, archivo=os.path.join('data', 'datos_proveedores.csv')):
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

def guardar_proveedor(id_proveedor, nombre_proveedor, archivo=os.path.join('data', 'datos_proveedores.csv')):
    """
    Guarda un nuevo proveedor en el archivo CSV.

    Args:
        id_proveedor (str): ID del proveedor.
        nombre_proveedor (str): Nombre del proveedor.
        archivo (str): Ruta al archivo CSV.
    """
    nuevo_proveedor = {"ID": id_proveedor, "Nombre": nombre_proveedor}

    # Verifica si el archivo ya existe para no duplicar encabezados
    archivo_existe = os.path.exists(archivo)

    with open(archivo, 'a', newline='', encoding='utf-8') as csvfile:
        campos = ["ID", "Nombre"]
        writer = csv.DictWriter(csvfile, fieldnames=campos)

        if not archivo_existe:
            writer.writeheader()
        writer.writerow(nuevo_proveedor)


# --- GESTIÓN DE CLIENTES ---

def obtener_cliente_por_id(id_cliente, archivo=os.path.join('data', 'datos_clientes.csv')):
    """
    Busca el nombre del cliente a partir de un ID en un archivo CSV.

    Args:
        id_cliente (str): ID del cliente a buscar.
        archivo (str): Ruta al archivo CSV de clientes.

    Returns:
        str or None: Nombre del cliente si se encuentra, o None si no se encuentra.
    """
    if not os.path.exists(archivo):
        return None

    with open(archivo, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get('ID') == id_cliente:
                return fila.get('Nombre')
    return None