import tkinter as tk
from tkinter import ttk, messagebox
from crud.operations import get_all_tasks, add_task, update_task_status, delete_task, filter_tasks, save_tasks_on_exit

class TodoApp(tk.Tk):
    """
    Clase principal de la aplicación de Lista de Tareas (To-Do List).
    """
    def __init__(self):
        super().__init__()
        self.title("Lista de Tareas (To-Do List)")
        self.geometry("700x500")

        # Configuración de la cuadrícula principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Guardar tareas al cerrar la aplicación
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Frame de entrada y acción (Fila 0)
        self.frame_entrada = ttk.Frame(self, padding="10")
        self.frame_entrada.grid(row=0, column=0, sticky="ew")
        self.crear_widgets_entrada()
        
        # Frame de visualización (Fila 1)
        self.frame_visualizacion = ttk.Frame(self, padding="10")
        self.frame_visualizacion.grid(row=1, column=0, sticky="nsew")
        self.crear_widgets_visualizacion()
        
        # Frame de filtro (Fila 2)
        self.frame_filtro = ttk.Frame(self, padding="10")
        self.frame_filtro.grid(row=2, column=0, sticky="ew")
        self.crear_widgets_filtro()
        
        self.actualizar_lista_tareas()

    def crear_widgets_entrada(self):
        """Crea los widgets para la entrada de nuevas tareas."""
        
        self.frame_entrada.grid_columnconfigure(1, weight=1)
        
        # Título
        ttk.Label(self.frame_entrada, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_titulo = ttk.Entry(self.frame_entrada, width=40)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Descripción
        ttk.Label(self.frame_entrada, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.text_descripcion = tk.Text(self.frame_entrada, height=2, width=40)
        self.text_descripcion.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Botón de acción: Agregar Tarea
        self.btn_agregar = ttk.Button(self.frame_entrada, text="Agregar Tarea", command=self.agregar_tarea_gui)
        self.btn_agregar.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="ns")

    def crear_widgets_visualizacion(self):
        """Crea el Treeview para mostrar la lista de tareas."""
        
        self.frame_visualizacion.grid_columnconfigure(0, weight=1)
        self.frame_visualizacion.grid_rowconfigure(0, weight=1)
        
        # Treeview
        self.tree = ttk.Treeview(self.frame_visualizacion, columns=("ID", "Título", "Descripción", "Completada"), show="headings")
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Título", text="Título", anchor=tk.W)
        self.tree.heading("Descripción", text="Descripción", anchor=tk.W)
        self.tree.heading("Completada", text="Estado", anchor=tk.W)
        
        # Ajuste de columnas
        self.tree.column("ID", width=40, stretch=tk.NO)
        self.tree.column("Título", width=150, stretch=tk.NO)
        self.tree.column("Descripción", stretch=tk.YES)
        self.tree.column("Completada", width=80, stretch=tk.NO)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(self.frame_visualizacion, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Botones de acción debajo del Treeview
        self.frame_acciones = ttk.Frame(self.frame_visualizacion)
        self.frame_acciones.grid(row=1, column=0, columnspan=2, pady=10, sticky="w")
        
        self.btn_completar = ttk.Button(self.frame_acciones, text="Marcar/Desmarcar", command=self.cambiar_estado_tarea)
        self.btn_completar.pack(side=tk.LEFT, padx=5)
        
        self.btn_eliminar = ttk.Button(self.frame_acciones, text="Eliminar Tarea", command=self.eliminar_tarea_gui)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

    def crear_widgets_filtro(self):
        """Crea los widgets para la funcionalidad de filtro/búsqueda."""
        
        self.frame_filtro.grid_columnconfigure(1, weight=1)
        
        # Campo de entrada para el filtro
        ttk.Label(self.frame_filtro, text="Buscar:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_filtro = ttk.Entry(self.frame_filtro, width=40)
        self.entry_filtro.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Botón de acción: Aplicar Filtro
        self.btn_filtrar = ttk.Button(self.frame_filtro, text="Aplicar Filtro", command=self.aplicar_filtro_gui)
        self.btn_filtrar.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        # Botón de acción: Limpiar Filtro
        self.btn_limpiar_filtro = ttk.Button(self.frame_filtro, text="Mostrar Todo", command=self.limpiar_filtro_gui)
        self.btn_limpiar_filtro.grid(row=0, column=3, padx=5, pady=5, sticky="e")
        
        # Asociar la función de filtro a la pulsación de tecla en el campo de filtro
        self.entry_filtro.bind("<KeyRelease>", self.aplicar_filtro_gui)

    def actualizar_lista_tareas(self, tasks_to_show=None):
        """Limpia el Treeview y lo rellena con las tareas proporcionadas o todas las tareas."""
        
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener las tareas a mostrar
        if tasks_to_show is None:
            tasks = get_all_tasks()
        else:
            tasks = tasks_to_show
            
        # Insertar las tareas en el Treeview
        for task in tasks:
            estado = "Completada" if task['completed'] else "Pendiente"
            self.tree.insert("", tk.END, values=(task['id'], task['title'], task['description'], estado))

    def agregar_tarea_gui(self):
        """Maneja la acción de agregar una tarea desde la GUI."""
        title = self.entry_titulo.get().strip()
        description = self.text_descripcion.get("1.0", tk.END).strip()

        try:
            add_task(title, description)
            self.entry_titulo.delete(0, tk.END)
            self.text_descripcion.delete("1.0", tk.END)
            self.actualizar_lista_tareas()
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la tarea: {e}")

    def cambiar_estado_tarea(self):
        """Maneja la acción de cambiar el estado de completado de una tarea."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar una tarea.")
            return
            
        item = seleccion[0]
        values = self.tree.item(item, "values")
        task_id = int(values[0])
        current_status = values[3] == "Completada"
        
        try:
            update_task_status(task_id, not current_status)
            self.actualizar_lista_tareas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el estado: {e}")

    def eliminar_tarea_gui(self):
        """Maneja la acción de eliminar una tarea seleccionada desde la GUI."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar una tarea para eliminar.")
            return
            
        item = seleccion[0]
        task_id = int(self.tree.item(item, "values")[0])
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la tarea con ID {task_id}?"): 
            try:
                if delete_task(task_id):
                    self.actualizar_lista_tareas()
                else:
                    messagebox.showerror("Error", "No se encontró la tarea para eliminar.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la tarea: {e}")

    def aplicar_filtro_gui(self, event=None):
        """Maneja la acción de filtrar tareas desde la GUI."""
        query = self.entry_filtro.get().strip()
        
        # Aquí se podría añadir lógica para filtrar por estado de completado si se añade un widget para ello
        tasks_filtradas = filter_tasks(query)
        
        self.actualizar_lista_tareas(tasks_filtradas)

    def limpiar_filtro_gui(self):
        """Limpia el campo de filtro y muestra todas las tareas."""
        self.entry_filtro.delete(0, tk.END)
        self.actualizar_lista_tareas()

    def on_close(self):
        """Maneja el cierre de la aplicación guardando las tareas."""
        save_tasks_on_exit()
        self.destroy()
