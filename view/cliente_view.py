# view/cliente_view.py

from controller.cliente_controller import (
    crear_cliente,
    listar_clientes,
    obtener_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente,
)


def menu_clientes():
    while True:
        print("\n--- GESTIÓN DE CLIENTES ---")
        print("1. Alta cliente")
        print("2. Listar clientes")
        print("3. Editar cliente")
        print("4. Eliminar cliente")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "1":
            alta_cliente()
        elif opcion == "2":
            mostrar_clientes()
        elif opcion == "3":
            editar_cliente()
        elif opcion == "4":
            borrar_cliente()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def alta_cliente():
    print("\n[Alta de cliente]")
    dni = input("DNI: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email (opcional): ").strip() or None
    telefono = input("Teléfono (opcional): ").strip() or None
    fecha_alta = input("Fecha de alta (YYYY-MM-DD): ").strip()

    try:
        cliente = crear_cliente(dni, nombre, apellido, email, telefono, fecha_alta)
        print(f"✅ Cliente creado con ID {cliente.cliente_id}")
    except Exception as e:
        print(f"❌ Error al crear cliente: {e}")


def mostrar_clientes():
    print("\n[Listado de clientes]")
    clientes = listar_clientes()
    if not clientes:
        print("No hay clientes registrados.")
        return

    for c in clientes:
        print(f"[{c.cliente_id}] {c.nombre} {c.apellido} - DNI: {c.dni}")


def editar_cliente():
    print("\n[Editar cliente]")
    try:
        cliente_id = int(input("ID de cliente a editar: ").strip())
    except ValueError:
        print("ID no válido.")
        return

    cliente = obtener_cliente_por_id(cliente_id)
    if not cliente:
        print("Cliente no encontrado.")
        return

    print(f"Editando cliente [{cliente.cliente_id}] {cliente.nombre} {cliente.apellido}")
    nuevo_dni = input(f"DNI ({cliente.dni}): ").strip() or cliente.dni
    nuevo_nombre = input(f"Nombre ({cliente.nombre}): ").strip() or cliente.nombre
    nuevo_apellido = input(f"Apellido ({cliente.apellido}): ").strip() or cliente.apellido
    nuevo_email = input(f"Email ({cliente.email or ''}): ").strip() or cliente.email
    nuevo_telefono = input(f"Teléfono ({cliente.telefono or ''}): ").strip() or cliente.telefono
    nueva_fecha_alta = input(f"Fecha alta ({cliente.fecha_alta}): ").strip() or cliente.fecha_alta

    try:
        ok = actualizar_cliente(
            cliente_id,
            nuevo_dni,
            nuevo_nombre,
            nuevo_apellido,
            nuevo_email,
            nuevo_telefono,
            nueva_fecha_alta,
        )
        if ok:
            print("✅ Cliente actualizado.")
        else:
            print("No se actualizó ningún registro.")
    except Exception as e:
        print(f"❌ Error al actualizar cliente: {e}")


def borrar_cliente():
    print("\n[Eliminar cliente]")
    try:
        cliente_id = int(input("ID de cliente a eliminar: ").strip())
    except ValueError:
        print("ID no válido.")
        return

    confirm = input("¿Estás seguro? (s/n): ").strip().lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    ok = eliminar_cliente(cliente_id)
    if ok:
        print("✅ Cliente eliminado.")
    else:
        print("No se eliminó el cliente (puede que no exista).")
