# view/aparato_view.py

from controller.aparato_controller import (
    listar_aparatos,
    crear_aparato,
    obtener_aparato_por_id,
    actualizar_aparato,
    eliminar_aparato,
)


def menu_aparatos():
    while True:
        print("\n--- GESTIÓN DE APARATOS ---")
        print("1. Listar aparatos")
        print("2. Crear aparato")
        print("3. Editar aparato")
        print("4. Eliminar aparato")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "1":
            mostrar_aparatos()
        elif opcion == "2":
            alta_aparato()
        elif opcion == "3":
            editar_aparato()
        elif opcion == "4":
            borrar_aparato()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def mostrar_aparatos():
    print("\n[Listado de aparatos]")
    aparatos = listar_aparatos()
    if not aparatos:
        print("No hay aparatos registrados.")
        return

    for a in aparatos:
        print(f"[{a.aparato_id}] {a.codigo} - {a.tipo} ({a.descripcion})")


def alta_aparato():
    print("\n[Alta de aparato]")
    codigo = input("Código: ").strip()
    tipo = input("Tipo: ").strip()
    descripcion = input("Descripción (opcional): ").strip() or None

    try:
        aparato = crear_aparato(codigo, tipo, descripcion)
        print(f"✅ Aparato creado con ID {aparato.aparato_id}")
    except Exception as e:
        print(f"❌ Error al crear aparato: {e}")


def editar_aparato():
    print("\n[Editar aparato]")
    try:
        aparato_id = int(input("ID de aparato a editar: ").strip())
    except ValueError:
        print("ID no válido.")
        return

    aparato = obtener_aparato_por_id(aparato_id)
    if not aparato:
        print("Aparato no encontrado.")
        return

    print(f"Editando aparato [{aparato.aparato_id}] {aparato.codigo} - {aparato.tipo}")
    nuevo_codigo = input(f"Código ({aparato.codigo}): ").strip() or aparato.codigo
    nuevo_tipo = input(f"Tipo ({aparato.tipo}): ").strip() or aparato.tipo
    nueva_descripcion = input(f"Descripción ({aparato.descripcion or ''}): ").strip() or aparato.descripcion

    ok = actualizar_aparato(aparato_id, nuevo_codigo, nuevo_tipo, nueva_descripcion)
    if ok:
        print("✅ Aparato actualizado.")
    else:
        print("No se actualizó ningún registro.")


def borrar_aparato():
    print("\n[Eliminar aparato]")
    try:
        aparato_id = int(input("ID de aparato a eliminar: ").strip())
    except ValueError:
        print("ID no válido.")
        return

    confirm = input("¿Estás seguro? (s/n): ").strip().lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    ok = eliminar_aparato(aparato_id)
    if ok:
        print("✅ Aparato eliminado.")
    else:
        print("No se eliminó el aparato (puede que no exista).")
