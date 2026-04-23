from .process import Process

class Node:
    """
    Define la unidad basica de los arboles de busqueda, vinculando un 
    objeto Process con referencias a sus nodos hijos y padre.
    """
    def __init__(self, process: Process):
        # Instancia de la clase Process que contiene los datos
        self.process = process
        # Referencia al hijo izquierdo
        self.left = None
        # Referencia al hijo derecho
        self.right = None
        # Referencia al nodo superior para facilitar rotaciones
        self.parent = None
        # Atributo de color para para Red-Black Tree (1 = rojo, 0 = negro)
        # Se inicializa en 1 por defecto para las nuevas inserciones
        self.color = 1