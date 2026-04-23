import random
import matplotlib.pyplot as plt
from graphviz import Digraph
from src.models.process import Process
from src.trees.bst import BST
from src.trees.splay_tree import SplayTree

def visualize(node, dot=None, count=None):
    # Se inicializan las variables por cada llamada independiente
    if dot is None: dot = Digraph(comment='Tree Snapshot')
    if count is None: count = [0]
    
    if node and count[0] < 15:
        count[0] += 1
        dot.node(str(id(node)), f"PID: {node.process.pid}\nVR: {node.process.vruntime:.1f}")
        
        # Validacion del hijo izquierdo antes de dibujar la arista
        if node.left and count[0] < 15:
            dot.edge(str(id(node)), str(id(node.left)))
            visualize(node.left, dot, count)
            
        # Validacion del hijo derecho antes de dibujar la arista
        if node.right and count[0] < 15:
            dot.edge(str(id(node)), str(id(node.right)))
            visualize(node.right, dot, count)
            
    return dot

# Escenario B (Peor Caso) 

# 1. Generacion de 1000 procesos ordenados ascendentemente (vruntime de 1 a 1000)
procesos_secuenciales = [Process(i, float(i)) for i in range(1, 1001)]
bst_b, splay_b = BST(), SplayTree()

# 2. Insercion secuencial en las estructuras
for p in procesos_secuenciales:
    bst_b.insert(p)
    splay_b.insert(p)

# 3. Busqueda especifica del ultimo proceso insertado (Proceso 1000)
_, pasos_bst = bst_b.search(1000.0)
_, pasos_splay = splay_b.search(1000.0)

print("-- Resultados Escenario B --")
print(f"Iteraciones para encontrar el proceso 1000 en BST: {pasos_bst}")
print(f"Iteraciones para encontrar el proceso 1000 en Splay Tree: {pasos_splay}")

# 4. Mostrar y enviar la visualizacion de la porcion representativa (primeros 15 nodos)
visualize(bst_b.root, count=[0]).render('docs/bst_escenario_b', format='png', cleanup=True)
visualize(splay_b.root, count=[0]).render('docs/splay_escenario_b', format='png', cleanup=True)
