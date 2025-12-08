import tkinter as tk
from tkinter import messagebox
from controller.auth_controller import autenticar_usuario


class LoginWindow(tk.Toplevel):
    """
    Ventana de inicio de sesión.
    Se muestra antes de cargar la vista principal.
    Cuando el login es correcto, llama a on_login_success(usuario)
    y se destruye.
    """
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.title("Iniciar sesión - GestiónGym")
        self.resizable(False, False)

        self.on_login_success = on_login_success  # callback hacia App()

        # ----------------------------
        #  Widgets
        # ----------------------------
        tk.Label(self, text="Usuario:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_user = tk.Entry(self, width=20)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_pass = tk.Entry(self, width=20, show="*")
        self.entry_pass.grid(row=1, column=1, padx=10, pady=10)

        self.btn_login = tk.Button(self, text="Entrar", command=self.do_login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=15)

        # ----------------------------
        #  Centrar ventana
        # ----------------------------
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Focus en usuario
        self.entry_user.focus_set()

    # ----------------------------
    #  Lógica del botón "Entrar"
    # ----------------------------
    def do_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        usuario = autenticar_usuario(username, password)

        if usuario:
            messagebox.showinfo("Éxito", f"Bienvenido {usuario.username}")
            self.on_login_success(usuario)  # ← devuelve el usuario a App
            self.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
