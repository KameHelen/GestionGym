# controller/pago_controller.py

from datetime import date
from model.conexion import crear_conexion
from model.pago import Pago
from .recibo_controller import marcar_recibo_como_pagado


def registrar_pago(recibo_id: int, fecha_pago: str | None = None,
                   metodo: str | None = None, referencia: str | None = None):
    """
    Registra un pago para un recibo concreto.
    También marca el recibo como 'pagado'.
    Devuelve un objeto Pago.
    """
    if fecha_pago is None:
        fecha_pago = date.today().isoformat()

    conn = crear_conexion()
    if conn is None:
        raise RuntimeError("No se pudo conectar a la base de datos.")

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Pago (recibo_id, fecha_pago, metodo, referencia)
                VALUES (?, ?, ?, ?);
                """,
                (recibo_id, fecha_pago, metodo, referencia)
            )
            pago_id = cursor.lastrowid

        # Marcar el recibo como pagado
        marcar_recibo_como_pagado(recibo_id)

        return Pago(pago_id, recibo_id, fecha_pago, metodo, referencia)
    finally:
        conn.close()


def listar_pagos_cliente(cliente_id: int):
    """
    Devuelve una lista de Pagos asociados a un cliente.
    (buscamos pagos a través de sus recibos)
    """
    conn = crear_conexion()
    if conn is None:
        return []

    pagos = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.*
            FROM Pago p
            JOIN Recibo r ON p.recibo_id = r.recibo_id
            WHERE r.cliente_id = ?
            ORDER BY p.fecha_pago DESC;
            """,
            (cliente_id,)
        )
        filas = cursor.fetchall()
        for fila in filas:
            pagos.append(
                Pago(
                    pago_id=fila["pago_id"],
                    recibo_id=fila["recibo_id"],
                    fecha_pago=fila["fecha_pago"],
                    metodo=fila["metodo"],
                    referencia=fila["referencia"],
                )
            )
    finally:
        conn.close()

    return pagos
