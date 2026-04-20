import random
import matplotlib.pyplot as plt
from graphviz import Digraph
from src.models.process import Process
from src.trees.bst import BST
from src.trees.splay_tree import SplayTree

def visualize(node, dot=None, count=[0]):
    # Representacion parcial con Graphviz para no saturar la imagen
    if dot is None: dot = Digraph(comment='BST Snapshot')
    if node and count[0] < 15:
        count[0] += 1
        dot.node(str(id(node)), f"PID: {node.process.pid}\nVR: {node.process.vruntime:.1f}")
        if node.left:
            dot.edge(str(id(node)), str(id(node.left)))
            visualize(node.left, dot, count)
        if node.right:
            dot.edge(str(id(node)), str(id(node.right)))
            visualize(node.right, dot, count)
    return dot

# 1. Simulacion: 1000 procesos aleatorios siguiendo el Paso 4
procesos = [Process(i, random.uniform(0, 5000)) for i in range(1000)]
bst, splay = BST(), SplayTree()

# Insercion de los mismos 1000 procesos en ambas estructuras
for p in procesos:
    bst.insert(p)
    splay.insert(p)

# 2. Medicion: 100 busquedas aleatorias de procesos existentes
muestras = random.sample(procesos, 100)
res_bst, res_splay = [], []

for m in muestras:
    # Ambos metodos search retornan (NodoEncontrado, CantidadDePasos)
    _, s1 = bst.search(m.vruntime)
    _, s2 = splay.search(m.vruntime)
    res_bst.append(s1)
    res_splay.append(s2)

# 3. Grafica Matplotlib comparativa
plt.figure(figsize=(10, 5))
plt.plot(res_bst, label='BST', alpha=0.8, marker='o', markersize=3, color='blue')
plt.plot(res_splay, label='Splay Tree', alpha=0.8, marker='x', markersize=3, color='green')
plt.xlabel('Procesos Evaluados')
plt.ylabel('Cantidad de Iteraciones')
plt.title('Escenario A: Rendimiento BST vs Splay Tree')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# 4. Exportar visualización de árbol (Paso 4.2)
# Genera un archivo PNG en la carpeta docs/
visualize(bst.root).render('docs/bst_graph', format='png', cleanup=True)
snapshot = visualize(splay.root)
snapshot.render('docs/splay_graph', format='png', cleanup=True)


print(f"Promedio BST: {sum(res_bst)/100:.2f}")
print(f"Promedio Splay: {sum(res_splay)/100:.2f}")
