# BlogNotas
# Samuel Torres Atehortua
# CRUD_PROJECT: Aplicación de Lista de Tareas (To-Do List)

Este proyecto implementa una aplicación de escritorio simple para la gestión de tareas (To-Do List) utilizando Python y la librería `tkinter` para la Interfaz Gráfica de Usuario (GUI). El diseño sigue una **arquitectura modular** estricta, separando la lógica de negocio, la persistencia de datos y la interfaz de usuario en módulos distintos, tal como se solicitó.

## Características

*   **CRUD Completo:** Permite Crear, Leer, Actualizar (marcar como completada/pendiente) y Eliminar tareas.
*   **Persistencia de Datos:** Las tareas se guardan automáticamente en un archivo `tasks.json`.
*   **Interfaz Gráfica:** Desarrollada con `tkinter` y `ttk` para una experiencia de usuario nativa.
*   **Modularidad:** Estructura de directorios clara para una fácil escalabilidad y mantenimiento.


## Requisitos

Para ejecutar esta aplicación, necesita tener instalado Python 3.x.

*   **Python:** 3.x
*   **Librerías:** `tkinter` (generalmente viene incluido con la instalación estándar de Python).

Si encuentra un error relacionado con `tkinter` (`ModuleNotFoundError: No module named 'tkinter'`), puede que necesite instalar el paquete específico para su distribución de Linux:

```bash
sudo apt-get update
sudo apt-get install python3-tk
