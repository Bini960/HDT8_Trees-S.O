import random
import matplotlib.pyplot as plt
from graphviz import Digraph
from src.models.process import Process
from src.trees.bst import BST
from src.trees.splay_tree import SplayTree
from src.trees.red_black_tree import RedBlackTree

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

# --- ESCENARIO A: LLEGADA ALEATORIA ---

# 1. Generación de 1000 procesos aleatorios (vruntime entre 0 y 5000)
procesos_a = [Process(i, random.uniform(0, 5000)) for i in range(1000)]
bst_a, splay_a, rbt_a = BST(), SplayTree(), RedBlackTree()

# 2. Inserción en las tres estructuras
for p in procesos_a:
    bst_a.insert(p)
    splay_a.insert(p)
    rbt_a.insert(p)

# 3. Visualización de una porción del BST (como solicita el paso 4.2)
visualize(bst_a.root, count=[0]).render('docs/bst_escenario_a', format='png', cleanup=True)

# 4. Búsqueda de 100 procesos al azar para medir rendimiento
muestra_100 = random.sample(procesos_a, 100)
iter_bst, iter_splay, iter_rbt = [], [], []

for m in muestra_100:
    _, steps_b = bst_a.search(m.vruntime)
    _, steps_s = splay_a.search(m.vruntime)
    _, steps_r = rbt_a.search(m.vruntime)
    iter_bst.append(steps_b)
    iter_splay.append(steps_s)
    iter_rbt.append(steps_r)

# 5. Gráfica comparativa de iteraciones
plt.figure(figsize=(12, 6))
plt.plot(iter_bst, label='BST', alpha=0.6)
plt.plot(iter_splay, label='Splay Tree', alpha=0.6)
plt.plot(iter_rbt, label='Red-Black Tree', alpha=0.8, color='red')
plt.title('Escenario A: Comparativa de Iteraciones (Llegada Aleatoria)')
plt.xlabel('Índice de Búsqueda (100 procesos)')
plt.ylabel('Cantidad de Iteraciones')
plt.legend()
plt.grid(True)
plt.savefig('docs/grafica_escenario_a.png')
plt.show()

print(f"-- Promedios Escenario A --")
print(f"Promedio BST: {sum(iter_bst)/100:.2f}")
print(f"Promedio Splay: {sum(iter_splay)/100:.2f}")
print(f"Promedio Red-Black: {sum(iter_rbt)/100:.2f}")

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


