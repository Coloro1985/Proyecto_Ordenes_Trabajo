from documentos.base_documento import BaseDocumento

class OrdenTrabajo(BaseDocumento):
    def __init__(self, numero_orden, proveedor, responsable, fecha_emision, fecha_inicio, fecha_fin, descripcion, items):
        super().__init__(numero_orden, proveedor, responsable, fecha_emision, descripcion, items)
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def obtener_datos_especificos(self):
        return {
            "Fecha de Inicio": self.fecha_inicio,
            "Fecha de Fin Estimada": self.fecha_fin
        }

    def tipo_documento(self):
        return "Orden de Trabajo"