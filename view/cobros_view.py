# view/cobros_view.py

from controller.recibo_controller import (
    generar_recibos_mes,
    listar_recibos_mes,
    obtener_morosos_mes,
)
from controller.pago_controller import registrar_pago


def menu_cobros():
    while True:
        print("\n--- COBROS Y RECIBOS ---")
        print("1. Generar recibos de un mes")
        print("2. Listar recibos de un mes")
        print("3. Registrar pago de un recibo")
        print("4. Listar morosos de un mes")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "1":
            generar_recibos_view()
        elif opcion == "2":
            listar_recibos_view()
        elif opcion == "3":
            registrar_pago_view()
        elif opcion == "4":
            listar_morosos_view()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def generar_recibos_view():
    print("\n[Generar recibos de un mes]")
    try:
        anyo = int(input("Año (YYYY): ").strip())
        mes = int(input("Mes (1-12): ").strip())
        importe = float(input("Importe de la cuota mensual: ").strip())
    except ValueError:
        print("Datos numéricos no válidos.")
        return

    creados = generar_recibos_mes(anyo, mes, importe)
    print(f"✅ Se generaron {creados} recibos nuevos.")


def listar_recibos_view():
    print("\n[Listar recibos de un mes]")
    try:
        anyo = int(input("Año (YYYY): ").strip())
        mes = int(input("Mes (1-12): ").strip())
    except ValueError:
        print("Datos no válidos.")
        return

    recibos = listar_recibos_mes(anyo, mes)
    if not recibos:
        print("No hay recibos para ese mes.")
        return

    for r in recibos:
        print(
            f"[{r.recibo_id}] Cliente {r.cliente_id} | "
            f"{r.periodo_mes}/{r.periodo_anyo} | {r.importe}€ | {r.estado}"
        )


def registrar_pago_view():
    print("\n[Registrar pago]")
    try:
        recibo_id = int(input("ID del recibo: ").strip())
    except ValueError:
        print("ID no válido.")
        return

    metodo = input("Método de pago (efectivo, tarjeta, etc.) (opcional): ").strip() or None
    referencia = input("Referencia (opcional): ").strip() or None

    try:
        pago = registrar_pago(recibo_id, metodo=metodo, referencia=referencia)
        print(f"✅ Pago registrado con ID {pago.pago_id}, recibo {pago.recibo_id}")
    except Exception as e:
        print(f"❌ Error al registrar pago: {e}")


def listar_morosos_view():
    print("\n[Listar morosos de un mes]")
    try:
        anyo = int(input("Año (YYYY): ").strip())
        mes = int(input("Mes (1-12): ").strip())
    except ValueError:
        print("Datos no válidos.")
        return

    morosos = obtener_morosos_mes(anyo, mes)
    if not morosos:
        print("No hay morosos para ese mes. 🎉")
        return

    print("\nClientes morosos:")
    for m in morosos:
        print(
            f"[{m['cliente_id']}] {m['nombre']} {m['apellido']} - DNI: {m['dni']}"
        )
