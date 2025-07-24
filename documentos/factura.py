from documentos.base_documento import BaseDocumento

class Factura(BaseDocumento):
    def __init__(self, numero, cliente, fecha_emision, items, datos_empresa):
        super().__init__(numero, fecha_emision, datos_empresa)
        self.cliente = cliente
        self.items = items  # Lista de dicts con descripción y valor

    def calcular_total(self):
        return sum(item['valor'] for item in self.items)

    def generar_representacion(self):
        representacion = f"FACTURA Nº {self.numero}\n"
        representacion += f"Cliente: {self.cliente}\n"
        representacion += f"Fecha de Emisión: {self.fecha_emision}\n\n"
        representacion += "Detalle de Productos o Servicios:\n"
        for item in self.items:
            representacion += f" - {item['descripcion']}: ${item['valor']:.2f}\n"
        representacion += f"\nTotal: ${self.calcular_total():,.2f}\n"
        return representacion
