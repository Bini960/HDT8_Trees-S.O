from .itree import ITree
from src.models.node import Node
from src.models.process import Process

class BST(ITree):
    def __init__(self):
        # Inicializacion de la estructura base
        super().__init__()

    def insert(self, process: Process) -> None:
        # Implementacion de insercion para que deje de ser abstracta
        nuevo = Node(process)
        if self.root is None:
            self.root = nuevo
            return
        curr = self.root
        while True:
            if process.vruntime < curr.process.vruntime:
                if curr.left is None:
                    curr.left = nuevo
                    nuevo.parent = curr
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = nuevo
                    nuevo.parent = curr
                    break
                curr = curr.right

    def search(self, vruntime: float) -> tuple:
        # Implementacion requerida para medir rendimiento
        curr = self.root
        steps = 0
        while curr:
            steps += 1
            if curr.process.vruntime == vruntime:
                return (curr, steps)
            curr = curr.left if vruntime < curr.process.vruntime else curr.right
        return (None, steps)