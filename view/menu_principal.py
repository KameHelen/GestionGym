# view/menu_principal.py

from view.cliente_view import menu_clientes
from view.aparato_view import menu_aparatos
from view.sesion_view import menu_reservas
from view.cobros_view import menu_cobros


def mostrar_menu_principal(usuario):
    while True:
        print("\n=== GESTIÓN GYM - MENÚ PRINCIPAL ===")
        print("1. Gestión de clientes")
        print("2. Gestión de aparatos")
        print("3. Gestión de reservas")
        print("4. Cobros y recibos")
        print("0. Salir")
        opcion = input("> ").strip()

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_aparatos()
        elif opcion == "3":
            menu_reservas(usuario)
        elif opcion == "4":
            menu_cobros()
        elif opcion == "0":
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción no válida.")
