# view/app.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkcalendar import DateEntry
from PIL import Image, ImageTk

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
    generar_recibo_individual,
    exportar_morosos_pdf,
    obtener_estado_pagos_mes
)
from controller.pago_controller import registrar_pago
from datetime import date

# Configuración global
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GestiónGym - Administrador")
        self.geometry("1100x750")

        # Configurar grid principal (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- Configurar Icono Ventana ---
        try:
            self.icon_photo = ImageTk.PhotoImage(file="resources/logo.png")
            self.iconphoto(False, self.icon_photo)
        except Exception as e:
            print(f"No se pudo cargar icono de ventana: {e}")

        # --- Sidebar (Navegación) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Spacer tras los botones

        # --- Logo Sidebar ---
        self.logo_img = None
        try:
            pil_img = Image.open("resources/logo.png")
            self.logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 100))
            self.lbl_logo_img = ctk.CTkLabel(self.sidebar_frame, text="", image=self.logo_img)
            self.lbl_logo_img.grid(row=0, column=0, padx=20, pady=(20, 0))
        except Exception as e:
            print(f"Error cargando logo sidebar: {e}")

        self.lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="GymForTheMoment", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_logo.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Botones de navegación
        self.btn_aparatos = ctk.CTkButton(self.sidebar_frame, text="Aparatos", 
                                          command=lambda: self.select_frame("aparatos"),
                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_aparatos.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_clientes = ctk.CTkButton(self.sidebar_frame, text="Clientes", 
                                          command=lambda: self.select_frame("clientes"),
                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_clientes.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_reservas = ctk.CTkButton(self.sidebar_frame, text="Reservas", 
                                          command=lambda: self.select_frame("reservas"),
                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_reservas.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_cobros = ctk.CTkButton(self.sidebar_frame, text="Cobros", 
                                        command=lambda: self.select_frame("cobros"),
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        self.btn_cobros.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # Apariencia Mode
        self.lbl_mode = ctk.CTkLabel(self.sidebar_frame, text="Apariencia:", anchor="w")
        self.lbl_mode.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.option_mode = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                             command=self.change_appearance_mode_event)
        self.option_mode.grid(row=8, column=0, padx=20, pady=(10, 20))

        # --- Vista Principal (Contenedor) ---
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Diccionario de vistas
        self.frames = {}
        
        # Treeview Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#2a2d2e", 
                        foreground="white", 
                        fieldbackground="#343638", 
                        bordercolor="#343638", 
                        borderwidth=0, 
                        font=("Roboto", 12), 
                        rowheight=30)
        style.configure("Treeview.Heading", 
                        background="#565b5e", 
                        foreground="white", 
                        relief="flat", 
                        font=("Roboto", 13, "bold"))
        style.map("Treeview", 
                  background=[("selected", "#1f538d")])

        # Inicializar vistas
        self.frames["aparatos"] = AparatosView(self.main_container)

        self.frames["clientes"] = ClientesView(self.main_container)
        self.frames["reservas"] = ReservasView(self.main_container)
        self.frames["cobros"] = CobrosView(self.main_container)

        self.select_frame("aparatos")

    def select_frame(self, name):
        # Reset buttons Style to 'transparent'
        buttons = [self.btn_aparatos, self.btn_clientes, self.btn_reservas, self.btn_cobros]
        for btn in buttons:
            btn.configure(fg_color="transparent")
        
        # Highlight selected
        if name == "aparatos": self.btn_aparatos.configure(fg_color=("gray75", "gray25"))
        if name == "clientes": self.btn_clientes.configure(fg_color=("gray75", "gray25"))
        if name == "reservas": self.btn_reservas.configure(fg_color=("gray75", "gray25"))
        if name == "cobros": self.btn_cobros.configure(fg_color=("gray75", "gray25"))

        # Show frame
        frame = self.frames[name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


# ================== CLASES DE VISTA HIJAS ==================

class AparatosView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Grid layout: Izquierda (Formulario) - Derecha (Lista)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # --- Columna Izquierda: Formulario Alta y Acciones ---
        self.left_col = ctk.CTkFrame(self)
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(self.left_col, text="Gestión Inventario", font=ctk.CTkFont(size=20, weight="bold")).pack(padx=20, pady=20, anchor="w")

        # Form fields
        ctk.CTkLabel(self.left_col, text="Código").pack(padx=20, anchor="w")
        self.ent_codigo = ctk.CTkEntry(self.left_col, placeholder_text="Ej: M-01")
        self.ent_codigo.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(self.left_col, text="Tipo").pack(padx=20, anchor="w")
        self.ent_tipo = ctk.CTkEntry(self.left_col, placeholder_text="Ej: Cinta, Pesas...")
        self.ent_tipo.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(self.left_col, text="Descripción").pack(padx=20, anchor="w")
        self.ent_desc = ctk.CTkEntry(self.left_col)
        self.ent_desc.pack(padx=20, pady=(0, 20), fill="x")

        ctk.CTkButton(self.left_col, text="Añadir Aparato", command=self.add_aparato).pack(padx=20, fill="x", pady=(0, 10))
        
        ttk.Separator(self.left_col, orient="horizontal").pack(fill="x", pady=20, padx=10)

        ctk.CTkLabel(self.left_col, text="Acciones Selección", font=ctk.CTkFont(size=14, weight="bold")).pack(padx=20, anchor="w")
        ctk.CTkButton(self.left_col, text="Eliminar Seleccionado", fg_color="#D32F2F", hover_color="#B71C1C", command=self.del_aparato).pack(padx=20, fill="x", pady=10)

        # --- Columna Derecha: Lista ---
        self.right_col = ctk.CTkFrame(self)
        self.right_col.grid(row=0, column=1, sticky="nsew")

        header = ctk.CTkFrame(self.right_col, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(header, text="Inventario Actual", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="⟳", width=40, command=self.cargar).pack(side="right")

        # Treeview
        columns = ("id", "codigo", "tipo", "descripcion")
        self.tree = ttk.Treeview(self.right_col, columns=columns, show="headings", height=20)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("descripcion", text="Descripción")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("codigo", width=100)
        self.tree.column("tipo", width=150)
        self.tree.column("descripcion", width=400)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.cargar()

    def add_aparato(self):
        from controller.aparato_controller import crear_aparato # Late import to avoid circular if any
        
        c = self.ent_codigo.get().strip()
        t = self.ent_tipo.get().strip()
        d = self.ent_desc.get().strip()

        if not c or not t or not d:
            messagebox.showerror("Error", "Todos los campos (Código, Tipo, Descripción) son obligatorios.")
            return

        try:
            crear_aparato(c, t, d)
            messagebox.showinfo("Éxito", "Aparato añadido correctamente")
            self.ent_codigo.delete(0, 'end')
            self.ent_tipo.delete(0, 'end')
            self.ent_desc.delete(0, 'end')
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def del_aparato(self):
        from controller.aparato_controller import eliminar_aparato
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un aparato de la lista.")
            return
        
        if not messagebox.askyesno("Confirmar", "¿Eliminar aparato seleccionado? Esto borrará sus sesiones."):
            return

        try:
            item = self.tree.item(sel[0])
            id_aparato = item['values'][0]
            eliminar_aparato(id_aparato)
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in listar_aparatos():
            self.tree.insert("", "end", values=(a.aparato_id, a.codigo, a.tipo, a.descripcion))


class ClientesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Split: Formulario arriba, lista abajo
        self.card_form = ctk.CTkFrame(self)
        self.card_form.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(self.card_form, text="Nuevo Cliente", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=20, pady=10, anchor="w")

        frame_grid = ctk.CTkFrame(self.card_form, fg_color="transparent")
        frame_grid.pack(padx=20, pady=10, fill="x")

        # DNI / Nombre / Apellido
        ctk.CTkLabel(frame_grid, text="DNI").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_dni = ctk.CTkEntry(frame_grid, placeholder_text="12345678X")
        self.entry_dni.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(frame_grid, text="Nombre").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.entry_nombre = ctk.CTkEntry(frame_grid)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(frame_grid, text="Apellido").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_apellido = ctk.CTkEntry(frame_grid)
        self.entry_apellido.grid(row=1, column=2, padx=5, pady=(0, 10), sticky="ew")

        # Email / Tel / Fecha
        ctk.CTkLabel(frame_grid, text="Email").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.entry_email = ctk.CTkEntry(frame_grid)
        self.entry_email.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(frame_grid, text="Teléfono").grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.entry_tel = ctk.CTkEntry(frame_grid)
        self.entry_tel.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(frame_grid, text="Fecha Alta").grid(row=2, column=2, padx=5, pady=2, sticky="w")
        # CALENDARIO MÁS GRANDE
        self.entry_fecha = DateEntry(frame_grid, width=12, background='darkblue', 
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                     font=("Roboto", 12)) 
        self.entry_fecha.grid(row=3, column=2, padx=5, pady=(0, 10), sticky="w")

        btn_add = ctk.CTkButton(self.card_form, text="Registrar Cliente", command=self.add_cliente)
        btn_add.pack(padx=20, pady=15, anchor="e")

        # --- Card Lista ---
        self.card_list = ctk.CTkFrame(self)
        self.card_list.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(self.card_list, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_frame, text="Directorio de Clientes", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        btn_refresh = ctk.CTkButton(header_frame, text="⟳", width=40, command=self.load_clientes)
        btn_refresh.pack(side="right")

        cols = ("id", "dni", "nombre", "apellido", "email", "telefono", "fecha")
        self.tree = ttk.Treeview(self.card_list, columns=cols, show="headings", height=10)
        for c in cols: self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.load_clientes()

    def add_cliente(self):
        try:
            cli = crear_cliente(self.entry_dni.get(), self.entry_nombre.get(), self.entry_apellido.get(), 
                          self.entry_email.get(), self.entry_tel.get(), self.entry_fecha.get_date().strftime("%Y-%m-%d"))
            
            # Generar primer recibo (mes actual)
            hoy = date.today()
            generar_recibo_individual(cli.cliente_id, hoy.year, hoy.month, 30.0)
            
            messagebox.showinfo("Éxito", f"Cliente creado y recibo generado para {hoy.month}/{hoy.year}.")
            self.load_clientes()
            self.entry_dni.delete(0, 'end')
            self.entry_nombre.delete(0, 'end')
            self.entry_apellido.delete(0, 'end')
            self.entry_email.delete(0, 'end')
            self.entry_tel.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_clientes(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for c in listar_clientes():
            self.tree.insert("", "end", values=(c.cliente_id, c.dni, c.nombre, c.apellido, c.email, c.telefono, c.fecha_alta))


class ReservasView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Grid layout: Izquierda (Dashboard/Form) - Derecha (Lista)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Columna Izquierda: Formulario y Acciones ---
        self.left_col = ctk.CTkFrame(self)
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(self.left_col, text="Nueva Reserva", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=20, pady=20, anchor="w")

        # Form fields
        ctk.CTkLabel(self.left_col, text="ID Aparato").pack(padx=20, anchor="w")
        self.ent_aparato = ctk.CTkEntry(self.left_col)
        self.ent_aparato.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(self.left_col, text="ID Cliente").pack(padx=20, anchor="w")
        self.ent_cliente = ctk.CTkEntry(self.left_col)
        self.ent_cliente.pack(padx=20, pady=(0, 10), fill="x")

        ctk.CTkLabel(self.left_col, text="Fecha").pack(padx=20, anchor="w")
        # CALENDARIO MÁS GRANDE
        self.ent_fecha = DateEntry(self.left_col, width=12, background='darkblue', 
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                   font=("Roboto", 12))
        self.ent_fecha.pack(padx=20, pady=(0, 10), anchor="w")
        
        ctk.CTkLabel(self.left_col, text="Hora (HH:MM)").pack(padx=20, anchor="w")
        self.ent_hora = ctk.CTkEntry(self.left_col, placeholder_text="09:00, 09:30...")
        self.ent_hora.pack(padx=20, pady=(0, 20), fill="x")

        ctk.CTkButton(self.left_col, text="Confirmar Reserva", command=self.add_reserva).pack(padx=20, fill="x")

        # Separator
        ttk.Separator(self.left_col, orient="horizontal").pack(fill="x", pady=20, padx=10)

        ctk.CTkLabel(self.left_col, text="Gestión de Sesión", font=ctk.CTkFont(size=16, weight="bold")).pack(padx=20, anchor="w")
        self.ent_cancel_id = ctk.CTkEntry(self.left_col, placeholder_text="ID Sesión")
        self.ent_cancel_id.pack(padx=20, pady=10, fill="x")
        ctk.CTkButton(self.left_col, text="Cancelar Sesión", fg_color="#D32F2F", hover_color="#B71C1C", command=self.cancel_reserva).pack(padx=20, fill="x")


        # --- Columna Derecha: Visualización ---
        self.right_col = ctk.CTkFrame(self)
        self.right_col.grid(row=0, column=1, sticky="nsew")

        # Filtro Fecha
        top_bar = ctk.CTkFrame(self.right_col, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(top_bar, text="Agenda del Día:").pack(side="left", padx=5)
        # CALENDARIO MÁS GRANDE
        self.filter_date = DateEntry(top_bar, width=12, background='darkblue', 
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                     font=("Roboto", 12))
        self.filter_date.pack(side="left", padx=5)
        
        ctk.CTkButton(top_bar, text="Buscar", width=60, command=self.load_sesiones).pack(side="left", padx=5)
        ctk.CTkButton(top_bar, text="Exportar PDF", width=100, fg_color="green", command=self.export_pdf).pack(side="right")


        # Treeview
        cols = ("id", "hora", "aparato", "cliente")
        self.tree = ttk.Treeview(self.right_col, columns=cols, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("aparato", text="Aparato")
        self.tree.heading("cliente", text="Cliente")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("hora", width=60, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Texto detalle
        self.txt_detail = ctk.CTkTextbox(self.right_col, height=100)
        self.txt_detail.pack(fill="x", padx=20, pady=10)

    def add_reserva(self):
        try:
            crear_sesion(int(self.ent_aparato.get()), int(self.ent_cliente.get()), 
                         self.ent_fecha.get_date().strftime("%Y-%m-%d"), self.ent_hora.get())
            messagebox.showinfo("Éxito", "Reserva creada")
            self.load_sesiones()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_reserva(self):
        if cancelar_sesion(int(self.ent_cancel_id.get() or 0)):
            messagebox.showinfo("Éxito", "Sesión cancelada")
            self.load_sesiones()
        else:
            messagebox.showerror("Error", "No se encontró la sesión")

    def load_sesiones(self):
        date = self.filter_date.get_date().strftime("%Y-%m-%d")
        for i in self.tree.get_children(): self.tree.delete(i)
        
        ocupacion = obtener_ocupacion_diaria(date)
        
        # Llenar tree
        for o in ocupacion:
            self.tree.insert("", "end", values=(o['sesion_id'], o['hora_inicio'], f"{o['aparato_codigo']} ({o['aparato_tipo']})", f"{o['cliente_id']} - {o['cliente_nombre']}"))
            
        # Llenar texto
        self.txt_detail.delete("1.0", "end")
        if not ocupacion:
            self.txt_detail.insert("end", "No hay sesiones programada para hoy.")
        else:
            for o in ocupacion:
                self.txt_detail.insert("end", f"[{o['hora_inicio']}] {o['aparato_tipo']} - {o['cliente_nombre']} {o['cliente_apellido']}\n")

    def export_pdf(self):
        try:
            f = exportar_sesiones_pdf(self.filter_date.get_date().strftime("%Y-%m-%d"))
            messagebox.showinfo("PDF", f"Archivo generado: {f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


class CobrosView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.card = ctk.CTkFrame(self)
        self.card.pack(fill="both", expand=True)

        # --- Top Controls ---
        top = ctk.CTkFrame(self.card, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(top, text="Periodo de Cobro:", font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        # Fecha actual por defecto
        today = date.today()
        
        self.ent_y = ctk.CTkEntry(top, width=60)
        self.ent_y.insert(0, str(today.year))
        self.ent_y.pack(side="left", padx=5)
        
        self.ent_m = ctk.CTkEntry(top, width=40)
        self.ent_m.insert(0, str(today.month))
        self.ent_m.pack(side="left", padx=5)
        
        ctk.CTkButton(top, text="Cargar Estado", command=self.cargar_estado).pack(side="left", padx=10)
        
        ctk.CTkButton(top, text="Exportar Pendientes PDF", fg_color="#D32F2F", command=self.export_morosos).pack(side="right", padx=10)

        # --- Tree ---
        cols = ("id", "nombre", "dni", "importe", "estado", "recibo_id") # recibo_id hidden ideally
        self.tree = ttk.Treeview(self.card, columns=cols, show="headings", height=20)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Cliente")
        self.tree.heading("dni", text="DNI")
        self.tree.heading("importe", text="Importe (€)")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("dni", width=100)
        self.tree.column("importe", width=80, anchor="e")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("recibo_id", width=0, stretch=False) # Oculto
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Evento doble click para pagar
        self.tree.bind("<Double-1>", self.on_double_click)
        
        ctk.CTkLabel(self.card, text="* Doble click en un cliente para gestionar el pago.", text_color="gray").pack(pady=10)

        # Cargar inicial
        self.cargar_estado()

    def cargar_estado(self):
        # Limpiar
        for i in self.tree.get_children(): self.tree.delete(i)
        
        try:
            y = int(self.ent_y.get())
            m = int(self.ent_m.get())
            
            datos = obtener_estado_pagos_mes(y, m)
            
            for d in datos:
                # Si recibo_id es None, guardamos "None" string para recuperarlo luego o 0
                rid = d['recibo_id'] if d['recibo_id'] else 0
                self.tree.insert("", "end", values=(
                    d['cliente_id'], 
                    f"{d['nombre']} {d['apellido']}", 
                    d['dni'], 
                    f"{d['importe']:.2f}", 
                    d['estado'],
                    rid
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos: {e}")

    def on_double_click(self, event):
        item = self.tree.selection()
        if not item: return
        vals = self.tree.item(item[0], 'values')
        
        cliente_id = int(vals[0])
        nombre = vals[1]
        estado = vals[4]
        recibo_id = int(vals[5])
        
        if estado == 'pagado':
            messagebox.showinfo("Info", "Este cliente ya está al corriente de pago.")
            return
            
        # Abrir popup de pago
        self.abrir_popup_pago(cliente_id, nombre, recibo_id)

    def abrir_popup_pago(self, cliente_id, nombre, recibo_id):
        # Crear Toplevel
        top = ctk.CTkToplevel(self)
        top.title("Registrar Pago")
        top.geometry("300x250")
        top.grab_set() # Modal
        
        ctk.CTkLabel(top, text="Registrar Pago", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        ctk.CTkLabel(top, text=f"Cliente: {nombre}").pack(pady=5)
        
        ctk.CTkLabel(top, text="Importe a cobrar (€):").pack(pady=(10, 0))
        ent_imp = ctk.CTkEntry(top)
        ent_imp.insert(0, "40.0")
        ent_imp.pack(pady=5)
        
        def confirmar():
            try:
                importe = float(ent_imp.get())
                y = int(self.ent_y.get())
                m = int(self.ent_m.get())
                
                # Si no existe recibo, crearlo primero
                rid = recibo_id
                if rid == 0:
                    rid = generar_recibo_individual(cliente_id, y, m, importe)
                
                # Registrar pago
                if rid and rid != 0:
                    registrar_pago(rid)
                    messagebox.showinfo("Éxito", "Pago registrado correctamente.")
                    top.destroy()
                    self.cargar_estado()
                else:
                    messagebox.showerror("Error", "No se pudo generar o localizar el recibo.")
                    
            except ValueError:
                messagebox.showerror("Error", "Importe inválido.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ctk.CTkButton(top, text="Confirmar Pago", fg_color="green", command=confirmar).pack(pady=20)

    def export_morosos(self):
        try:
            f = exportar_morosos_pdf(int(self.ent_y.get()), int(self.ent_m.get()))
            messagebox.showinfo("PDF", f"Archivo generado: {f}")
        except Exception as e: messagebox.showerror("Error", str(e))
