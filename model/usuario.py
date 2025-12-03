# model/usuario.py

class Usuario:
    def __init__(self, usuario_id, username, password_hash, rol="admin"):
        self.usuario_id = usuario_id
        self.username = username
        self.password_hash = password_hash
        self.rol = rol

    def __repr__(self):
        return f"<Usuario {self.usuario_id} - {self.username} ({self.rol})>"
