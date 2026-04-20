from .bst import BST
from src.models.node import Node
from src.models.process import Process

class SplayTree(BST):
    """
    Implementacion de un Splay Tree que reorganiza su estructura mediante 
    movimientos zig y zag al acceder a los nodos.
    """
    def __init__(self):
        # Inicializacion de la estructura base BST
        super().__init__()

    def insert(self, process: Process) -> None:
        # Insercion seguida de la operacion splay hacia la raiz
        pass
    
    def search(self, vruntime: float) -> tuple:
        # Llamada al metodo search de la superclase BST
        found_node, steps = super().search(vruntime)
        
        # Ejecucion de rotaciones ascendentes si la busqueda fue exitosa
        if found_node is not None:
            self._splay(found_node)
            
        # Retorno de la tupla (Par de valores) requerida manteniendo el conteo de pasos original
        return (found_node, steps)

    def _splay(self, node: Node) -> None:
        # Ejecucion de rotaciones ascendentes hasta la raiz
        pass

    def _zig(self, node: Node) -> None:
        # Rotacion a la derecha 
        pass

    def _zag(self, node: Node) -> None:
        # Rotacion a la izquierda 
        pass