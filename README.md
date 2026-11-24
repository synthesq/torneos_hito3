# SynthesQ Torneos

Aplicación web desarrollada en **Django** para la gestión de torneos de esports, integrada con base de datos **MySQL** y soporte para administración de juegos, torneos, estados y autenticación de usuarios.

## Características principales

* **Gestión completa de torneos (CRUD):** creación, visualización detallada, edición y eliminación de torneos.
* **Catálogo de juegos y filtros:** organización por videojuego, estado (*Próximo*, *Activo*, *Inactivo*), cupos y bolsa de premios.
* **Autenticación y control de acceso:** inicio de sesión para administradores y protección de vistas de gestión.
* **Persistencia en MySQL:** integración nativa con MySQL mediante `mysqlclient` y codificación `utf8mb4`.
* **Carga de datos iniciales:** comando personalizado de Django (`cargar_datos`) para poblar la base de datos de prueba al instante.
* **Interfaz personalizada:** plantillas con Bootstrap, estilos propios (`custom.css`), modo oscuro/claro (`app.js`) e identidad visual (`logo.svg`).

---

## Estructura del proyecto

```text
torneos_hito3/
├── config/                 # Configuración global de Django (settings, urls, wsgi/asgi)
├── static/                 # Archivos estáticos (CSS, JS, logo SVG)
├── torneos/                # Aplicación principal
│   ├── management/commands/# Comando personalizado cargar_datos.py
│   ├── migrations/         # Migraciones de base de datos
│   ├── templates/          # Plantillas HTML (registration y torneos)
│   ├── templatetags/       # Filtros personalizados (formatos.py)
│   ├── forms.py            # Formularios
│   ├── models.py           # Modelos (Juego, Torneo)
│   ├── urls.py             # Rutas de la aplicación
│   └── views.py            # Vistas
├── .gitignore
├── manage.py
└── requirements.txt
  
