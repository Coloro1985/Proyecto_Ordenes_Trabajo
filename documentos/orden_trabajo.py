from documentos.base_documento import BaseDocumento

class OrdenTrabajo(BaseDocumento):
    def __init__(self, datos):
        super().__init__(datos)
        # Extrae las fechas específicas para la orden de trabajo
        fechas = datos.get('fechas_importantes', {})
        self.fecha_inicio = fechas.get("Fecha de Inicio")
        self.fecha_fin = fechas.get("Fecha Estimada de Finalización")

    def obtener_datos_especificos(self):
        datos = {
            "Fecha de inicio": self.fecha_inicio,
            "Fecha de fin": self.fecha_fin
        }
        print("[DEBUG] Datos específicos de OrdenTrabajo:", datos)
        return datos

    def tipo_documento(self):
        return "Orden de Trabajo"