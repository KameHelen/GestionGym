# model/conexion.py
import sqlite3
from pathlib import Path

# Ruta al fichero de base de datos (en la raíz del proyecto)
DB_PATH = Path("gestiongym.db")


def crear_conexion():
    """Crea una conexión a la base de datos."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)  # Usamos sqlite3.connect
        conn.row_factory = sqlite3.Row   # Para poder acceder a columnas por nombre
        conn.execute("PRAGMA foreign_keys = ON;")  # Activar claves foráneas
        print(f"Conexión a SQLite establecida: {DB_PATH}")
    except sqlite3.Error as e:  # Cambiamos Error por sqlite3.Error
        print(f"Error al conectar a la base de datos: {e}")
    return conn


def crear_tablas():
    """Crea las tablas necesarias en la base de datos (si no existen)."""
    conn = crear_conexion()
    if conn is None:
        print("No se pudo crear la conexión, no se crean tablas.")
        return

    try:
        cursor = conn.cursor()

        # Tabla Cliente
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Cliente (
                cliente_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                dni          TEXT UNIQUE NOT NULL,
                nombre       TEXT NOT NULL,
                apellido     TEXT NOT NULL,
                email        TEXT,
                telefono     TEXT,
                fecha_alta   TEXT NOT NULL
            );
            """
        )

        # Tabla Aparato
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Aparato (
                aparato_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo       TEXT UNIQUE,
                tipo         TEXT NOT NULL,
                descripcion  TEXT
            );
            """
        )

        # Tabla Usuario (admin)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Usuario (
                usuario_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                rol           TEXT NOT NULL CHECK (rol IN ('admin'))
            );
            """
        )

        # Tabla Sesion
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Sesion (
                sesion_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                aparato_id   INTEGER NOT NULL,
                cliente_id   INTEGER NOT NULL,
                fecha        TEXT NOT NULL,     -- 'YYYY-MM-DD'
                hora_inicio  TEXT NOT NULL,     -- 'HH:MM'
                duracion     INTEGER NOT NULL DEFAULT 30,
                created_by   INTEGER,
                FOREIGN KEY (aparato_id) REFERENCES Aparato(aparato_id) ON DELETE CASCADE,
                FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id) ON DELETE CASCADE,
                FOREIGN KEY (created_by) REFERENCES Usuario(usuario_id) ON DELETE SET NULL,
                UNIQUE (aparato_id, fecha, hora_inicio),
                CHECK (substr(hora_inicio, 4, 2) IN ('00', '30')),
                CHECK (CAST(substr(hora_inicio, 1, 2) AS INTEGER) BETWEEN 0 AND 23),
                CHECK (duracion = 30)
            );
            """
        )

        # Tabla Recibo
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Recibo (
                recibo_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id       INTEGER NOT NULL,
                periodo_anyo     INTEGER NOT NULL,
                periodo_mes      INTEGER NOT NULL, -- 1..12
                fecha_generacion TEXT NOT NULL,
                importe          REAL NOT NULL,
                estado           TEXT NOT NULL CHECK (estado IN ('pendiente', 'pagado')),
                FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id) ON DELETE CASCADE,
                UNIQUE (cliente_id, periodo_anyo, periodo_mes)
            );
            """
        )

        # Tabla Pago
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Pago (
                pago_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                recibo_id   INTEGER NOT NULL,
                fecha_pago  TEXT NOT NULL,
                metodo      TEXT,
                referencia  TEXT,
                FOREIGN KEY (recibo_id) REFERENCES Recibo(recibo_id) ON DELETE CASCADE
            );
            """
        )

        # Índices opcionales recomendados
        cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_pago_recibo ON Pago(recibo_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_sesion_aparato_fecha ON Sesion(aparato_id, fecha, hora_inicio);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_recibo_cliente_periodo ON Recibo(cliente_id, periodo_anyo, periodo_mes);"
        )

        conn.commit()
        print("Tablas creadas/verificadas correctamente.")
    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")
    finally:
        conn.close()
