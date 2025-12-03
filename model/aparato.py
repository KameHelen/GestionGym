# model/aparato.py

class Aparato:
    # Lista de aparatos por defecto para inicializar la BD
    # (codigo, tipo, descripcion)
    APARATOS_POR_DEFECTO = [
        ("CINTA01", "Cinta de correr", "Cinta de correr profesional"),
        ("CINTA02", "Cinta de correr", "Cinta de correr estándar"),
        ("ELIP01", "Elíptica", "Máquina elíptica con pantalla"),
        ("BICI01", "Bicicleta estática", "Bicicleta estática reclinada"),
        ("BICI02", "Bicicleta estática", "Bicicleta de spinning"),
        ("PRES01", "Press banca", "Banco de press con barra"),
        ("MULT01", "Multigimnasio", "Estación multifunción"),
        ("REMO01", "Remo", "Máquina de remo"),
    ]

    def __init__(self, aparato_id, codigo, tipo, descripcion=None):
        self.aparato_id = aparato_id
        self.codigo = codigo
        self.tipo = tipo
        self.descripcion = descripcion

    def __repr__(self):
        return f"<Aparato {self.aparato_id} - {self.tipo} ({self.codigo})>"
