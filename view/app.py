# view/app.py

import tkinter as tk
from tkinter import ttk, messagebox

from controller.aparato_controller import listar_aparatos
from controller.cliente_controller import crear_cliente, listar_clientes
from controller.sesion_controller import (
    crear_sesion,
    listar_sesiones_dia,
    obtener_ocupacion_diaria,
    cancelar_sesion,
)
from controller.recibo_controller import (
    generar_recibos_mes,
    listar_recibos_mes,
    obtener_morosos_mes,
)
from controller.pago_controller import registrar_pago


# ========== SUBVISTAS (FRAMES) ==========

class AparatosView(ttk.Frame):
    title = "Aparatos"

    def __init__(self, master):
        super().__init__(master)

        columns = ("id", "codigo", "tipo", "descripcion")
        self.tree_aparatos = ttk.Treeview(
            self, columns=columns, show="headings", height=20
        )
        self.tree_aparatos.heading("id", text="ID")
        self.tree_aparatos.heading("codigo", text="Código")
        self.tree_aparatos.heading("tipo", text="Tipo")
        self.tree_aparatos.heading("descripcion", text="Descripción")
        self.tree_aparatos.column("id", width=50, anchor="center")
        self.tree_aparatos.column("codigo", width=100)
        self.tree_aparatos.column("tipo", width=150)
        self.tree_aparatos.column("descripcion", width=400)

        self.tree_aparatos.pack(fill="both", expand=True, padx=10, pady=10)

        btn_recargar = tk.Button(
            self, text="Recargar aparatos", command=self.cargar_aparatos
        )
        btn_recargar.pack(pady=5)

        self.cargar_aparatos()

    def cargar_aparatos(self):
        for row in self.tree_aparatos.get_children():
            self.tree_aparatos.delete(row)

        aparatos = listar_aparatos()
        for a in aparatos:
            self.tree_aparatos.insert(
                "", "end",
                values=(a.aparato_id, a.codigo, a.tipo, a.descripcion)
            )


class ClientesView(ttk.Frame):
    title = "Clientes"

    def __init__(self, master):
        super().__init__(master)

        # Formulario alta
        frame_form = ttk.LabelFrame(self, text="Alta de cliente")
        frame_form.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_form, text="DNI:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Email:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Fecha alta (YYYY-MM-DD):").grid(row=2, column=2, padx=5, pady=5, sticky="e")

        self.entry_dni = tk.Entry(frame_form, width=15)
        self.entry_nombre = tk.Entry(frame_form, width=15)
        self.entry_apellido = tk.Entry(frame_form, width=15)
        self.entry_email = tk.Entry(frame_form, width=20)
        self.entry_telefono = tk.Entry(frame_form, width=15)
        self.entry_fecha_alta = tk.Entry(frame_form, width=15)

        self.entry_dni.grid(row=0, column=1, padx=5, pady=5)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=5)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=5)
        self.entry_email.grid(row=1, column=3, padx=5, pady=5)
        self.entry_telefono.grid(row=2, column=1, padx=5, pady=5)
        self.entry_fecha_alta.grid(row=2, column=3, padx=5, pady=5)

        btn_alta = tk.Button(frame_form, text="Crear cliente", command=self.crear_cliente_gui)
        btn_alta.grid(row=3, column=0, columnspan=4, pady=10)

        # Listado
        frame_list = ttk.LabelFrame(self, text="Listado de clientes")
        frame_list.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "dni", "nombre", "apellido", "email", "telefono", "fecha_alta")
        self.tree_clientes = ttk.Treeview(
            frame_list, columns=columns, show="headings", height=15
        )
        for col, text in zip(columns, ["ID", "DNI", "Nombre", "Apellido",
                                       "Email", "Teléfono", "Fecha alta"]):
            self.tree_clientes.heading(col, text=text)

        self.tree_clientes.column("id", width=40, anchor="center")
        self.tree_clientes.column("dni", width=80, anchor="center")
        self.tree_clientes.column("nombre", width=100)
        self.tree_clientes.column("apellido", width=100)
        self.tree_clientes.column("email", width=150)
        self.tree_clientes.column("telefono", width=100)
        self.tree_clientes.column("fecha_alta", width=100, anchor="center")

        self.tree_clientes.pack(fill="both", expand=True, padx=5, pady=5)

        btn_recargar_clientes = tk.Button(
            frame_list, text="Recargar clientes", command=self.cargar_clientes
        )
        btn_recargar_clientes.pack(pady=5)

        self.cargar_clientes()

    def crear_cliente_gui(self):
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        email = self.entry_email.get().strip() or None
        telefono = self.entry_telefono.get().strip() or None
        fecha_alta = self.entry_fecha_alta.get().strip()

        if not dni or not nombre or not apellido or not fecha_alta:
            messagebox.showerror("Error", "DNI, nombre, apellido y fecha de alta son obligatorios.")
            return

        try:
            cliente = crear_cliente(dni, nombre, apellido, email, telefono, fecha_alta)
            messagebox.showinfo("Éxito", f"Cliente creado con ID {cliente.cliente_id}")
            self.entry_dni.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el cliente:\n{e}")

    def cargar_clientes(self):
        for row in self.tree_clientes.get_children():
            self.tree_clientes.delete(row)

        clientes = listar_clientes()
        for c in clientes:
            self.tree_clientes.insert(
                "", "end",
                values=(c.cliente_id, c.dni, c.nombre, c.apellido,
                        c.email, c.telefono, c.fecha_alta)
            )


class ReservasView(ttk.Frame):
    title = "Reservas"

    def __init__(self, master):
        super().__init__(master)

        # Formulario reserva
        frame_form = ttk.LabelFrame(self, text="Crear reserva")
        frame_form.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_form, text="ID aparato:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="ID cliente:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_form, text="Hora (HH:MM, 00 o 30):").grid(row=1, column=2, padx=5, pady=5, sticky="e")

        self.entry_res_aparato = tk.Entry(frame_form, width=10)
        self.entry_res_cliente = tk.Entry(frame_form, width=10)
        self.entry_res_fecha = tk.Entry(frame_form, width=12)
        self.entry_res_hora = tk.Entry(frame_form, width=8)

        self.entry_res_aparato.grid(row=0, column=1, padx=5, pady=5)
        self.entry_res_cliente.grid(row=0, column=3, padx=5, pady=5)
        self.entry_res_fecha.grid(row=1, column=1, padx=5, pady=5)
        self.entry_res_hora.grid(row=1, column=3, padx=5, pady=5)

        btn_crear_reserva = tk.Button(
            frame_form, text="Crear reserva", command=self.crear_reserva_gui
        )
        btn_crear_reserva.grid(row=2, column=0, columnspan=4, pady=10)

        # Listado de sesiones
        frame_list = ttk.LabelFrame(self, text="Sesiones de un día")
        frame_list.pack(fill="both", expand=True, padx=10, pady=10)

        top = ttk.Frame(frame_list)
        top.pack(fill="x", padx=5, pady=5)

        tk.Label(top, text="Fecha (YYYY-MM-DD):").pack(side="left")
        self.entry_list_fecha = tk.Entry(top, width=12)
        self.entry_list_fecha.pack(side="left", padx=5)
        btn_cargar_sesiones = tk.Button(
            top, text="Cargar sesiones", command=self.cargar_sesiones_dia_gui
        )
        btn_cargar_sesiones.pack(side="left", padx=5)

        tk.Label(top, text="   ID sesión a cancelar:").pack(side="left")
        self.entry_cancel_sesion = tk.Entry(top, width=6)
        self.entry_cancel_sesion.pack(side="left", padx=5)
        btn_cancelar = tk.Button(
            top, text="Cancelar sesión", command=self.cancelar_sesion_gui
        )
        btn_cancelar.pack(side="left", padx=5)

        columns = ("id", "aparato", "cliente", "fecha", "hora")
        self.tree_sesiones = ttk.Treeview(
            frame_list, columns=columns, show="headings", height=15
        )
        for col, text in zip(columns, ["ID", "Aparato", "Cliente", "Fecha", "Hora"]):
            self.tree_sesiones.heading(col, text=text)

        self.tree_sesiones.column("id", width=40, anchor="center")
        self.tree_sesiones.column("aparato", width=80, anchor="center")
        self.tree_sesiones.column("cliente", width=80, anchor="center")
        self.tree_sesiones.column("fecha", width=100, anchor="center")
        self.tree_sesiones.column("hora", width=80, anchor="center")

        self.tree_sesiones.pack(fill="both", expand=True, padx=5, pady=5)

        # Ocupación detallada
        frame_ocu = ttk.LabelFrame(self, text="Ocupación detallada")
        frame_ocu.pack(fill="both", expand=True, padx=10, pady=10)

        top2 = ttk.Frame(frame_ocu)
        top2.pack(fill="x", padx=5, pady=5)
        tk.Label(top2, text="Fecha (YYYY-MM-DD):").pack(side="left")
        self.entry_ocu_fecha = tk.Entry(top2, width=12)
        self.entry_ocu_fecha.pack(side="left", padx=5)
        btn_ocu = tk.Button(
            top2, text="Ver ocupación", command=self.ver_ocupacion_gui
        )
        btn_ocu.pack(side="left", padx=5)

        self.text_ocupacion = tk.Text(frame_ocu, height=8)
        self.text_ocupacion.pack(fill="both", expand=True, padx=5, pady=5)

    def crear_reserva_gui(self):
        try:
            aparato_id = int(self.entry_res_aparato.get().strip())
            cliente_id = int(self.entry_res_cliente.get().strip())
        except ValueError:
            messagebox.showerror("Error", "ID de aparato y cliente deben ser números.")
            return

        fecha = self.entry_res_fecha.get().strip()
        hora = self.entry_res_hora.get().strip()

        try:
            sesion = crear_sesion(aparato_id, cliente_id, fecha, hora, None)
            messagebox.showinfo("Éxito", f"Sesión creada con ID {sesion.sesion_id}")
            self.cargar_sesiones_dia_gui()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la sesión:\n{e}")

    def cargar_sesiones_dia_gui(self):
        fecha = self.entry_list_fecha.get().strip()
        for row in self.tree_sesiones.get_children():
            self.tree_sesiones.delete(row)

        sesiones = listar_sesiones_dia(fecha)
        for s in sesiones:
            self.tree_sesiones.insert(
                "", "end",
                values=(s.sesion_id, s.aparato_id, s.cliente_id, s.fecha, s.hora_inicio)
            )

    def cancelar_sesion_gui(self):
        try:
            sesion_id = int(self.entry_cancel_sesion.get().strip())
        except ValueError:
            messagebox.showerror("Error", "ID de sesión no válido.")
            return

        if cancelar_sesion(sesion_id):
            messagebox.showinfo("Éxito", "Sesión cancelada.")
            self.cargar_sesiones_dia_gui()
        else:
            messagebox.showerror("Error", "No se encontró la sesión.")

    def ver_ocupacion_gui(self):
        fecha = self.entry_ocu_fecha.get().strip()
        ocupacion = obtener_ocupacion_diaria(fecha)
        self.text_ocupacion.delete("1.0", tk.END)
        if not ocupacion:
            self.text_ocupacion.insert(tk.END, "No hay sesiones para esa fecha.")
            return

        for o in ocupacion:
            linea = (
                f"[{o['sesion_id']}] {o['fecha']} {o['hora_inicio']} | "
                f"Aparato {o['aparato_codigo']} ({o['aparato_tipo']}) | "
                f"Cliente {o['cliente_id']} - {o['cliente_nombre']} {o['cliente_apellido']}\n"
            )
            self.text_ocupacion.insert(tk.END, linea)


class CobrosView(ttk.Frame):
    title = "Cobros"

    def __init__(self, master):
        super().__init__(master)

        # Generar recibos
        frame_gen = ttk.LabelFrame(self, text="Generar recibos mensuales")
        frame_gen.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_gen, text="Año (YYYY):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(frame_gen, text="Mes (1-12):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Label(frame_gen, text="Importe cuota:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_any_rec = tk.Entry(frame_gen, width=6)
        self.entry_mes_rec = tk.Entry(frame_gen, width=4)
        self.entry_imp_rec = tk.Entry(frame_gen, width=8)

        self.entry_any_rec.grid(row=0, column=1, padx=5, pady=5)
        self.entry_mes_rec.grid(row=0, column=3, padx=5, pady=5)
        self.entry_imp_rec.grid(row=1, column=1, padx=5, pady=5)

        btn_gen = tk.Button(frame_gen, text="Generar recibos", command=self.generar_recibos_gui)
        btn_gen.grid(row=2, column=0, columnspan=4, pady=10)

        # Listar recibos + registrar pago + morosos
        frame_list = ttk.LabelFrame(self, text="Recibos y pagos")
        frame_list.pack(fill="both", expand=True, padx=10, pady=10)

        top = ttk.Frame(frame_list)
        top.pack(fill="x", padx=5, pady=5)

        tk.Label(top, text="Año (YYYY):").pack(side="left")
        self.entry_any_list = tk.Entry(top, width=6)
        self.entry_any_list.pack(side="left", padx=5)

        tk.Label(top, text="Mes (1-12):").pack(side="left")
        self.entry_mes_list = tk.Entry(top, width=4)
        self.entry_mes_list.pack(side="left", padx=5)

        btn_listar = tk.Button(top, text="Listar recibos", command=self.listar_recibos_gui)
        btn_listar.pack(side="left", padx=5)

        tk.Label(top, text="   ID recibo para pago:").pack(side="left")
        self.entry_recibo_pagar = tk.Entry(top, width=6)
        self.entry_recibo_pagar.pack(side="left", padx=5)
        btn_pagar = tk.Button(top, text="Registrar pago", command=self.registrar_pago_gui)
        btn_pagar.pack(side="left", padx=5)

        btn_morosos = tk.Button(top, text="Ver morosos", command=self.listar_morosos_gui)
        btn_morosos.pack(side="right", padx=5)

        columns = ("id", "cliente", "anyo", "mes", "importe", "estado")
        self.tree_recibos = ttk.Treeview(
            frame_list, columns=columns, show="headings", height=15
        )
        for col, text in zip(columns, ["ID", "Cliente", "Año", "Mes", "Importe", "Estado"]):
            self.tree_recibos.heading(col, text=text)

        self.tree_recibos.column("id", width=40, anchor="center")
        self.tree_recibos.column("cliente", width=80, anchor="center")
        self.tree_recibos.column("anyo", width=60, anchor="center")
        self.tree_recibos.column("mes", width=40, anchor="center")
        self.tree_recibos.column("importe", width=80, anchor="center")
        self.tree_recibos.column("estado", width=80, anchor="center")

        self.tree_recibos.pack(fill="both", expand=True, padx=5, pady=5)

    def generar_recibos_gui(self):
        try:
            anyo = int(self.entry_any_rec.get().strip())
            mes = int(self.entry_mes_rec.get().strip())
            importe = float(self.entry_imp_rec.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Año, mes e importe deben ser numéricos.")
            return

        creados = generar_recibos_mes(anyo, mes, importe)
        messagebox.showinfo("Resultado", f"Se generaron {creados} recibos nuevos.")

    def listar_recibos_gui(self):
        try:
            anyo = int(self.entry_any_list.get().strip())
            mes = int(self.entry_mes_list.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Año y mes deben ser numéricos.")
            return

        for row in self.tree_recibos.get_children():
            self.tree_recibos.delete(row)

        recibos = listar_recibos_mes(anyo, mes)
        for r in recibos:
            self.tree_recibos.insert(
                "", "end",
                values=(r.recibo_id, r.cliente_id, r.periodo_anyo,
                        r.periodo_mes, r.importe, r.estado)
            )

    def registrar_pago_gui(self):
        try:
            recibo_id = int(self.entry_recibo_pagar.get().strip())
        except ValueError:
            messagebox.showerror("Error", "ID de recibo debe ser numérico.")
            return

        try:
            pago = registrar_pago(recibo_id)
            messagebox.showinfo("Éxito", f"Pago registrado con ID {pago.pago_id}")
            self.listar_recibos_gui()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el pago:\n{e}")

    def listar_morosos_gui(self):
        try:
            anyo = int(self.entry_any_list.get().strip())
            mes = int(self.entry_mes_list.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Año y mes deben ser numéricos.")
            return

        morosos = obtener_morosos_mes(anyo, mes)
        if not morosos:
            messagebox.showinfo("Morosos", "No hay morosos en ese mes. 🎉")
            return

        texto = "Morosos:\n\n"
        for m in morosos:
            texto += f"[{m['cliente_id']}] {m['nombre']} {m['apellido']} - DNI: {m['dni']}\n"

        messagebox.showinfo("Morosos", texto)


# ========== VISTA PRINCIPAL (APP) ==========

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GestiónGym - Administrador")
        self.geometry("1100x650")

        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Array de vistas hijas
        self.views = [
            AparatosView(self.notebook),
            ClientesView(self.notebook),
            ReservasView(self.notebook),
            CobrosView(self.notebook),
        ]

        # Añadir cada vista como pestaña
        for view in self.views:
            self.notebook.add(view, text=view.title)
