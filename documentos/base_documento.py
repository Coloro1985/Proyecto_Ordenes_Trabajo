
class BaseDocumento:
    def __init__(self, numero, fecha_emision, responsable, fecha_inicio, fecha_fin, proveedor, descripcion_trabajo, items):
        self.numero = numero
        self.fecha_emision = fecha_emision
        self.responsable = responsable
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.proveedor = proveedor
        self.descripcion_trabajo = descripcion_trabajo
        self.items = items  # Se espera que sea una lista de diccionarios con claves 'nombre' y 'valor'

    def calcular_total(self):
        return sum(item.get('valor', 0) for item in self.items)

    def a_dict(self):
        return {
            'clase': self.__class__.__name__,  # Referencia explícita al nombre de la clase para claridad semántica
            'numero': self.numero,
            'fecha_emision': self.fecha_emision,
            'responsable': self.responsable,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'proveedor': self.proveedor,
            'descripcion_trabajo': self.descripcion_trabajo,
            'items': self.items,
            'total': self.calcular_total()
        }