import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'documentos'))

import tkinter as tk
from tkinter import ttk, messagebox
from utilidades import on_submit, obtener_proveedor_por_id, obtener_cliente_por_id

class FormularioDocumento:
    def __init__(self, parent):
        self.entries = {}
        self.servicios = []
        self.item_frames = []
        self.tipo_documento = tk.StringVar(value="Orden de Trabajo")

        self.datos_empresa = {
            "Nombre": "Sociedad Gardner y Esteffan LTDA",
            "Dirección": "Van Buren 208",
            "Ciudad": "Copiapó",
            "Teléfono": "77.703.720-k",
            "Correo Electrónico": "claudioesteffan@gmail.com"
        }

        self.frame_principal = ttk.Frame(parent, padding="10")
        self.frame_principal.pack(fill="both", expand=True)

        self._crear_campos_principales()
        self._crear_campo_descripcion()
        self._crear_items()
        self._crear_tipo_documento()
        self._crear_ids()

        ttk.Button(self.frame_principal, text="Generar PDF", command=self._generar_pdf).pack(pady=10)

    def _crear_campos_principales(self):
        campos = [
            "Número de Orden", "Correo Electrónico", "Fecha de Emisión",
            "Responsable de la Orden", "Fecha de Inicio",
            "Fecha Estimada de Finalización", "Proveedor"
        ]
        for campo in campos:
            frame = ttk.Frame(self.frame_principal)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text=campo + ": ", width=30, anchor="w").pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(side="left", fill="x", expand=True)
            self.entries[campo] = entry

    def _crear_campo_descripcion(self):
        frame_desc = ttk.LabelFrame(self.frame_principal, text="Descripción del Trabajo")
        frame_desc.pack(fill="both", pady=5)
        self.descripcion_text = tk.Text(frame_desc, height=5)
        self.descripcion_text.pack(fill="both", expand=True)

    def _crear_items(self):
        self.frame_items = ttk.LabelFrame(self.frame_principal, text="Ítems de la Orden")
        self.frame_items.pack(fill="x", pady=5)
        boton_item = ttk.Button(self.frame_principal, text="Agregar Ítem", command=self._agregar_item)
        boton_item.pack(pady=5)

    def _agregar_item(self):
        frame = ttk.Frame(self.frame_items)
        frame.pack(fill="x", pady=2)
        concepto = ttk.Entry(frame)
        concepto.pack(side="left", fill="x", expand=True)
        valor = ttk.Entry(frame, width=10)
        valor.pack(side="left", padx=5)
        self.item_frames.append((concepto, valor))

    def _crear_tipo_documento(self):
        frame_tipo = ttk.LabelFrame(self.frame_principal, text="Tipo de Documento")
        frame_tipo.pack(fill="x", pady=5)
        for tipo in ["Orden de Trabajo", "Orden de Compra", "Factura"]:
            ttk.Radiobutton(
                frame_tipo, text=tipo, variable=self.tipo_documento, value=tipo
            ).pack(side="left", padx=5)

    def _crear_ids(self):
        frame_id_prov = ttk.Frame(self.frame_principal)
        frame_id_prov.pack(fill="x", pady=2)
        ttk.Label(frame_id_prov, text="ID Proveedor:", width=30).pack(side="left")
        self.entry_id_proveedor = ttk.Entry(frame_id_prov)
        self.entry_id_proveedor.pack(side="left", fill="x", expand=True)

        frame_id_cli = ttk.Frame(self.frame_principal)
        frame_id_cli.pack(fill="x", pady=2)
        ttk.Label(frame_id_cli, text="ID Cliente:", width=30).pack(side="left")
        self.entry_id_cliente = ttk.Entry(frame_id_cli)
        self.entry_id_cliente.pack(side="left", fill="x", expand=True)

    def _generar_pdf(self):
        self.entries["ID Proveedor"] = self.entry_id_proveedor
        self.entries["ID Cliente"] = self.entry_id_cliente
        descripcion = self.descripcion_text.get("1.0", "end-1c").strip()
        if not descripcion:
            self.descripcion_text.focus_set()
            self.descripcion_text.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            messagebox.showwarning("Campo requerido", "El campo 'Descripción del Trabajo' no puede estar vacío.")
            self.descripcion_text.after(2000, lambda: self.descripcion_text.config(highlightthickness=0))
            return

        if self.tipo_documento.get() == "Orden de Trabajo":
            from documentos.orden_trabajo import OrdenTrabajo as DocumentoSeleccionado
        elif self.tipo_documento.get() == "Orden de Compra":
            from documentos.orden_compra import OrdenCompra as DocumentoSeleccionado
        elif self.tipo_documento.get() == "Factura":
            from documentos.factura import Factura as DocumentoSeleccionado

        on_submit(
            {**self.entries, "descripcion": descripcion},
            self.datos_empresa,
            self.tipo_documento.get(),
            self.servicios,
            [(c.get(), v.get()) for c, v in self.item_frames if c.get() and v.get()],
            obtener_proveedor_por_id(self.entry_id_proveedor.get().strip()),
            obtener_cliente_por_id(self.entry_id_cliente.get().strip()),
            DocumentoSeleccionado
        )


def iniciar_interfaz():
    root = tk.Tk()
    root.title("Generador de Órdenes de Trabajo")
    formulario = FormularioDocumento(root)
    root.mainloop()
