# view/sesion_view.py

from controller.sesion_controller import (
    crear_sesion,
    listar_sesiones_dia,
    cancelar_sesion,
    obtener_ocupacion_diaria,
)


def menu_reservas(usuario):
    while True:
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Crear sesión (reserva)")
        print("2. Listar sesiones de un día")
        print("3. Ver ocupación diaria (detallada)")
        print("4. Cancelar sesión")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "1":
            alta_sesion(usuario)
        elif opcion == "2":
            listar_sesiones()
        elif opcion == "3":
            ver_ocupacion_diaria()
        elif opcion == "4":
            cancelar_sesion_view()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def alta_sesion(usuario):
    print("\n[Crear sesión / reserva]")
    try:
        aparato_id = int(input("ID aparato: ").strip())
        cliente_id = int(input("ID cliente: ").strip())
    except ValueError:
        print("ID no válido.")
        return

    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    hora = input("Hora (HH:MM, minutos 00 o 30): ").strip()

    try:
        sesion = crear_sesion(aparato_id, cliente_id, fecha, hora, usuario.usuario_id)
        print(f"✅ Sesión creada con ID {sesion.sesion_id}")
    except Exception as e:
        print(f"❌ No se pudo crear la sesión: {e}")


def listar_sesiones():
    print("\n[Listar sesiones de un día]")
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    sesiones = listar_sesiones_dia(fecha)

    if not sesiones:
        print("No hay sesiones para esa fecha.")
        return

    for s in sesiones:
        print(f"[{s.sesion_id}] Aparato {s.aparato_id} - Cliente {s.cliente_id} - {s.fecha} {s.hora_inicio}")


def ver_ocupacion_diaria():
    print("\n[Ocupación diaria detallada]")
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    ocupacion = obtener_ocupacion_diaria(fecha)

    if not ocupacion:
        print("No hay sesiones para esa fecha.")
        return

    for o in ocupacion:
        print(
            f"[{o['sesion_id']}] {o['fecha']} {o['hora_inicio']} | "
            f"Aparato {o['aparato_codigo']} ({o['aparato_tipo']}) | "
            f"Cliente {o['cliente_id']} - {o['cliente_nombre']} {o['cliente_apellido']}"
        )


def cancelar_sesion_view():
    print("\n[Cancelar sesión]")
    try:
        sesion_id = int(input("ID de la sesión a cancelar: ").strip())
    except ValueError:
        print("ID no válido.")
        return

    ok = cancelar_sesion(sesion_id)
    if ok:
        print("✅ Sesión cancelada.")
    else:
        print("No se canceló ninguna sesión (puede que no exista).")
