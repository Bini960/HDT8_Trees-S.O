from .bst import BST
from src.models.node import Node
from src.models.process import Process

class SplayTree(BST):
    def insert(self, process: Process) -> None:
        # Insercion y splay inmediato
        super().insert(process)
        nodo, _ = super().search(process.vruntime)
        if nodo:
            self._splay(nodo)

    def _splay(self, node: Node) -> None:
        # Reorganizacion del arbol hacia la raiz
        while node.parent:
            if not node.parent.parent:
                self._zig(node) if node.parent.left == node else self._zag(node)
            elif node.parent.left == node and node.parent.parent.left == node.parent:
                self._zig(node.parent); self._zig(node)
            elif node.parent.right == node and node.parent.parent.right == node.parent:
                self._zag(node.parent); self._zag(node)
            else:
                if node.parent.left == node:
                    self._zig(node); self._zag(node)
                else:
                    self._zag(node); self._zig(node)

    def _zig(self, node: Node) -> None:
        p, g = node.parent, node.parent.parent
        p.left = node.right
        if node.right: node.right.parent = p
        node.right, p.parent, node.parent = p, node, g
        if g:
            if g.left == p: g.left = node
            else: g.right = node
        else: self.root = node

    def _zag(self, node: Node) -> None:
        p, g = node.parent, node.parent.parent
        p.right = node.left
        if node.left: node.left.parent = p
        node.left, p.parent, node.parent = p, node, g
        if g:
            if g.left == p: g.left = node
            else: g.right = node
        else: self.root = node