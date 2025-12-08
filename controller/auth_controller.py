# controller/auth_controller.py

import hashlib
from model.conexion import crear_conexion
from model.usuario import Usuario


def _hash_password(password: str) -> str:
    """Devuelve el hash SHA256 de la contraseña."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def crear_admin_si_no_existe(
    username: str = "admin",
    password: str = "admin"
):
    """
    Crea un usuario admin por defecto si no existe ninguno con ese username.
    """
    conn = crear_conexion()
    if conn is None:
        print("No se pudo conectar a la base de datos. No se puede crear admin.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT usuario_id FROM Usuario WHERE username = ?;",
            (username,)
        )
        fila = cursor.fetchone()
        if fila is not None:
            # Ya existe
            return

        pwd_hash = _hash_password(password)
        with conn:
            cursor.execute(
                "INSERT INTO Usuario (username, password_hash, rol) VALUES (?, ?, 'admin');",
                (username, pwd_hash)
            )
        print(f"Usuario admin '{username}' creado con contraseña por defecto.")
    except Exception as e:
        print(f"Error al crear admin por defecto: {e}")
    finally:
        conn.close()


def autenticar_usuario(username: str, password: str):
    """
    Intenta autenticar un usuario.
    Devuelve un objeto Usuario si las credenciales son correctas, o None si no.
    """
    conn = crear_conexion()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return None

    try:
        cursor = conn.cursor()
        pwd_hash = _hash_password(password)
        cursor.execute(
            """
            SELECT usuario_id, username, password_hash, rol
            FROM Usuario
            WHERE username = ? AND password_hash = ?;
            """,
            (username, pwd_hash)
        )
        fila = cursor.fetchone()
        if fila is None:
            return None

        return Usuario(
            usuario_id=fila["usuario_id"],
            username=fila["username"],
            password_hash=fila["password_hash"],
            rol=fila["rol"]
        )
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
        return None
    finally:
        conn.close()
