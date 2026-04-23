from .bst import BST
from src.models.node import Node
from src.models.process import Process

class SplayTree(BST):
    """
    Implementación del Árbol Splay.
    Su objetivo es reorganizar la estructura interna, moviendo 
    el nodo de memoria más recientemente utilizado hacia la raíz mediante 
    rotaciones.
    """
    def insert(self, process: Process) -> None:
        # Insercion y splay inmediato
        super().insert(process)
        nodo, _ = super().search(process.vruntime)
        if nodo:
            self._splay(nodo)

    def search(self, vruntime: float) -> tuple:
        # Busca el nodo usando la logica del BST
        nodo, pasos = super().search(vruntime)
        # Ejecuta rotaciones ascendentes si el nodo fue encontrado
        if nodo:
            self._splay(nodo)
        # Retorna la tupla con el nodo y los pasos contados
        return nodo, pasos

    def _splay(self, node: Node) -> None:
        # Bucle condicional ascendente que se detiene al alcanzar la raiz del arbol
        while node.parent:
            #El nodo es hijo directo de la raiz (no existe abuelo)
            if not node.parent.parent:
                # Selecciona y ejecuta la rotacion simple adecuada (zig o zag)
                self._zig(node) if node.parent.left == node else self._zag(node)
            # Caso izquierdo (Zig-Zig): Nodo y padre son hijos izquierdos
            elif node.parent.left == node and node.parent.parent.left == node.parent:
                self._zig(node.parent); self._zig(node)

            # Caso derecho (Zag-Zag): Nodo y padre son hijos derechos
            elif node.parent.right == node and node.parent.parent.right == node.parent:
                self._zag(node.parent); self._zag(node)
            #Casos en donde el nodo y su padre estan en ramas opuestas (Zig-Zag o Zag-Zig)
            else:
                # Caso cruzado izquierdo-derecho (Zig-Zag) 
                if node.parent.left == node:
                    self._zig(node); self._zag(node)
                # Caso cruzado derecho-izquierdo (Zag-Zig)
                else:
                    self._zag(node); self._zig(node)

    def _zig(self, node: Node) -> None:
        # Rotacion a la derecha. Crea punteros temporales al padre y abuelo
        p, g = node.parent, node.parent.parent
        # El hijo derecho del nodo activo reemplaza la rama izquierda del padre
        p.left = node.right
        # Reasigna el puntero padre del sub-arbol desplazado
        if node.right: node.right.parent = p
        # El nodo activo se convierte en el padre original
        node.right, p.parent, node.parent = p, node, g
        # Actualiza la conexion desde la parte superior (abuelo) hacia el nodo que subió
        if g:
            if g.left == p: g.left = node
            else: g.right = node
        # Elimina el enlace superior declarando al nodo activo como la raiz 
        else: self.root = node

    def _zag(self, node: Node) -> None:
        # Rotacion a la izquierda. Crea punteros temporales al padre y abuelo
        p, g = node.parent, node.parent.parent
        # El hijo izquierdo del nodo activo reemplaza la rama derecha del padre
        p.right = node.left
        # Reasigna el puntero padre del sub-arbol desplazado
        if node.left: node.left.parent = p
        #El nodo quita al padre original a su izquierda
        node.left, p.parent, node.parent = p, node, g
        # Actualiza la conexion desde la parte superior (abuelo) hacia el nodo que subió
        if g:
            if g.left == p: g.left = node
            else: g.right = node
        # Elimina el enlace superior declarando al nodo activo como la raiz definitiva   
        else: self.root = node