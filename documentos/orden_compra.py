# Fichero: documentos/orden_compra.py

from documentos.base_documento import BaseDocumento

class OrdenCompra(BaseDocumento):
    def __init__(self, datos):
        super().__init__(datos)
        # El proveedor ya se inicializa en BaseDocumento, no se necesita más lógica aquí.

    def generar_representacion(self):
        # Este método es un ejemplo, la lógica de PDF se maneja en otro lado.
        total_str = f"${self.calcular_total():,.2f}"
        
        representacion = f"ORDEN DE COMPRA Nº {self.numero}\n"
        representacion += f"Proveedor: {self.proveedor}\n"
        representacion += f"Fecha de Emisión: {self.fecha_emision}\n\n"
        representacion += "Items:\n"
        for item in self.items:
            valor_item = f"${float(item.get('valor', 0)):.2f}"
            representacion += f" - {item.get('nombre', 'N/A')}: {valor_item}\n"
        representacion += f"\nTotal: {total_str}\n"
        return representacion