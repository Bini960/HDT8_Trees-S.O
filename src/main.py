import random
import matplotlib.pyplot as plt
from graphviz import Digraph
from src.models.process import Process
from src.trees.bst import BST
from src.trees.splay_tree import SplayTree
from src.trees.red_black_tree import RedBlackTree

def visualize(node, dot=None, count=None, phantom=None):
    # Se inicializan las variables por cada llamada independiente
    if dot is None: dot = Digraph(comment='Tree Snapshot')
    if count is None: count = [0]
    
    # Se verifica que el nodo no sea nulo ni sea el nodo_fantasma del RBT
    if node and node != phantom and count[0] < 15:
        count[0] += 1
        
        # Determinar color: Rojo si color=1, Negro si color=0 (por defecto negro para BST/Splay)
        node_color = "red" if getattr(node, 'color', None) == 1 else "black"
        
        dot.node(str(id(node)), 
            f"PID: {node.process.pid}\nVR: {node.process.vruntime:.1f}", 
            color=node_color, fontcolor=node_color)
        
        # Validación del hijo izquierdo antes de dibujar la arista
        if node.left and node.left != phantom and count[0] < 15:
            dot.edge(str(id(node)), str(id(node.left)))
            visualize(node.left, dot, count, phantom) # Pasar el phantom recursivamente
            
        # Validación del hijo derecho antes de dibujar la arista
        if node.right and node.right != phantom and count[0] < 15:
            dot.edge(str(id(node)), str(id(node.right)))
            visualize(node.right, dot, count, phantom) # Pasar el phantom recursivamente
            
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

# --- PASO 5: ESCENARIO B - LLEGADA SECUENCIAL ---

# 1. Generación de 1000 procesos ordenados (1 a 1000)
procesos_secuenciales = [Process(i, float(i)) for i in range(1, 1001)]
bst_b = BST()
splay_b = SplayTree()
rbt_b = RedBlackTree() # Se agrega el Red-Black Tree

# 2. Inserción secuencial
for p in procesos_secuenciales:
    bst_b.insert(p)
    splay_b.insert(p)
    rbt_b.insert(p)

# 3. Búsqueda del proceso 1000 en las tres estructuras
_, pasos_bst = bst_b.search(1000.0)
_, pasos_splay = splay_b.search(1000.0)
_, pasos_rbt = rbt_b.search(1000.0)

print("-- Resultados Escenario B (Búsqueda del proceso 1000) --")
print(f"BST: {pasos_bst} iteraciones")
print(f"Splay Tree: {pasos_splay} iteraciones")
print(f"Red-Black Tree: {pasos_rbt} iteraciones")

# 4. Generar visualizaciones representativas
visualize(bst_b.root, count=[0]).render('docs/bst_escenario_b', format='png', cleanup=True)
visualize(splay_b.root, count=[0]).render('docs/splay_escenario_b', format='png', cleanup=True)
# Para el RBT se pasa el nodo_fantasma para evitar graficarlo
visualize(rbt_b.root, count=[0], phantom=rbt_b.nodo_fantasma).render('docs/rbt_escenario_b', format='png', cleanup=True)


# --- ESCENARIO C: PROCESO FRECUENTE (Proceso Frecuente de I/O) ---

# 1. Preparación de las estructuras con 1000 procesos aleatorios
procesos_c = [Process(i, random.uniform(0, 5000)) for i in range(1, 1001)]
splay_c = SplayTree()
rbt_c = RedBlackTree() # Integración del Red-Black Tree

for p in procesos_c:
    splay_c.insert(p)
    rbt_c.insert(p)

# 2. Simulación: Buscar el MISMO proceso 50 veces seguidas
proceso_objetivo = random.choice(procesos_c)
iter_splay = []
iter_rbt = []

print(f"\n-- Escenario C: Buscando PID {proceso_objetivo.pid} 50 veces --")

for _ in range(50):
    _, pasos_s = splay_c.search(proceso_objetivo.vruntime)
    _, pasos_r = rbt_c.search(proceso_objetivo.vruntime)
    iter_splay.append(pasos_s)
    iter_rbt.append(pasos_r)

# 3. Gráfica comparativa de iteraciones
plt.figure(figsize=(10, 6))
plt.plot(iter_rbt, label='Red-Black Tree (Estático)', color='red', linestyle='--')
plt.plot(iter_splay, label='Splay Tree (Dinámico)', color='green', linewidth=2)
plt.title('Escenario C: 50 Búsquedas del Mismo Proceso')
plt.xlabel('Número de Intento')
plt.ylabel('Iteraciones')
plt.legend()
plt.grid(True)
plt.savefig('docs/comparativa_escenario_c.png')
plt.show()

print(f"Promedio Splay Tree: {sum(iter_splay)/50:.2f}")
print(f"Promedio Red-Black Tree: {sum(iter_rbt)/50:.2f}")
