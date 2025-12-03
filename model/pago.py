# model/pago.py

class Pago:
    def __init__(self, pago_id, recibo_id, fecha_pago, metodo=None, referencia=None):
        self.pago_id = pago_id
        self.recibo_id = recibo_id
        self.fecha_pago = fecha_pago
        self.metodo = metodo       # ej: 'efectivo', 'tarjeta'
        self.referencia = referencia

    def __repr__(self):
        return f"<Pago {self.pago_id} - Recibo {self.recibo_id} - {self.fecha_pago}>"
