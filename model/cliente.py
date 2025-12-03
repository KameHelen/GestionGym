# model/cliente.py

class Cliente:
    def __init__(self, cliente_id, dni, nombre, apellido, email=None, telefono=None, fecha_alta=None):
        self.cliente_id = cliente_id
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.fecha_alta = fecha_alta

    def __repr__(self):
        return f"<Cliente {self.cliente_id} - {self.nombre} {self.apellido}>"
