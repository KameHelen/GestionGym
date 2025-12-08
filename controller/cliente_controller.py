# controller/cliente_controller.py

from model.conexion import crear_conexion
from model.cliente import Cliente


def crear_cliente(dni, nombre, apellido, email=None, telefono=None, fecha_alta=None):
    """
    Crea un nuevo cliente en la base de datos y devuelve un objeto Cliente.
    Lanza ValueError si faltan campos obligatorios.
    """
    if not dni or not nombre or not apellido or not fecha_alta:
        raise ValueError("DNI, nombre, apellido y fecha de alta son obligatorios.")

    conn = crear_conexion()
    if conn is None:
        raise RuntimeError("No se pudo conectar a la base de datos.")

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Cliente (dni, nombre, apellido, email, telefono, fecha_alta)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (dni, nombre, apellido, email, telefono, fecha_alta)
            )
            cliente_id = cursor.lastrowid

        return Cliente(cliente_id, dni, nombre, apellido, email, telefono, fecha_alta)
    finally:
        conn.close()


def listar_clientes():
    """
    Devuelve una lista de objetos Cliente con todos los registros de la tabla.
    """
    conn = crear_conexion()
    if conn is None:
        return []

    clientes = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT cliente_id, dni, nombre, apellido, email, telefono, fecha_alta
            FROM Cliente
            ORDER BY apellido, nombre;
            """
        )
        filas = cursor.fetchall()
        for fila in filas:
            clientes.append(
                Cliente(
                    cliente_id=fila["cliente_id"],
                    dni=fila["dni"],
                    nombre=fila["nombre"],
                    apellido=fila["apellido"],
                    email=fila["email"],
                    telefono=fila["telefono"],
                    fecha_alta=fila["fecha_alta"]
                )
            )
    finally:
        conn.close()

    return clientes


def obtener_cliente_por_id(cliente_id: int):
    """
    Devuelve un objeto Cliente por su ID, o None si no existe.
    """
    conn = crear_conexion()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT cliente_id, dni, nombre, apellido, email, telefono, fecha_alta
            FROM Cliente
            WHERE cliente_id = ?;
            """,
            (cliente_id,)
        )
        fila = cursor.fetchone()
        if fila is None:
            return None

        return Cliente(
            cliente_id=fila["cliente_id"],
            dni=fila["dni"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            email=fila["email"],
            telefono=fila["telefono"],
            fecha_alta=fila["fecha_alta"]
        )
    finally:
        conn.close()


def obtener_cliente_por_dni(dni: str):
    """
    Devuelve un objeto Cliente buscando por DNI, o None si no existe.
    Útil para evitar clientes duplicados.
    """
    conn = crear_conexion()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT cliente_id, dni, nombre, apellido, email, telefono, fecha_alta
            FROM Cliente
            WHERE dni = ?;
            """,
            (dni,)
        )
        fila = cursor.fetchone()
        if fila is None:
            return None

        return Cliente(
            cliente_id=fila["cliente_id"],
            dni=fila["dni"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            email=fila["email"],
            telefono=fila["telefono"],
            fecha_alta=fila["fecha_alta"]
        )
    finally:
        conn.close()


def actualizar_cliente(cliente_id: int, dni, nombre, apellido,
                       email=None, telefono=None, fecha_alta=None):
    """
    Actualiza los datos de un cliente.
    Devuelve True si se actualizó alguna fila, False si no existía.
    """
    if not dni or not nombre or not apellido:
        raise ValueError("DNI, nombre y apellido son obligatorios.")

    conn = crear_conexion()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Cliente
                SET dni = ?, nombre = ?, apellido = ?, email = ?, telefono = ?, fecha_alta = ?
                WHERE cliente_id = ?;
                """,
                (dni, nombre, apellido, email, telefono, fecha_alta, cliente_id)
            )
            return cursor.rowcount > 0
    finally:
        conn.close()


def eliminar_cliente(cliente_id: int):
    """
    Elimina un cliente por ID.
    OJO: si tiene sesiones o recibos relacionados, la FK puede impedirlo
    según la configuración (aquí usamos ON DELETE CASCADE en algunas tablas).
    Devuelve True si se eliminó alguna fila.
    """
    conn = crear_conexion()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Cliente WHERE cliente_id = ?;",
                (cliente_id,)
            )
            return cursor.rowcount > 0
    finally:
        conn.close()
