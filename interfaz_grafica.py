import tkinter as tk
from tkinter import ttk, messagebox
from estilos import configurar_estilos
from PIL import Image, ImageTk
from utilidades import (
    validar_numero,  # Asegura que esté importado
    on_submit,
    obtener_numero_orden,
    obtener_datos_empresa_fijos
)

from generador_pdf import generar_orden_trabajo, generar_orden_compra


def iniciar_interfaz():
    root = tk.Tk()
    root.title("Generador de Órdenes de Trabajo")

    # Obtener datos fijos de la empresa
    datos_empresa = obtener_datos_empresa_fijos()

    # Configurar estilos personalizados
    configurar_estilos()

    # Frame para la información de la empresa (fija)
    frame_empresa = ttk.LabelFrame(root, text="Información de la Empresa")
    frame_empresa.pack(fill="x", padx=10, pady=5)

    for campo, valor in datos_empresa.items():
        frame = ttk.Frame(frame_empresa)
        label_campo = ttk.Label(frame, text=f"{campo}:", font=("Arial", 10, "bold"))
        label_valor = ttk.Label(frame, text=valor, font=("Arial", 10))
        label_campo.pack(side="left", padx=5, pady=2)
        label_valor.pack(side="left", padx=5, pady=2)
        frame.pack(fill="x")

    # Cargar y mostrar el logo de la empresa
    imagen_logo = Image.open('/Users/claudioesteffansepulveda/Desktop/Programacion/Workspace/Ordenes De Trabajo/ProyectoOT/NuevoLogoGareste.png')
    imagen_logo = imagen_logo.resize((100, 100), Image.LANCZOS)
    logo = ImageTk.PhotoImage(imagen_logo)
    etiqueta_logo = tk.Label(root, image=logo)
    etiqueta_logo.image = logo
    etiqueta_logo.pack(pady=10)

    # Obtener el siguiente número de orden
    numero_orden = obtener_numero_orden() + 1

    # Registrar validación numérica
    validar_numero_cmd = root.register(validar_numero)

    # Tipo de documento a generar
    tipo_documento = tk.StringVar(value="orden_trabajo")
    frame_tipo = ttk.LabelFrame(root, text="Tipo de Documento")
    ttk.Radiobutton(frame_tipo, text="Orden de Trabajo", variable=tipo_documento, value="orden_trabajo").pack(side="left", padx=10)
    ttk.Radiobutton(frame_tipo, text="Orden de Compra", variable=tipo_documento, value="orden_compra").pack(side="left", padx=10)
    frame_tipo.pack(padx=10, pady=5, fill="x")

    # Lista de campos dinámicos para el formulario
    campos = [
        'Número de Orden', 'Correo Electrónico', 'Fecha de Emisión', 
        'Departamento Solicitante', 'Responsable de la Orden',
        'Descripción del Trabajo', 'Fecha de Inicio', 
        'Fecha Estimada de Finalización',
        'Concepto 1', 'Valor 1', 'Concepto 2', 'Valor 2',
        'Concepto 3', 'Valor 3', 'Concepto 4', 'Valor 4',
        'Concepto 5', 'Valor 5', 'Total Estimado', 'Comentarios'
    ]

    entries = {}
    for campo in campos:
        frame = ttk.Frame(root)
        label = ttk.Label(frame, text=campo)
        entry = ttk.Entry(frame)

        # Validación solo para campos numéricos
        if campo in ['Valor 1', 'Valor 2', 'Valor 3', 'Valor 4', 'Valor 5', 'Total Estimado']:
            entry.config(validate="key", validatecommand=(validar_numero_cmd, '%P'))

        # Campo 'Número de Orden' prellenado y de solo lectura
        if campo == 'Número de Orden':
            entry.insert(0, str(numero_orden))
            entry.config(state='readonly')

        label.pack(side='left')
        entry.pack(side='right', fill='x', expand=True)
        frame.pack(fill='x', padx=5, pady=5)
        entries[campo] = entry

    # Depuración
    print("Entries:", entries)
    print("Datos empresa:", datos_empresa)

    # Sección para agregar servicios personalizados si se elige "Orden de Compra"
    frame_servicios = ttk.LabelFrame(root, text="Servicios de la Orden de Compra")
    frame_servicios.pack(fill="both", padx=10, pady=5)

    servicios = []

    def agregar_servicio():
        descripcion = entry_descripcion.get().strip()
        valor = entry_valor.get().strip()
        if descripcion and valor.replace('.', '', 1).isdigit():
            servicios.append({"descripcion": descripcion, "valor_usd": valor})
            lista_servicios.insert(tk.END, f"{descripcion} - ${valor} USD")
            entry_descripcion.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrada inválida", "Debes ingresar una descripción y un valor numérico.")

    def eliminar_servicio():
        seleccion = lista_servicios.curselection()
        if seleccion:
            index = seleccion[0]
            lista_servicios.delete(index)
            servicios.pop(index)
        else:
            messagebox.showinfo("Seleccionar servicio", "Selecciona un servicio para eliminar.")

    ttk.Label(frame_servicios, text="Descripción:").grid(row=0, column=0, padx=5, pady=5)
    entry_descripcion = ttk.Entry(frame_servicios, width=40)
    entry_descripcion.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_servicios, text="Valor (USD):").grid(row=1, column=0, padx=5, pady=5)
    entry_valor = ttk.Entry(frame_servicios, width=20)
    entry_valor.grid(row=1, column=1, padx=5, pady=5)

    boton_agregar = ttk.Button(frame_servicios, text="+ Agregar Servicio", command=agregar_servicio)
    boton_agregar.grid(row=0, column=2, rowspan=2, padx=10)

    boton_eliminar = ttk.Button(frame_servicios, text="Eliminar Servicio", command=eliminar_servicio)
    boton_eliminar.grid(row=3, column=0, columnspan=3, pady=(5, 0))

    lista_servicios = tk.Listbox(frame_servicios, height=5)
    lista_servicios.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    # Botón para generar el PDF
    boton_generar = ttk.Button(root, text="Generar PDF", command=lambda: on_submit(entries, datos_empresa, tipo_documento.get(), servicios))
    boton_generar.pack(pady=10)

    root.mainloop()
