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


def obtener_estado_pagos_mes(anyo: int, mes: int):
    """
    Devuelve una lista de diccionarios con el estado de pago de TODOS los clientes
    para el mes/año dado.
    Si no existe recibo, se considera 'pendiente' (virtual).
    """
    conn = crear_conexion()
    if conn is None:
        return []

    resultados = []
    try:
        cursor = conn.cursor()
        # LEFT JOIN de Cliente a Recibo filtrando por el mes/año especifico en el JOIN
        # OJO: Para hacer el left join correctamente con filtros en la tabla derecha,
        # necesitamos mover las condiciones de Recibo al ON o usar subquery.
        # SQLite soporta condiciones complejas en ON.
        
        query = """
            SELECT 
                c.cliente_id, c.nombre, c.apellido, c.dni,
                r.recibo_id, r.importe, r.estado
            FROM Cliente c
            LEFT JOIN Recibo r ON c.cliente_id = r.cliente_id 
                               AND r.periodo_anyo = ? 
                               AND r.periodo_mes = ?
            ORDER BY c.apellido, c.nombre;
        """
        cursor.execute(query, (anyo, mes))
        filas = cursor.fetchall()
        
        for fila in filas:
            estado = fila["estado"] if fila["estado"] else "pendiente"
            importe = fila["importe"] if fila["importe"] is not None else 40.0 # Default sugerido
            
            resultados.append({
                "cliente_id": fila["cliente_id"],
                "nombre": fila["nombre"],
                "apellido": fila["apellido"],
                "dni": fila["dni"],
                "recibo_id": fila["recibo_id"], # Puede ser None
                "importe": importe,
                "estado": estado
            })
    finally:
        conn.close()

    return resultados


def exportar_morosos_pdf(anyo: int, mes: int) -> str:
    """
    Genera un PDF con la lista de morosos (estado 'pendiente') para el mes indicado.
    Usa obtener_estado_pagos_mes para determinar quién debe.
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    
    todos = obtener_estado_pagos_mes(anyo, mes)
    # Filtrar solo 'pendiente'
    morosos = [c for c in todos if c['estado'] == 'pendiente']
    
    filename = f"morosos_{anyo}_{mes}.pdf"
    
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Listado de Morosos - GymForTheMoment")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Periodo: {mes}/{anyo}")
    
    # Tabla
    y = height - 100
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "ID")
    c.drawString(100, y, "Nombre")
    c.drawString(300, y, "DNI")
    c.drawString(450, y, "Deuda (Est.)")
    
    y -= 20
    c.setFont("Helvetica", 10)
    
    if not morosos:
        c.drawString(50, y, "No hay morosos para este periodo. ¡Todo pagado!")
    
    for m in morosos:
        if y < 50:
            c.showPage()
            y = height - 50
        
        c.drawString(50, y, str(m['cliente_id']))
        c.drawString(100, y, f"{m['nombre']} {m['apellido']}")
        c.drawString(300, y, m['dni'])
        c.drawString(450, y, f"{m['importe']} €")
        y -= 15
        
    c.save()
    return filename


def generar_recibo_individual(cliente_id: int, anyo: int, mes: int, importe: float) -> int | None:
    """
    Genera un único recibo para un cliente específico.
    Devuelve el ID del recibo creado, o None si error.
    """
    from model.conexion import crear_conexion # Ensure import if needed, though usually at top
    conn = crear_conexion()
    if conn is None:
        return None

    try:
        with conn:
            cursor = conn.cursor()
            fecha_generacion = date.today().isoformat()
            cursor.execute(
                """
                INSERT INTO Recibo (cliente_id, periodo_anyo, periodo_mes,
                                    fecha_generacion, importe, estado)
                VALUES (?, ?, ?, ?, ?, 'pendiente');
                """,
                (cliente_id, anyo, mes, fecha_generacion, importe)
            )
            return cursor.lastrowid
    except Exception as e:
        print(f"Error generando recibo individual: {e}")
        return None
    finally:
        conn.close()


def marcar_recibo_como_pagado(recibo_id: int):
    """
    Marca un recibo como pagado (solo cambia estado).
    El registro de pago como tal lo hace pago_controller.registrar_pago().
    """
    from model.conexion import crear_conexion # Ensure import if needed
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

