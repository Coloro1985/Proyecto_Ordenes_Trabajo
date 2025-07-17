import os
from datetime import datetime
from tkinter import messagebox
from generador_pdf import generar_orden_trabajo, generar_orden_compra
import tkinter as tk

# Función principal
def on_submit(entries, datos_empresa, tipo_documento, servicios):
    try:
        # Validar campos obligatorios
        validar_datos_obligatorios(entries, [
            'Correo Electrónico', 'Fecha de Emisión', 'Departamento Solicitante',
            'Responsable de la Orden', 'Descripción del Trabajo',
            'Fecha de Inicio', 'Fecha Estimada de Finalización'
        ])
        
        # Validar campos numéricos
        validar_datos_numericos(entries, ['Valor 1', 'Valor 2', 'Valor 3', 'Valor 4', 'Valor 5', 'Total Estimado'])
        
        # Validar campos de fechas
        validar_datos_fechas(entries, ['Fecha de Emisión', 'Fecha de Inicio', 'Fecha Estimada de Finalización'])

        # Obtener y estructurar los datos
        datos = obtener_datos_formulario(entries)
        datos['empresa'] = datos_empresa  # Añadir datos fijos de la empresa

        # Generar PDF según tipo_documento
        if tipo_documento == "orden_compra":
            if not servicios:
                raise ValueError("Debe agregar al menos un servicio a la orden de compra.")
            total_usd = sum(float(s['valor_usd']) for s in servicios)
            datos_oc = {
                "numero_orden": entries['Número de Orden'].get(),
                "fecha_emision": entries['Fecha de Emisión'].get(),
                "proveedor": entries['Responsable de la Orden'].get(),  # Asumido como proveedor
                "detalles_servicios": servicios,
                "total_usd": f"{total_usd:.2f}",
                "condiciones": [
                    "Pago dentro de los próximos 30 días posteriores a la emisión.",
                    "Confirmar recepción vía correo electrónico."
                ]
            }
            ruta_pdf = generar_orden_compra(datos_oc)
        else:
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
def obtener_datos_formulario(entries):
    """
    Recopila y estructura los datos ingresados en el formulario.
    Args:
        entries (dict): Diccionario con los campos del formulario y sus valores.
    Returns:
        dict: Datos estructurados listos para ser procesados.
    """
    try:
        # Costos estimados dinámicos
        costos_estimados = [
            ["Concepto", "Cantidad", "Precio/Unidad", "Valor Total"]
        ]
        for i in range(1, 6):  # Concepto 1 a Concepto 5
            concepto = entries[f"Concepto {i}"].get()
            valor = entries[f"Valor {i}"].get()
            if concepto or valor:  # Solo añadir si hay datos
                costos_estimados.append([concepto, "", "", valor])

        # Añadir el total estimado
        costos_estimados.append(["Total Estimado", "", "", entries["Total Estimado"].get()])

        # Estructura final de datos
        datos = {
            "empresa": {},  # Esto se completa en on_submit
            "numero_orden": entries['Número de Orden'].get(),
            "fecha_emision": entries['Fecha de Emisión'].get(),
            "departamento_solicitante": entries['Departamento Solicitante'].get(),
            "responsable_orden": entries['Responsable de la Orden'].get(),
            "descripcion_trabajo": [entries['Descripción del Trabajo'].get()],
            "fechas_importantes": {
                "Fecha de Inicio": entries['Fecha de Inicio'].get(),
                "Fecha Estimada de Finalización": entries['Fecha Estimada de Finalización'].get()
            },
            "costos_estimados": costos_estimados,
            "aprobaciones": {
                "Comentarios y otros": entries['Comentarios'].get()
            }
        }
        return datos
    except KeyError as e:
        messagebox.showerror("Error", f"Falta el campo: {e}")
        return None







