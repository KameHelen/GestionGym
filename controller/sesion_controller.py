# controller/sesion_controller.py

from datetime import datetime
from model.conexion import crear_conexion
from model.sesion import Sesion
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4



# ---------- VALIDACIONES DE NEGOCIO ----------

def es_fecha_laborable(fecha_str: str) -> bool:
    """
    Devuelve True si la fecha es de lunes a viernes.
    fecha_str: 'YYYY-MM-DD'
    """
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        # Monday=0, Sunday=6
        return fecha.weekday() < 5
    except ValueError:
        return False


def es_hora_valida(hora_str: str) -> bool:
    """
    Devuelve True si la hora está en formato HH:MM,
    minutos 00 o 30, y hora entre 00:00 y 23:30.
    """
    try:
        partes = hora_str.split(":")
        if len(partes) != 2:
            return False
        h = int(partes[0])
        m = int(partes[1])
        if h < 0 or h > 23:
            return False
        if m not in (0, 30):
            return False
        return True
    except Exception:
        return False


def hay_sesion_en_slot(aparato_id: int, fecha: str, hora_inicio: str) -> bool:
    """
    Devuelve True si ya existe una sesión para ese aparato, día y hora.
    """
    conn = crear_conexion()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM Sesion
            WHERE aparato_id = ? AND fecha = ? AND hora_inicio = ?;
            """,
            (aparato_id, fecha, hora_inicio)
        )
        fila = cursor.fetchone()
        total = fila[0] if fila is not None else 0
        return total > 0
    finally:
        conn.close()


# ---------- CRUD / OPERACIONES DE SESIONES ----------

def crear_sesion(aparato_id: int, cliente_id: int, fecha: str,
                 hora_inicio: str, created_by: int | None = None):
    """
    Crea una sesión de 30 minutos validando:
    - Fecha laborable (L-V)
    - Hora válida (HH:MM, 00 o 30, 00-23:30)
    - No solapamiento con otra sesión en mismo aparato/slot
    """
    if not es_fecha_laborable(fecha):
        raise ValueError("La fecha debe ser de lunes a viernes.")

    if not es_hora_valida(hora_inicio):
        raise ValueError("La hora no es válida. Usa formato HH:MM, minutos 00 o 30.")

    if hay_sesion_en_slot(aparato_id, fecha, hora_inicio):
        raise ValueError("Ya existe una sesión en ese aparato para ese día y franja.")

    conn = crear_conexion()
    if conn is None:
        raise RuntimeError("No se pudo conectar a la base de datos.")

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Sesion (aparato_id, cliente_id, fecha, hora_inicio, duracion, created_by)
                VALUES (?, ?, ?, ?, 30, ?);
                """,
                (aparato_id, cliente_id, fecha, hora_inicio, created_by)
            )
            sesion_id = cursor.lastrowid

        return Sesion(sesion_id, aparato_id, cliente_id, fecha, hora_inicio, 30, created_by)
    finally:
        conn.close()


def cancelar_sesion(sesion_id: int) -> bool:
    """
    Elimina una sesión (cancelación).
    Devuelve True si se eliminó alguna fila.
    (Aquí se podría implementar una política de cancelación más compleja).
    """
    conn = crear_conexion()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Sesion WHERE sesion_id = ?;", (sesion_id,))
            return cursor.rowcount > 0
    finally:
        conn.close()


def listar_sesiones_dia(fecha: str):
    """
    Devuelve una lista de Sesion para una fecha dada.
    """
    conn = crear_conexion()
    if conn is None:
        return []

    sesiones = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM Sesion
            WHERE fecha = ?
            ORDER BY aparato_id, hora_inicio;
            """,
            (fecha,)
        )
        filas = cursor.fetchall()
        for fila in filas:
            sesiones.append(
                Sesion(
                    sesion_id=fila["sesion_id"],
                    aparato_id=fila["aparato_id"],
                    cliente_id=fila["cliente_id"],
                    fecha=fila["fecha"],
                    hora_inicio=fila["hora_inicio"],
                    duracion=fila["duracion"],
                    created_by=fila["created_by"],
                )
            )
    finally:
        conn.close()

    return sesiones


def obtener_ocupacion_diaria(fecha: str):
    """
    Devuelve una lista de diccionarios con:
    aparato_id, codigo, tipo, cliente_id, nombre_cliente, hora_inicio
    para todas las sesiones de un día dado.
    Esto facilita que la vista pinte la ocupación por aparato.
    """
    conn = crear_conexion()
    if conn is None:
        return []

    resultados = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                s.sesion_id,
                s.aparato_id,
                a.codigo AS aparato_codigo,
                a.tipo AS aparato_tipo,
                s.cliente_id,
                c.nombre AS cliente_nombre,
                c.apellido AS cliente_apellido,
                s.fecha,
                s.hora_inicio
            FROM Sesion s
            JOIN Aparato a ON s.aparato_id = a.aparato_id
            JOIN Cliente c ON s.cliente_id = c.cliente_id
            WHERE s.fecha = ?
            ORDER BY a.tipo, a.codigo, s.hora_inicio;
            """,
            (fecha,)
        )
        filas = cursor.fetchall()
        for fila in filas:
            resultados.append(
                {
                    "sesion_id": fila["sesion_id"],
                    "aparato_id": fila["aparato_id"],
                    "aparato_codigo": fila["aparato_codigo"],
                    "aparato_tipo": fila["aparato_tipo"],
                    "cliente_id": fila["cliente_id"],
                    "cliente_nombre": fila["cliente_nombre"],
                    "cliente_apellido": fila["cliente_apellido"],
                    "fecha": fila["fecha"],
                    "hora_inicio": fila["hora_inicio"],
                }
            )
    finally:
        conn.close()

    return resultados


def exportar_sesiones_pdf(fecha: str) -> str:
    """
    Genera un PDF con el listado de sesiones para la fecha indicada.
    Devuelve el nombre del archivo generado.
    """
    ocupacion = obtener_ocupacion_diaria(fecha)
    filename = f"sesiones_{fecha}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Listado de Sesiones - GymForTheMoment")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Fecha: {fecha}")

    # Tabla (encabezados)
    y = height - 100
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Hora")
    c.drawString(100, y, "Aparato")
    c.drawString(250, y, "Tipo")
    c.drawString(350, y, "Cliente")

    y -= 20
    c.setFont("Helvetica", 10)

    for o in ocupacion:
        if y < 50:
            c.showPage()
            y = height - 50

        c.drawString(50, y, o['hora_inicio'])
        c.drawString(100, y, o['aparato_codigo'])
        c.drawString(250, y, o['aparato_tipo'])
        c.drawString(350, y, f"{o['cliente_nombre']} {o['cliente_apellido']}")
        y -= 15

    c.save()
    return filename

