# view/app.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkcalendar import DateEntry

from controller.aparato_controller import listar_aparatos
from controller.cliente_controller import crear_cliente, listar_clientes
from controller.sesion_controller import (
    crear_sesion,
    listar_sesiones_dia,
    obtener_ocupacion_diaria,
    cancelar_sesion,
    exportar_sesiones_pdf
)
from controller.recibo_controller import (
    generar_recibos_mes,
    listar_recibos_mes,
    obtener_morosos_mes,
)
from controller.pago_controller import registrar_pago

# Configuración global de CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class AparatosView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        lbl_title = ctk.CTkLabel(self, text="Gestión de Aparatos", font=("Roboto", 20, "bold"))
        lbl_title.pack(pady=10)

        # Treeview (Tabla) - Se mantiene ttk.Treeview porque ctk no tiene tabla nativa aún
        columns = ("id", "codigo", "tipo", "descripcion")
        self.tree_aparatos = ttk.Treeview(
            self, columns=columns, show="headings", height=15
        )
        self.tree_aparatos.heading("id", text="ID")
        self.tree_aparatos.heading("codigo", text="Código")
        self.tree_aparatos.heading("tipo", text="Tipo")
        self.tree_aparatos.heading("descripcion", text="Descripción")
        
        self.tree_aparatos.column("id", width=50, anchor="center")
        self.tree_aparatos.column("codigo", width=100)
        self.tree_aparatos.column("tipo", width=150)
        self.tree_aparatos.column("descripcion", width=400)

        # Style for Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.tree_aparatos.pack(fill="both", expand=True, padx=20, pady=10)

        btn_recargar = ctk.CTkButton(
            self, text="Recargar Lista", command=self.cargar_aparatos
        )
        btn_recargar.pack(pady=10)

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


class ClientesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # --- Formulario Alta ---
        frame_form = ctk.CTkFrame(self)
        frame_form.pack(fill="x", padx=20, pady=10)
        
        lbl_form = ctk.CTkLabel(frame_form, text="Alta de Cliente", font=("Roboto", 16, "bold"))
        lbl_form.grid(row=0, column=0, columnspan=4, pady=(10, 10))

        # Fila 1
        ctk.CTkLabel(frame_form, text="DNI:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_dni = ctk.CTkEntry(frame_form, width=150)
        self.entry_dni.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_form, text="Nombre:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.entry_nombre = ctk.CTkEntry(frame_form, width=150)
        self.entry_nombre.grid(row=1, column=3, padx=10, pady=5)

        # Fila 2
        ctk.CTkLabel(frame_form, text="Apellido:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_apellido = ctk.CTkEntry(frame_form, width=150)
        self.entry_apellido.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_form, text="Email:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.entry_email = ctk.CTkEntry(frame_form, width=200)
        self.entry_email.grid(row=2, column=3, padx=10, pady=5)

        # Fila 3
        ctk.CTkLabel(frame_form, text="Teléfono:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_telefono = ctk.CTkEntry(frame_form, width=150)
        self.entry_telefono.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_form, text="Fecha Alta:").grid(row=3, column=2, padx=10, pady=5, sticky="e")
        # Widget DateEntry de tkcalendar
        self.entry_fecha_alta = DateEntry(frame_form, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_fecha_alta.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        btn_alta = ctk.CTkButton(frame_form, text="Crear Cliente", command=self.crear_cliente_gui)
        btn_alta.grid(row=4, column=0, columnspan=4, pady=15)

        # --- Listado ---
        frame_list = ctk.CTkFrame(self)
        frame_list.pack(fill="both", expand=True, padx=20, pady=10)

        lbl_list = ctk.CTkLabel(frame_list, text="Listado de Clientes", font=("Roboto", 14, "bold"))
        lbl_list.pack(pady=5)

        columns = ("id", "dni", "nombre", "apellido", "email", "telefono", "fecha_alta")
        self.tree_clientes = ttk.Treeview(
            frame_list, columns=columns, show="headings", height=10
        )
        for col, text in zip(columns, ["ID", "DNI", "Nombre", "Apellido",
                                       "Email", "Teléfono", "Fecha Alta"]):
            self.tree_clientes.heading(col, text=text)

        self.tree_clientes.column("id", width=40, anchor="center")
        self.tree_clientes.column("dni", width=80, anchor="center")
        self.tree_clientes.column("nombre", width=100)
        self.tree_clientes.column("apellido", width=100)
        self.tree_clientes.column("email", width=150)
        self.tree_clientes.column("telefono", width=100)
        self.tree_clientes.column("fecha_alta", width=100, anchor="center")

        self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=5)

        btn_recargar_clientes = ctk.CTkButton(
            frame_list, text="Recargar Lista", command=self.cargar_clientes
        )
        btn_recargar_clientes.pack(pady=5)

        self.cargar_clientes()

    def crear_cliente_gui(self):
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        email = self.entry_email.get().strip() or None
        telefono = self.entry_telefono.get().strip() or None
        fecha_alta = self.entry_fecha_alta.get_date().strftime("%Y-%m-%d")

        if not dni or not nombre or not apellido or not fecha_alta:
            messagebox.showerror("Error", "DNI, nombre, apellido y fecha de alta son obligatorios.")
            return

        try:
            cliente = crear_cliente(dni, nombre, apellido, email, telefono, fecha_alta)
            messagebox.showinfo("Éxito", f"Cliente creado con ID {cliente.cliente_id}")
            self.entry_dni.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            # self.entry_email.delete(0, tk.END) # CTKEntry doesn't support delete 0, END like that? wait it does
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


class ReservasView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # --- Crear Reserva ---
        frame_form = ctk.CTkFrame(self)
        frame_form.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_form, text="Nueva Reserva", font=("Roboto", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        ctk.CTkLabel(frame_form, text="ID Aparato:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_res_aparato = ctk.CTkEntry(frame_form, width=80)
        self.entry_res_aparato.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(frame_form, text="ID Cliente:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.entry_res_cliente = ctk.CTkEntry(frame_form, width=80)
        self.entry_res_cliente.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(frame_form, text="Fecha:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_res_fecha = DateEntry(frame_form, width=12, background='darkblue',
                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_res_fecha.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(frame_form, text="Hora (HH:MM):").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.entry_res_hora = ctk.CTkEntry(frame_form, width=80, placeholder_text="09:00")
        self.entry_res_hora.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        btn_crear_reserva = ctk.CTkButton(
            frame_form, text="Confirmar Reserva", command=self.crear_reserva_gui
        )
        btn_crear_reserva.grid(row=3, column=0, columnspan=4, pady=15)

        # --- Listado de Sesiones / Exportar ---
        frame_list = ctk.CTkFrame(self)
        frame_list.pack(fill="both", expand=True, padx=20, pady=10)

        # Controles superiores lista
        top = ctk.CTkFrame(frame_list, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(top, text="Ver sesiones del día:").pack(side="left", padx=5)
        self.entry_list_fecha = DateEntry(top, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_list_fecha.pack(side="left", padx=5)
        
        btn_cargar_sesiones = ctk.CTkButton(
            top, text="Cargar", width=80, command=self.cargar_sesiones_dia_gui
        )
        btn_cargar_sesiones.pack(side="left", padx=5)

        btn_exportar_pdf = ctk.CTkButton(
            top, text="Exportar PDF", width=100, fg_color="green", hover_color="darkgreen",
            command=self.exportar_pdf_gui
        )
        btn_exportar_pdf.pack(side="left", padx=20)

        # Cancelar sesión
        frame_cancel = ctk.CTkFrame(frame_list, fg_color="transparent")
        frame_cancel.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame_cancel, text="ID Sesión a cancelar:").pack(side="left", padx=5)
        self.entry_cancel_sesion = ctk.CTkEntry(frame_cancel, width=60)
        self.entry_cancel_sesion.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            frame_cancel, text="Cancelar", width=80, fg_color="red", hover_color="darkred",
            command=self.cancelar_sesion_gui
        )
        btn_cancelar.pack(side="left", padx=5)

        # Treeview Sesiones
        columns = ("id", "aparato", "cliente", "fecha", "hora")
        self.tree_sesiones = ttk.Treeview(
            frame_list, columns=columns, show="headings", height=10
        )
        for col, text in zip(columns, ["ID", "Aparato", "Cliente", "Fecha", "Hora"]):
            self.tree_sesiones.heading(col, text=text)

        self.tree_sesiones.column("id", width=40, anchor="center")
        self.tree_sesiones.column("aparato", width=80, anchor="center")
        self.tree_sesiones.column("cliente", width=80, anchor="center")
        self.tree_sesiones.column("fecha", width=100, anchor="center")
        self.tree_sesiones.column("hora", width=80, anchor="center")

        self.tree_sesiones.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Ocupación Detallada (Texto) ---
        frame_ocu = ctk.CTkFrame(self)
        frame_ocu.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(frame_ocu, text="Vista Detallada de Ocupación").pack(pady=5)
        
        self.text_ocupacion = ctk.CTkTextbox(frame_ocu, height=100)
        self.text_ocupacion.pack(fill="both", expand=True, padx=10, pady=5)


    def crear_reserva_gui(self):
        try:
            aparato_id = int(self.entry_res_aparato.get().strip())
            cliente_id = int(self.entry_res_cliente.get().strip())
        except ValueError:
            messagebox.showerror("Error", "ID de aparato y cliente deben ser números.")
            return

        fecha = self.entry_res_fecha.get_date().strftime("%Y-%m-%d")
        hora = self.entry_res_hora.get().strip()

        try:
            sesion = crear_sesion(aparato_id, cliente_id, fecha, hora, None)
            messagebox.showinfo("Éxito", f"Sesión creada con ID {sesion.sesion_id}")
            # Actualizar listado si es para el mismo día
            if self.entry_list_fecha.get_date().strftime("%Y-%m-%d") == fecha:
                 self.cargar_sesiones_dia_gui()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la sesión:\n{e}")

    def cargar_sesiones_dia_gui(self):
        fecha = self.entry_list_fecha.get_date().strftime("%Y-%m-%d")
        for row in self.tree_sesiones.get_children():
            self.tree_sesiones.delete(row)

        sesiones = listar_sesiones_dia(fecha)
        for s in sesiones:
            self.tree_sesiones.insert(
                "", "end",
                values=(s.sesion_id, s.aparato_id, s.cliente_id, s.fecha, s.hora_inicio)
            )
        
        # También actualizar el texto de ocupación
        self.ver_ocupacion_gui(fecha)

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

    def ver_ocupacion_gui(self, fecha):
        ocupacion = obtener_ocupacion_diaria(fecha)
        self.text_ocupacion.delete("1.0", tk.END)
        if not ocupacion:
            self.text_ocupacion.insert(tk.END, "No hay sesiones para esa fecha.")
            return

        for o in ocupacion:
            linea = (
                f"[{o['sesion_id']}] {o['hora_inicio']} | "
                f"Aparato {o['aparato_codigo']} ({o['aparato_tipo']}) | "
                f"Cliente {o['cliente_id']} - {o['cliente_nombre']} {o['cliente_apellido']}\n"
            )
            self.text_ocupacion.insert(tk.END, linea)

    def exportar_pdf_gui(self):
        fecha = self.entry_list_fecha.get_date().strftime("%Y-%m-%d")
        try:
            filename = exportar_sesiones_pdf(fecha)
            messagebox.showinfo("PDF Exportado", f"Se ha generado el archivo:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error Exportación", f"No se pudo generar el PDF:\n{e}")


class CobrosView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # --- Generar Recibos ---
        frame_gen = ctk.CTkFrame(self)
        frame_gen.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_gen, text="Generación de Recibos", font=("Roboto", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        ctk.CTkLabel(frame_gen, text="Año:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_any_rec = ctk.CTkEntry(frame_gen, width=80)
        self.entry_any_rec.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_gen, text="Mes (1-12):").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.entry_mes_rec = ctk.CTkEntry(frame_gen, width=50)
        self.entry_mes_rec.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(frame_gen, text="Importe Cuota:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_imp_rec = ctk.CTkEntry(frame_gen, width=80)
        self.entry_imp_rec.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        btn_gen = ctk.CTkButton(frame_gen, text="Generar Recibos Mensuales", command=self.generar_recibos_gui)
        btn_gen.grid(row=3, column=0, columnspan=4, pady=15)

        # --- Listar y Pagar ---
        frame_list = ctk.CTkFrame(self)
        frame_list.pack(fill="both", expand=True, padx=20, pady=10)

        top = ctk.CTkFrame(frame_list, fg_color="transparent")
        top.pack(fill="x", padx=5, pady=5)

        self.entry_any_list = ctk.CTkEntry(top, width=60, placeholder_text="YYYY")
        self.entry_any_list.pack(side="left", padx=5)
        
        self.entry_mes_list = ctk.CTkEntry(top, width=40, placeholder_text="MM")
        self.entry_mes_list.pack(side="left", padx=5)

        btn_listar = ctk.CTkButton(top, text="Listar", width=80, command=self.listar_recibos_gui)
        btn_listar.pack(side="left", padx=10)

        ctk.CTkLabel(top, text="|").pack(side="left", padx=5)

        self.entry_recibo_pagar = ctk.CTkEntry(top, width=60, placeholder_text="ID Recibo")
        self.entry_recibo_pagar.pack(side="left", padx=5)
        
        btn_pagar = ctk.CTkButton(top, text="Registrar Pago", width=120, fg_color="green", hover_color="darkgreen",
                                  command=self.registrar_pago_gui)
        btn_pagar.pack(side="left", padx=5)

        btn_morosos = ctk.CTkButton(top, text="Ver Morosos", fg_color="red", hover_color="darkred",
                                    command=self.listar_morosos_gui)
        btn_morosos.pack(side="right", padx=10)

        # Treeview Recibos
        columns = ("id", "cliente", "anyo", "mes", "importe", "estado")
        self.tree_recibos = ttk.Treeview(
            frame_list, columns=columns, show="headings", height=12
        )
        for col, text in zip(columns, ["ID", "Cliente", "Año", "Mes", "Importe", "Estado"]):
            self.tree_recibos.heading(col, text=text)

        self.tree_recibos.column("id", width=40, anchor="center")
        self.tree_recibos.column("cliente", width=80, anchor="center")
        self.tree_recibos.column("anyo", width=60, anchor="center")
        self.tree_recibos.column("mes", width=40, anchor="center")
        self.tree_recibos.column("importe", width=80, anchor="center")
        self.tree_recibos.column("estado", width=80, anchor="center")

        self.tree_recibos.pack(fill="both", expand=True, padx=10, pady=5)

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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GestiónGym - Administrador")
        self.geometry("1100x700")

        # TabView (Pestañas modernas de CTK)
        self.tabview = ctk.CTkTabview(self, width=1100, height=650)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear Pestañas
        self.tabview.add("Aparatos")
        self.tabview.add("Clientes")
        self.tabview.add("Reservas")
        self.tabview.add("Cobros")

        # Instanciar las vistas dentro de cada pestaña
        # self.tabview.tab("Nombre") actúa como el master (Frame)
        self.view_aparatos = AparatosView(self.tabview.tab("Aparatos"))
        self.view_aparatos.pack(fill="both", expand=True)

        self.view_clientes = ClientesView(self.tabview.tab("Clientes"))
        self.view_clientes.pack(fill="both", expand=True)

        self.view_reservas = ReservasView(self.tabview.tab("Reservas"))
        self.view_reservas.pack(fill="both", expand=True)

        self.view_cobros = CobrosView(self.tabview.tab("Cobros"))
        self.view_cobros.pack(fill="both", expand=True)
