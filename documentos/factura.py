from documentos.base_documento import BaseDocumento

class Factura(BaseDocumento):
    def __init__(self, datos):
        super().__init__(datos)
        self.cliente = datos.get('cliente') # Atributo específico para la factura

    def generar_representacion(self):
        # Este método es un ejemplo, la lógica de PDF se maneja en otro lado.
        total_str = f"${self.calcular_total():,.2f}"

        representacion = f"FACTURA Nº {self.numero}\n"
        representacion += f"Cliente: {self.cliente}\n"
        representacion += f"Fecha de Emisión: {self.fecha_emision}\n\n"
        representacion += "Detalle de Productos o Servicios:\n"
        for item in self.items:
            valor_item = f"${float(item.get('valor', 0)):.2f}"
            representacion += f" - {item.get('nombre', 'N/A')}: {valor_item}\n"
        representacion += f"\nTotal: {total_str}\n"
        return representacion