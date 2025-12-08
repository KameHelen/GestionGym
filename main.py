# main.py

from model.conexion import crear_tablas
from controller.aparato_controller import inicializar_aparatos_por_defecto
from view.app import App


def main():
    # 1. Preparar base de datos
    crear_tablas()
    inicializar_aparatos_por_defecto()

    # 2. Lanzar app (solo admin, sin login)
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
