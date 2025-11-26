from typing import TypedDict

class Task(TypedDict):
    """Define la estructura de una tarea."""
    id: int
    title: str
    description: str
    completed: bool
