# model/sesion.py

class Sesion:
    def __init__(self, sesion_id, aparato_id, cliente_id, fecha, hora_inicio,
                 duracion=30, created_by=None):
        self.sesion_id = sesion_id
        self.aparato_id = aparato_id
        self.cliente_id = cliente_id
        self.fecha = fecha            # 'YYYY-MM-DD'
        self.hora_inicio = hora_inicio  # 'HH:MM'
        self.duracion = duracion      # siempre 30 minutos
        self.created_by = created_by  # usuario_id del admin que la creó

    def __repr__(self):
        return (f"<Sesion {self.sesion_id} - Cliente {self.cliente_id} - "
                f"Aparato {self.aparato_id} {self.fecha} {self.hora_inicio}>")
