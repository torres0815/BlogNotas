import json
import os
from typing import List, Dict, Any

DATA_FILE = "tasks.json"

def load_tasks() -> List[Dict[str, Any]]:
    """Carga las tareas desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks: List[Dict[str, Any]]):
    """Guarda la lista de tareas en el archivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)
