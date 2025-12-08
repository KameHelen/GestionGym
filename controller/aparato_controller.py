# controller/aparato_controller.py

from model.conexion import crear_conexion
from model.aparato import Aparato


def inicializar_aparatos_por_defecto():
    """
    Inserta los aparatos por defecto solo si la tabla Aparato está vacía.
    Se debe llamar al inicio del programa.
    """
    conn = crear_conexion()
    if conn is None:
        print("No se pudo conectar a la base de datos. No se inicializan aparatos.")
        return

    try:
        cursor = conn.cursor()

        # Comprobar cuántos aparatos hay ya
        cursor.execute("SELECT COUNT(*) AS total FROM Aparato;")
        fila = cursor.fetchone()
        total = fila[0] if fila is not None else 0

        if total > 0:
            print(f"La tabla Aparato ya tiene {total} registros. No se insertan aparatos por defecto.")
            return

        # Insertar los aparatos por defecto
        for codigo, tipo, descripcion in Aparato.APARATOS_POR_DEFECTO:
            cursor.execute(
                "INSERT INTO Aparato (codigo, tipo, descripcion) VALUES (?, ?, ?);",
                (codigo, tipo, descripcion)
            )

        conn.commit()
        print("Aparatos por defecto insertados correctamente.")

    except Exception as e:
        print(f"Error al inicializar aparatos por defecto: {e}")
    finally:
        conn.close()


def crear_aparato(codigo, tipo, descripcion=None):
    """Crea un nuevo aparato y devuelve un objeto Aparato."""
    conn = crear_conexion()
    if conn is None:
        raise RuntimeError("No se pudo conectar a la base de datos.")

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Aparato (codigo, tipo, descripcion) VALUES (?, ?, ?);",
                (codigo, tipo, descripcion)
            )
            aparato_id = cursor.lastrowid
        return Aparato(aparato_id, codigo, tipo, descripcion)
    finally:
        conn.close()


def listar_aparatos():
    """Devuelve una lista de objetos Aparato con todos los registros."""
    conn = crear_conexion()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return []

    aparatos = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aparato_id, codigo, tipo, descripcion FROM Aparato ORDER BY tipo, codigo;"
        )
        filas = cursor.fetchall()

        for fila in filas:
            aparatos.append(
                Aparato(
                    aparato_id=fila["aparato_id"],
                    codigo=fila["codigo"],
                    tipo=fila["tipo"],
                    descripcion=fila["descripcion"]
                )
            )
    except Exception as e:
        print(f"Error al listar aparatos: {e}")
    finally:
        conn.close()

    return aparatos


def obtener_aparato_por_id(aparato_id):
    """Devuelve un objeto Aparato por su ID, o None si no existe."""
    conn = crear_conexion()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aparato_id, codigo, tipo, descripcion FROM Aparato WHERE aparato_id = ?;",
            (aparato_id,)
        )
        fila = cursor.fetchone()
        if fila is None:
            return None
        return Aparato(
            aparato_id=fila["aparato_id"],
            codigo=fila["codigo"],
            tipo=fila["tipo"],
            descripcion=fila["descripcion"]
        )
    finally:
        conn.close()


def actualizar_aparato(aparato_id, codigo, tipo, descripcion=None):
    """Actualiza un aparato existente. Devuelve True si se actualizó."""
    conn = crear_conexion()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Aparato
                SET codigo = ?, tipo = ?, descripcion = ?
                WHERE aparato_id = ?;
                """,
                (codigo, tipo, descripcion, aparato_id)
            )
            return cursor.rowcount > 0
    finally:
        conn.close()


def eliminar_aparato(aparato_id):
    """Elimina un aparato por ID. Devuelve True si se borró."""
    conn = crear_conexion()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Aparato WHERE aparato_id = ?;", (aparato_id,))
            return cursor.rowcount > 0
    finally:
        conn.close()
