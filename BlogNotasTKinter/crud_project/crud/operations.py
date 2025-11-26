from typing import List, Optional, Dict
from models.task import Task
from crud.database import load_tasks, save_tasks

# Variable global para mantener el estado de las tareas en memoria
tasks: Dict[int, Task] = {}
next_id: int = 1

def _initialize_tasks():
    """Carga las tareas desde el archivo y establece el próximo ID."""
    global tasks, next_id
    task_list = load_tasks()
    tasks = {task['id']: task for task in task_list}
    if tasks:
        next_id = max(tasks.keys()) + 1
    else:
        next_id = 1

# Inicializar las tareas al cargar el módulo
_initialize_tasks()

def get_all_tasks() -> List[Task]:
    """Retorna todas las tareas."""
    return list(tasks.values())

def add_task(title: str, description: str) -> Task:
    """Agrega una nueva tarea."""
    if not title or not title.strip():
        raise ValueError("El título no puede estar vacío.")
    if len(title) > 100:
        raise ValueError("El título no puede exceder 100 caracteres.")
    if len(description) > 500:
        raise ValueError("La descripción no puede exceder 500 caracteres.")
    global next_id
    new_task: Task = {
        'id': next_id,
        'title': title.strip(),
        'description': description.strip(),
        'completed': False
    }
    tasks[next_id] = new_task
    next_id += 1
    return new_task

def update_task_status(task_id: int, completed: bool) -> Optional[Task]:
    """Actualiza el estado de completado de una tarea."""
    if task_id in tasks:
        tasks[task_id]['completed'] = completed
        return tasks[task_id]
    return None

def delete_task(task_id: int) -> bool:
    """Elimina una tarea por su ID."""
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False

def filter_tasks(query: str, completed_status: Optional[bool] = None) -> List[Task]:
    """Filtra tareas por título/descripción y estado de completado."""
    query_lower = query.lower()

    filtered_list = [
        task for task in tasks.values()
        if query_lower in task['title'].lower() or query_lower in task['description'].lower()
    ]

    if completed_status is not None:
        filtered_list = [
            task for task in filtered_list
            if task['completed'] == completed_status
        ]

    return filtered_list

def save_tasks_on_exit():
    """Guarda las tareas al salir de la aplicación."""
    save_tasks(list(tasks.values()))
