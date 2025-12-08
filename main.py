# main.py

from model.conexion import crear_tablas
from controller.aparato_controller import inicializar_aparatos_por_defecto, listar_aparatos
from controller.auth_controller import crear_admin_si_no_existe, autenticar_usuario
from controller.cliente_controller import crear_cliente, listar_clientes
from controller.sesion_controller import crear_sesion, listar_sesiones_dia


# ---------------- LOGIN ----------------

def login():
    print("\n==== LOGIN ====")
    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()

    usuario = autenticar_usuario(username, password)
    if usuario:
        print(f"Bienvenido, {usuario.username}!")
        return usuario
    else:
        print("❌ Credenciales incorrectas")
        return None


# ---------------- MENÚ PRINCIPAL ----------------

def menu_principal(usuario):
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Listar aparatos")
        print("2. Crear cliente")
        print("3. Listar clientes")
        print("4. Crear sesión (reserva)")
        print("5. Listar sesiones de un día")
        print("0. Salir")

        opcion = input("> ")

        if opcion == "1":
            menu_listar_aparatos()

        elif opcion == "2":
            menu_crear_cliente()

        elif opcion == "3":
            menu_listar_clientes()

        elif opcion == "4":
            menu_crear_sesion(usuario)

        elif opcion == "5":
            menu_listar_sesiones()

        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")


# ---------------- OPCIONES ----------------

def menu_listar_aparatos():
    print("\n--- LISTA DE APARATOS ---")
    aparatos = listar_aparatos()
    for a in aparatos:
        print(f"[{a.aparato_id}] {a.codigo} - {a.tipo} ({a.descripcion})")


def menu_crear_cliente():
    print("\n--- CREAR CLIENTE ---")
    dni = input("DNI: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    email = input("Email: ")
    telefono = input("Teléfono: ")
    fecha_alta = input("Fecha alta (YYYY-MM-DD): ")

    try:
        cliente = crear_cliente(dni, nombre, apellido, email, telefono, fecha_alta)
        print(f"Cliente creado correctamente con ID {cliente.cliente_id}")
    except Exception as e:
        print(f"❌ Error creando el cliente: {e}")


def menu_listar_clientes():
    print("\n--- LISTA DE CLIENTES ---")
    clientes = listar_clientes()
    for c in clientes:
        print(f"[{c.cliente_id}] {c.nombre} {c.apellido} - DNI: {c.dni}")


def menu_crear_sesion(usuario):
    print("\n--- CREAR SESIÓN (RESERVA) ---")
    try:
        aparato_id = int(input("ID aparato: "))
        cliente_id = int(input("ID cliente: "))
        fecha = input("Fecha (YYYY-MM-DD): ")
        hora = input("Hora (HH:MM, 00 o 30 min): ")

        sesion = crear_sesion(aparato_id, cliente_id, fecha, hora, usuario.usuario_id)
        print(f"Sesión creada con ID {sesion.sesion_id}")

    except Exception as e:
        print(f"❌ No se pudo crear la sesión: {e}")


def menu_listar_sesiones():
    print("\n--- SESIONES DE UN DÍA ---")
    fecha = input("Fecha (YYYY-MM-DD): ")
    sesiones = listar_sesiones_dia(fecha)

    if not sesiones:
        print("No hay sesiones para ese día.")
        return

    for s in sesiones:
        print(f"[{s.sesion_id}] Aparato {s.aparato_id} "
              f"Cliente {s.cliente_id} {s.fecha} {s.hora_inicio}")


# ---------------- MAIN ----------------

def main():
    print("Inicializando sistema...")

    # 1. Crear tablas
    crear_tablas()

    # 2. Insertar aparatos por defecto
    inicializar_aparatos_por_defecto()

    # 3. Crear admin si no existe
    crear_admin_si_no_existe()

    # 4. Login
    usuario = None
    while usuario is None:
        usuario = login()

    # 5. Menú principal
    menu_principal(usuario)


if __name__ == "__main__":
    main()
