# model/recibo.py

class Recibo:
    def __init__(self, recibo_id, cliente_id, periodo_anyo, periodo_mes,
                 fecha_generacion, importe, estado="pendiente"):
        self.recibo_id = recibo_id
        self.cliente_id = cliente_id
        self.periodo_anyo = periodo_anyo
        self.periodo_mes = periodo_mes
        self.fecha_generacion = fecha_generacion
        self.importe = importe
        self.estado = estado  # 'pendiente' o 'pagado'

    def __repr__(self):
        return (f"<Recibo {self.recibo_id} - Cliente {self.cliente_id} - "
                f"{self.periodo_mes}/{self.periodo_anyo} ({self.estado})>")
