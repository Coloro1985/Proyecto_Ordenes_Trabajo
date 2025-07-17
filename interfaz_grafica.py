import tkinter as tk
from tkinter import ttk, messagebox
from estilos import configurar_estilos
from pathlib import Path
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
    ruta_logo = Path(__file__).parent / 'assets' / 'NuevoLogoGareste.png'
    imagen_logo = Image.open(ruta_logo)
    imagen_logo = imagen_logo.resize((90, 45), Image.LANCZOS)
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

    import datetime

    # Lista de campos dinámicos para el formulario
    campos = [
        'Número de Orden', 'Correo Electrónico', 'Fecha de Emisión',
        'Responsable de la Orden',
        'Fecha de Inicio',
        'Fecha Estimada de Finalización'
    ]

    entries = {}
    for campo in campos:
        frame = ttk.Frame(root)
        label = ttk.Label(frame, text=campo)
        entry = ttk.Entry(frame)
        entry.config(width=40)

        # Validación solo para campos numéricos
        if campo in ['Total Estimado', 'Total']:
            entry.config(validate="key", validatecommand=(validar_numero_cmd, '%P'))

        # Campo 'Número de Orden' prellenado y de solo lectura
        if campo == 'Número de Orden':
            entry.insert(0, str(numero_orden))
            entry.config(state='readonly')
        elif campo == 'Fecha de Emisión':
            fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
            entry.insert(0, fecha_actual)
            entry.config(state='readonly')

        label.pack(side='left')
        entry.pack(side='right', fill='x', expand=True)
        frame.pack(fill='x', padx=5, pady=5)
        entries[campo] = entry

    # Campo especial para ID de Proveedor
    frame_proveedor = ttk.Frame(root)
    label_proveedor = ttk.Label(frame_proveedor, text="ID Proveedor:")
    entry_id_proveedor = ttk.Entry(frame_proveedor, width=20)
    label_nombre_proveedor = ttk.Label(frame_proveedor, text="", foreground="gray")

    def cargar_nombre_proveedor(event=None):
        from utilidades import obtener_proveedor_por_id
        id_proveedor = entry_id_proveedor.get().strip()
        nombre = obtener_proveedor_por_id(id_proveedor)
        if nombre:
            label_nombre_proveedor.config(text=nombre)
        else:
            label_nombre_proveedor.config(text="Proveedor no encontrado")

    entry_id_proveedor.bind("<FocusOut>", cargar_nombre_proveedor)

    label_proveedor.pack(side="left")
    entry_id_proveedor.pack(side="left", padx=5)
    label_nombre_proveedor.pack(side="left", padx=10)
    frame_proveedor.pack(fill="x", padx=5, pady=5)

    # Guardar este entry en entries para poder usarlo en on_submit
    entries["Proveedor"] = entry_id_proveedor

    # Sección para agregar dinámicamente conceptos y valores
    frame_items = ttk.LabelFrame(root, text="Ítems de la Orden")
    frame_items.pack(fill='x', padx=10, pady=5)

    item_frames = []

    def agregar_item():
        sub_frame = ttk.Frame(frame_items)
        concepto_entry = ttk.Entry(sub_frame)
        valor_entry = ttk.Entry(sub_frame, validate="key", validatecommand=(validar_numero_cmd, '%P'))
        ttk.Label(sub_frame, text="Concepto:").pack(side="left", padx=5)
        concepto_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Label(sub_frame, text="Valor:").pack(side="left", padx=5)
        valor_entry.pack(side="left", fill="x", padx=5)
        sub_frame.pack(fill="x", pady=2)
        item_frames.append((concepto_entry, valor_entry))

    # Botón para agregar ítems
    boton_agregar_item = ttk.Button(root, text="+ Agregar Ítem", command=agregar_item)
    boton_agregar_item.pack(padx=10, pady=5)

    frame_servicios = ttk.LabelFrame(root, text="Servicios de la Orden de Compra")

    def actualizar_visibilidad_campos():
        es_orden_trabajo = tipo_documento.get() == "orden_trabajo"

        # Mostrar/Ocultar frame de ítems
        if es_orden_trabajo:
            frame_items.pack(fill='x', padx=10, pady=5)
        else:
            frame_items.pack_forget()

        # Mostrar/Ocultar frame de servicios
        if not es_orden_trabajo:
            frame_servicios.pack(fill="both", padx=10, pady=5)
        else:
            frame_servicios.pack_forget()

    ttk.Radiobutton(frame_tipo, text="Orden de Trabajo", variable=tipo_documento, value="orden_trabajo", command=actualizar_visibilidad_campos).pack(side="left", padx=10)
    ttk.Radiobutton(frame_tipo, text="Orden de Compra", variable=tipo_documento, value="orden_compra", command=actualizar_visibilidad_campos).pack(side="left", padx=10)
    frame_tipo.pack(padx=10, pady=5, fill="x")

    actualizar_visibilidad_campos()

    # Depuración
    print("Entries:", entries)
    print("Datos empresa:", datos_empresa)

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
    from utilidades import obtener_proveedor_por_id
    boton_generar = ttk.Button(
        root, 
        text="Generar PDF", 
        command=lambda: on_submit(
            entries,
            datos_empresa,
            tipo_documento.get(),
            servicios,
            [(c.get(), v.get()) for c, v in item_frames if c.get() and v.get()],
            obtener_proveedor_por_id(entry_id_proveedor.get().strip())
        )
    )
    boton_generar.pack(pady=10)

    root.mainloop()
