from documentos.base_documento import BaseDocumento

class OrdenCompra(BaseDocumento):
    def __init__(self, numero, proveedor, fecha_emision, items, datos_empresa):
        super().__init__(numero, fecha_emision, datos_empresa)
        self.proveedor = proveedor
        self.items = items  # Lista de tuplas o dicts con descripción y valor

    def calcular_total(self):
        return sum(item['valor'] for item in self.items)

    def generar_representacion(self):
        representacion = f"ORDEN DE COMPRA Nº {self.numero}\n"
        representacion += f"Proveedor: {self.proveedor}\n"
        representacion += f"Fecha de Emisión: {self.fecha_emision}\n\n"
        representacion += "Items:\n"
        for item in self.items:
            representacion += f" - {item['descripcion']}: ${item['valor']:.2f}\n"
        representacion += f"\nTotal: ${self.calcular_total():,.2f}\n"
        return representacion