import os
import sys
from utilidades import guardar_proveedor, guardar_cliente
# Esta línea ya no es necesaria si tu estructura de proyecto es estándar y ejecutas desde main.py
# sys.path.append(os.path.join(os.path.dirname(__file__), 'documentos'))

import tkinter as tk
from tkinter import ttk, messagebox
# Asegúrate de que utilidades.py esté accesible
from utilidades import on_submit, obtener_proveedor_por_id, obtener_cliente_por_id, obtener_datos_empresa_fijos, obtener_numero_orden, actualizar_numero_orden

class VentanaGestionDatos(tk.Toplevel):
    """
    Una ventana emergente para agregar nuevos proveedores o clientes.
    """
    def __init__(self, parent, tipo):
        super().__init__(parent)
        self.tipo = tipo  # 'proveedor' o 'cliente'
        self.title(f"Agregar Nuevo {self.tipo.capitalize()}")
        self.geometry("400x150")
        
        # Widgets de la ventana
        ttk.Label(self, text="ID:").pack(pady=(10, 0))
        self.id_entry = ttk.Entry(self, width=40)
        self.id_entry.pack()

        ttk.Label(self, text="Nombre Completo:").pack(pady=(10, 0))
        self.nombre_entry = ttk.Entry(self, width=40)
        self.nombre_entry.pack()

        ttk.Button(self, text="Guardar", command=self._guardar).pack(pady=20)
        
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def _guardar(self):
        id_dato = self.id_entry.get().strip()
        nombre_dato = self.nombre_entry.get().strip()

        if not id_dato or not nombre_dato:
            messagebox.showerror("Error", "Ambos campos, ID y Nombre, son obligatorios.")
            return

        try:
            if self.tipo == 'proveedor':
                guardar_proveedor(id_dato, nombre_dato)
            elif self.tipo == 'cliente':
                guardar_cliente(id_dato, nombre_dato)
            
            messagebox.showinfo("Éxito", f"{self.tipo.capitalize()} guardado correctamente.")
            self.destroy() # Cierra la ventana emergente al guardar
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Ocurrió un error: {e}")

class FormularioDocumento:

    def __init__(self, parent):
        # 1. Inicializar variables
        self.entries = {}
        self.item_frames = []
        self.tipo_documento = tk.StringVar(value="Orden de Trabajo")
        self.datos_empresa = obtener_datos_empresa_fijos()

        # 2. Crear el contenedor principal PRIMERO
        self.frame_principal = ttk.Frame(parent, padding="10")
        self.frame_principal.pack(fill="both", expand=True)

        # 3. Crear todos los componentes de la interfaz UNA SOLA VEZ
        self._crear_campos_principales()
        self._crear_ids()

        # Frame para los botones de gestión
        frame_gestion = ttk.Frame(self.frame_principal)
        frame_gestion.pack(pady=10)
        ttk.Button(frame_gestion, text="Gestionar Proveedores", command=self._abrir_ventana_proveedores).pack(side="left", padx=5)
        ttk.Button(frame_gestion, text="Gestionar Clientes", command=self._abrir_ventana_clientes).pack(side="left", padx=5)
        
        self._crear_campo_descripcion()
        self._crear_items()
        self._crear_tipo_documento()
        
        # Botón final para generar el documento
        ttk.Button(self.frame_principal, text="Generar Documento", command=self._generar_documento).pack(pady=10)

        # 4. Cargar datos iniciales
        self._cargar_numero_orden()
    
    def _abrir_ventana_proveedores(self):
        VentanaGestionDatos(self.frame_principal, 'proveedor')

    def _abrir_ventana_clientes(self):
        VentanaGestionDatos(self.frame_principal, 'cliente')


    def _cargar_numero_orden(self):
        numero = obtener_numero_orden()
        # Hacemos el campo editable temporalmente para insertar el número
        self.entries['Número de Orden'].config(state='normal')
        self.entries['Número de Orden'].insert(0, str(numero))
        self.entries['Número de Orden'].config(state='readonly')

    def _crear_campos_principales(self):
        # --- CORRECCIÓN: Quitamos Proveedor de aquí, ya que se maneja por ID ---
        campos = [
            "Número de Orden", "Correo Electrónico", "Fecha de Emisión",
            "Responsable de la Orden", "Fecha de Inicio", "Fecha Estimada de Finalización"
        ]
        for campo in campos:
            frame = ttk.Frame(self.frame_principal)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text=campo + ":", width=30, anchor="w").pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(side="left", fill="x", expand=True)
            self.entries[campo] = entry

    def _crear_ids(self):
        frame_id_prov = ttk.Frame(self.frame_principal)
        frame_id_prov.pack(fill="x", pady=2)
        ttk.Label(frame_id_prov, text="ID Proveedor:", width=30).pack(side="left")
        # --- CORRECCIÓN: Añadimos los campos de ID al diccionario principal 'entries' ---
        self.entries["ID Proveedor"] = ttk.Entry(frame_id_prov)
        self.entries["ID Proveedor"].pack(side="left", fill="x", expand=True)

        frame_id_cli = ttk.Frame(self.frame_principal)
        frame_id_cli.pack(fill="x", pady=2)
        ttk.Label(frame_id_cli, text="ID Cliente:", width=30).pack(side="left")
        self.entries["ID Cliente"] = ttk.Entry(frame_id_cli)
        self.entries["ID Cliente"].pack(side="left", fill="x", expand=True)

    def _crear_campo_descripcion(self):
        frame_desc = ttk.LabelFrame(self.frame_principal, text="Descripción del Trabajo")
        frame_desc.pack(fill="both", expand=True, pady=5)
        # --- CORRECCIÓN: Guardamos la referencia al widget de texto en 'entries' ---
        self.entries["Descripción del Trabajo"] = tk.Text(frame_desc, height=5)
        self.entries["Descripción del Trabajo"].pack(fill="both", expand=True)

    def _crear_items(self):
        self.frame_items = ttk.LabelFrame(self.frame_principal, text="Ítems del Documento")
        self.frame_items.pack(fill="x", pady=5)
        ttk.Button(self.frame_principal, text="Agregar Ítem", command=self._agregar_item).pack(pady=5)

    def _agregar_item(self):
        frame = ttk.Frame(self.frame_items)
        frame.pack(fill="x", pady=2)
        
        concepto_entry = ttk.Entry(frame)
        concepto_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        valor_entry = ttk.Entry(frame, width=15)
        valor_entry.pack(side="left")

        # Guardamos un diccionario por cada ítem, es más limpio
        self.item_frames.append({"concepto": concepto_entry, "valor": valor_entry})
        
    def _crear_tipo_documento(self):
        frame_tipo = ttk.LabelFrame(self.frame_principal, text="Tipo de Documento")
        frame_tipo.pack(fill="x", pady=5)
        tipos = ["Orden de Trabajo", "Orden de Compra", "Factura"]
        for tipo in tipos:
            ttk.Radiobutton(
                frame_tipo, text=tipo, variable=self.tipo_documento, value=tipo
            ).pack(side="left", padx=5)
    
    def _generar_documento(self):
        # --- CÓDIGO COMPLETAMENTE REFACTORIZADO Y SIMPLIFICADO ---
        
        # 1. Obtener la descripción y validarla
        descripcion_texto = self.entries["Descripción del Trabajo"].get("1.0", "end-1c").strip()
        if not descripcion_texto:
            messagebox.showwarning("Campo requerido", "El campo 'Descripción del Trabajo' no puede estar vacío.")
            return

        # 2. Obtener IDs y los nombres correspondientes
        id_proveedor = self.entries["ID Proveedor"].get().strip()
        nombre_proveedor = obtener_proveedor_por_id(id_proveedor)
        if not nombre_proveedor:
            messagebox.showwarning("Proveedor no encontrado", f"No se encontró un proveedor con el ID: {id_proveedor}")
            return
            
        id_cliente = self.entries["ID Cliente"].get().strip()
        nombre_cliente = obtener_cliente_por_id(id_cliente)
        if not nombre_cliente:
            messagebox.showwarning("Cliente no encontrado", f"No se encontró un cliente con el ID: {id_cliente}")
            return
        
        # 3. Preparar la lista de ítems (ahora llamados servicios en el backend)
        # Esto es lo que `utilidades.on_submit` espera
        lista_servicios = []
        for frame in self.item_frames:
            concepto = frame["concepto"].get().strip()
            valor = frame["valor"].get().strip()
            if concepto and valor:
                lista_servicios.append({"nombre": concepto, "valor": valor})

        # 4. Obtener tipo de documento
        tipo_doc_seleccionado = self.tipo_documento.get()

        # 5. Llamar a on_submit con los datos correctos y simplificados
        # Ya no necesitamos pasar clases, wrappers, ni nada complejo.
        on_submit(
            entries=self.entries,
            datos_empresa=self.datos_empresa,
            tipo_documento=tipo_doc_seleccionado,
            servicios=lista_servicios,
            item_frames=self.item_frames, # Pasamos los frames por si se necesita para la validación
            proveedor=nombre_proveedor,
            cliente=nombre_cliente,
            descripcion_trabajo=descripcion_texto # <-- CORRECCIÓN CLAVE: Pasamos el texto directamente
        )

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Generador de Documentos")
    FormularioDocumento(root)
    root.mainloop()