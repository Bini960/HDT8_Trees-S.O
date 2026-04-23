from .itree import ITree
from src.models.node import Node
from src.models.process import Process

class BST(ITree):
    """
    Implementa un Árbol Binario de Búsqueda estándar.
    Su objetivo es organizar los procesos del sistema según su 
    tiempo de ejecución, enviando los menores a la izquierda 
    y los mayores a la derecha.
    """
    def __init__(self):
        # Llama al constructor de la clase abstracta ITree para inicializar la raiz en None
        super().__init__()

    def insert(self, process: Process) -> None:
        # Implementacion de insercion para que deje de ser abstracta
        nuevo = Node(process)
        # Si el arbol esta vacio, el nuevo nodo se asigna directamente como la raiz
        if self.root is None:
            self.root = nuevo
            return
        # Puntero de ayuda para recorrer la estructura comenzando desde la raiz
        curr = self.root
        while True:
            # Evalua la llave de ordenamiento (vruntime) para decidir la rama
            if process.vruntime < curr.process.vruntime:
                # Si el puntero izquierdo esta libre, se conecta el nodo
                if curr.left is None:
                    curr.left = nuevo
                    nuevo.parent = curr
                    break
                # Desplaza el puntero principal al hijo izquierdo
                curr = curr.left
            else:
                # Si el puntero derecho esta libre, se conecta al nodo
                if curr.right is None:
                    curr.right = nuevo
                    nuevo.parent = curr
                    break
                # Desplaza el puntero principal al hijo derecho
                curr = curr.right

    def search(self, vruntime: float) -> tuple:
        # Puntero de ayuda para recorrer la estructura comenzando desde la raiz
        curr = self.root
        # Acumulador para llevar el control algoritmico del rendimiento
        steps = 0
        # Continua el bucle mientras no se alcance un extremo nulo
        while curr:
            # Incrementa el contador por el acceso en memoria del nodo actual
            steps += 1
            if curr.process.vruntime == vruntime:
                return (curr, steps)
            curr = curr.left if vruntime < curr.process.vruntime else curr.right
        # Retorna un puntero vacio y los pasos totales ante un fallo al buscar
        return (None, steps)