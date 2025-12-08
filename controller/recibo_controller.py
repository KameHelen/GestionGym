# controller/recibo_controller.py

from datetime import date
from model.conexion import crear_conexion
from model.recibo import Recibo


def generar_recibos_mes(anyo: int, mes: int, importe_cuota: float):
    """
    Genera recibos para todos los clientes para un mes/año dado.
    No duplica recibos (gracias a la UNIQUE en (cliente_id, periodo_anyo, periodo_mes)).
    Devuelve el número de recibos creados.
    """
    conn = crear_conexion()
    if conn is None:
        raise RuntimeError("No se pudo conectar a la base de datos.")

    creados = 0
    try:
        cursor = conn.cursor()
        # Obtener todos los clientes
        cursor.execute("SELECT cliente_id FROM Cliente;")
        clientes = cursor.fetchall()

        fecha_generacion = date.today().isoformat()

        for fila in clientes:
            cliente_id = fila["cliente_id"]

            # Intentar insertar recibo, si ya existe, ignoramos el error
            try:
                cursor.execute(
                    """
                    INSERT INTO Recibo (cliente_id, periodo_anyo, periodo_mes,
                                        fecha_generacion, importe, estado)
                    VALUES (?, ?, ?, ?, ?, 'pendiente');
                    """,
                    (cliente_id, anyo, mes, fecha_generacion, importe_cuota)
                )
                creados += 1
            except Exception:
                # Probablemente ya existe un recibo para ese cliente y mes
                conn.rollback()
                # Reabrimos transacción para los siguientes
                cursor = conn.cursor()

        conn.commit()
    finally:
        conn.close()

    return creados


def listar_recibos_mes(anyo: int, mes: int):
    """Devuelve una lista de objetos Recibo para un mes/año concreto."""
    conn = crear_conexion()
    if conn is None:
        return []

    recibos = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM Recibo
            WHERE periodo_anyo = ? AND periodo_mes = ?
            ORDER BY cliente_id;
            """,
            (anyo, mes)
        )
        filas = cursor.fetchall()
        for fila in filas:
            recibos.append(
                Recibo(
                    recibo_id=fila["recibo_id"],
                    cliente_id=fila["cliente_id"],
                    periodo_anyo=fila["periodo_anyo"],
                    periodo_mes=fila["periodo_mes"],
                    fecha_generacion=fila["fecha_generacion"],
                    importe=fila["importe"],
                    estado=fila["estado"]
                )
            )
    finally:
        conn.close()

    return recibos


def listar_recibos_cliente(cliente_id: int):
    """Devuelve una lista de recibos de un cliente."""
    conn = crear_conexion()
    if conn is None:
        return []

    recibos = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM Recibo
            WHERE cliente_id = ?
            ORDER BY periodo_anyo DESC, periodo_mes DESC;
            """,
            (cliente_id,)
        )
        filas = cursor.fetchall()
        for fila in filas:
            recibos.append(
                Recibo(
                    recibo_id=fila["recibo_id"],
                    cliente_id=fila["cliente_id"],
                    periodo_anyo=fila["periodo_anyo"],
                    periodo_mes=fila["periodo_mes"],
                    fecha_generacion=fila["fecha_generacion"],
                    importe=fila["importe"],
                    estado=fila["estado"]
                )
            )
    finally:
        conn.close()

    return recibos


def obtener_morosos_mes(anyo: int, mes: int):
    """
    Devuelve una lista de clientes (id, nombre, apellido, dni) que tienen
    recibos 'pendiente' para ese mes/año.
    """
    conn = crear_conexion()
    if conn is None:
        return []

    morosos = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT c.cliente_id, c.nombre, c.apellido, c.dni
            FROM Cliente c
            JOIN Recibo r ON c.cliente_id = r.cliente_id
            WHERE r.periodo_anyo = ?
              AND r.periodo_mes = ?
              AND r.estado = 'pendiente'
            ORDER BY c.apellido, c.nombre;
            """,
            (anyo, mes)
        )
        filas = cursor.fetchall()
        for fila in filas:
            morosos.append(
                {
                    "cliente_id": fila["cliente_id"],
                    "nombre": fila["nombre"],
                    "apellido": fila["apellido"],
                    "dni": fila["dni"],
                }
            )
    finally:
        conn.close()

    return morosos


def marcar_recibo_como_pagado(recibo_id: int):
    """
    Marca un recibo como pagado (solo cambia estado).
    El registro de pago como tal lo hace pago_controller.registrar_pago().
    """
    conn = crear_conexion()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Recibo
                SET estado = 'pagado'
                WHERE recibo_id = ?;
                """,
                (recibo_id,)
            )
            return cursor.rowcount > 0
    finally:
        conn.close()
