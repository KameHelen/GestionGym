# Gestión Gym - Sistema de Administración de Gimnasios
**Autor:** Elena Mesa Requena  
**Curso:** Desarrollo de Aplicaciones Multiplataforma (DAM)  
**Fecha de Entrega:** Diciembre 2024
---
## 📋 Descripción
**Gestión Gym** es una aplicación de escritorio completa desarrollada en **Python** para la administración integral de un gimnasio. Diseñada con una arquitectura **MVC (Modelo-Vista-Controlador)** y una interfaz gráfica moderna basada en **CustomTkinter**, permite gestionar el ciclo de vida completo del negocio: desde el alta de clientes y máquinas hasta la reserva de sesiones y el control de facturación.
## ✨ Características Principales
### 1. Gestión de Clientes
*   **Alta y Modificación:** Registro completo con validación estricta de datos (DNI español, formatos de teléfono/email).
*   **Directorio:** Listado visual con filtrado rápido.
*   **Control de Duplicados:** Evita automáticamente registros repetidos por DNI.
### 2. Gestión de Aparatos (Inventario)
*   Control de máquinas y equipamiento (Cintas, Pesas, Bicicletas...).
*   Seguimiento de disponibilidad para reservas.
### 3. Sistema de Reservas Avanzado (Wizard)
*   **Asistente Paso a Paso:** Nuevo sistema guiado para crear reservas sin errores.
*   **Disponibilidad Dinámica:** Cálculo automático de "slots" (huecos) libres cada 30 minutos según el tipo de aparato.
*   **Buscador en Tiempo Real:** Localización instantánea de clientes por nombre o DNI durante la reserva.
*   **Agenda Diaria:** Visualización automática de las sesiones del día al entrar en la sección.
### 4. Facturación y Cobros
*   **Generación de Recibos:** Emisión automática de cuotas mensuales.
*   **Control de Morosos:** Identificación rápida de pagos pendientes.
*   **Buscador Integrado:** Filtrado de la lista de cobros por cliente.
*   **Exportación a PDF:** Generación de informes profesionales de impagos y ocupación.
### 5. Interfaz Gráfica (UI/UX)
*   **Diseño Moderno:** Uso de `CustomTkinter` para una apariencia profesional.
*   **Tema Adaptativo:** Modos **Claro** y **Oscuro** integrados, con adaptación automática de tablas y controles.
*   ** Navegación Intuitiva:** Barra lateral y sistema de pestañas.
---
## 🛠️ Tecnologías Utilizadas
*   **Lenguaje:** Python 3.x
*   **GUI:** `customtkinter` (Interfaz), `tkinter` (Ventanas emergentes/Mensajes).
*   **Base de Datos:** SQLite (Persistencia local).
*   **Reportes:** `reportlab` (Generación de PDFs).
*   **Componentes:** `tkcalendar` (Selectores de fecha), `pillow` (Manejo de imágenes).
---
## 🚀 Instalación y Ejecución
### Requisitos Previos
*   Tener instalado **Python 3.10** o superior.
### Pasos
1.  **Clonar o descargar** este repositorio.
2.  **Instalar dependencias:**
    Abre una terminal en la carpeta del proyecto y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```
    *Contenido de requirements.txt:*
    ```text
    customtkinter
    tkcalendar
    reportlab
    pillow
    ```
3.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```
    *El sistema creará automáticamente la base de datos `gestiongym.db` si no existe.*
---
## 📂 Estructura del Proyecto
El código sigue el patrón de diseño MVC:
```text
GestiónGym/
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt         # Lista de librerías necesarias
├── model/                   # Capa de Datos
│   ├── conexion.py          # Gestión de SQLite
│   ├── cliente.py           # Clase Cliente
│   ├── sesion.py            # Clase Sesion
│   └── ...
├── view/                    # Capa de Presentación (Interfaz)
│   └── app.py               # Ventana Principal, Vistas y Widgets
├── controller/              # Capa de Lógica de Negocio
│   ├── cliente_controller.py
│   ├── sesion_controller.py
│   └── ...
├── utils/                   # Utilidades (PDFs, Helpers)
└── resources/               # Imágenes y Assets
```
