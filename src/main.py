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

# --- ESCENARIO C: PROCESO FRECUENTE (Proceso Frecuente de I/O) ---

# 1. Generación de 1000 procesos en orden aleatorio
procesos = [Process(i, random.uniform(0, 5000)) for i in range(1, 1001)]
splay_tree = SplayTree()

# 2. Inserción de procesos
for p in procesos:
    splay_tree.insert(p)

# 3. Simulación de E/S: Buscar el MISMO proceso 50 veces seguidas
proceso_objetivo = random.choice(procesos)
resultados_iteraciones = []

print(f"-- Resultados Escenario C (PID: {proceso_objetivo.pid}) --")

for i in range(50):
    _, pasos = splay_tree.search(proceso_objetivo.vruntime)
    resultados_iteraciones.append(pasos)
    if i < 3 or i == 49:
        print(f"Búsqueda {i+1}: {pasos} iteraciones")

# 4. Gráfica de rendimiento
plt.figure(figsize=(10, 5))
plt.plot(resultados_iteraciones, marker='o', color='green', label='Splay Tree')
plt.title('splay_escenario_c')
plt.xlabel('Número de Intento')
plt.ylabel('Cantidad de Iteraciones')
plt.legend()
plt.grid(True)
plt.show()

# 5. Visualización del estado final (el proceso buscado debería estar en la raíz)
visualize(splay_tree.root, count=[0]).render('docs/splay_escenario_c', format='png', cleanup=True)
