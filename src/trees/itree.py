from abc import ABC, abstractmethod
from src.models.process import Process

class ITree(ABC):
    """
    Interfaz abstracta que establece el contrato para las operaciones 
    principales de los arboles de busqueda en la simulacion.
    """
    def __init__(self):
        # Referencia al nodo raiz del arbol
        self.root = None

    @abstractmethod
    def insert(self, process: Process) -> None:
        # Firma obligatoria para la insercion de un proceso
        pass

    @abstractmethod
    def search(self, vruntime: float) -> tuple:
        # Firma obligatoria para la busqueda; debe retornar (Node, int)
        pass