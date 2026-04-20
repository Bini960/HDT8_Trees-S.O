from .itree import ITree
from src.models.process import Process

class BST(ITree):
    """
    Implementacion de un Arbol Binario de Busqueda estandar para la 
    gestion de procesos basada en vruntime.
    """
    def __init__(self):
        # Inicializacion de la estructura base
        super().__init__()

    def insert(self, process: Process) -> None:
        # Logica de insercion comparando vruntimes
        pass

    def search(self, vruntime: float) -> tuple:
        # Busqueda recursiva o iterativa con conteo de pasos
        return (None, 0)