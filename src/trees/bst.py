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
            # Inicializacion del nodo actual apuntando a la raiz
            current = self.root
            # Inicializacion del contador de iteraciones
            steps = 0

            # Bucle de recorrido mientras no se alcance una hoja nula
            while current is not None:
                # Incremento del contador por la comparacion en el nodo actual
                steps += 1
                
                # Retorno del nodo y los pasos si existe coincidencia exacta
                if current.process.vruntime == vruntime:
                    return (current, steps)
                
                # Desplazamiento al hijo izquierdo si el valor es menor
                elif vruntime < current.process.vruntime:
                    current = current.left
                
                # Desplazamiento al hijo derecho si el valor es mayor
                else:
                    current = current.right

            # Retorno de nulo y los pasos totales si el proceso no se encuentra
            return (None, steps)