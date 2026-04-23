from .itree import ITree
from src.models.node import Node
from src.models.process import Process

class RedBlackTree(ITree):
    """
    Implementación del Red-Black Tree.
    Su objetivo es garantizar un tiempo de búsqueda logarítmico,
    utilizando reglas de color binarias y rotaciones para evitar el desbalanceo, incluso en el peor caso de inserción.
    """
    def __init__(self):
        # Llama al constructor base para inicializar la estructura
        super().__init__()
        # Crea un proceso vacío para representar los límites del árbol
        proceso_vacio = Process(-1, -1.0)
        # Nodo especial que sirve como hoja vacía y siempre es negro
        self.nodo_fantasma = Node(proceso_vacio)
        # Define el color negro para el nodo fantasma
        self.nodo_fantasma.color = 0
        # Al inicio, la raíz apunta a este nodo vacío
        self.root = self.nodo_fantasma

    def _left_rotate(self, x: Node) -> None:
        # Puntero temporal al hijo derecho que subirá de posición
        y = x.right
        # El hijo izquierdo de y pasa a ser el nuevo hijo derecho de x
        x.right = y.left
        # Si ese hijo no es vacío, actualiza su puntero al padre
        if y.left != self.nodo_fantasma:
            y.left.parent = x
        # El nuevo padre de y será el antiguo padre de x
        y.parent = x.parent
        # Si x era la raíz, ahora y toma su lugar en la cima
        if x.parent is None:
            self.root = y
        # Ajusta la conexión desde el padre original hacia el nuevo hijo y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        # Coloca a x como el hijo izquierdo de y
        y.left = x
        # Finaliza la rotación asignando a y como padre de x
        x.parent = y

    def _right_rotate(self, y: Node) -> None:
        # Puntero temporal al hijo izquierdo que subirá de posición
        x = y.left
        # El hijo derecho de x pasa a ser el nuevo hijo izquierdo de y
        y.left = x.right
        # Si ese hijo no es vacío, actualiza su puntero al padre
        if x.right != self.nodo_fantasma:
            x.right.parent = y
        # El nuevo padre de x será el antiguo padre de y
        x.parent = y.parent
        # Si y era la raíz, ahora x toma su lugar hasta arriba
        if y.parent is None:
            self.root = x
        # Ajusta la conexión desde el padre original hacia el nuevo hijo x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        # Coloca a y como el hijo derecho de x
        x.right = y
        # Finaliza la rotación asignando a x como padre de y
        y.parent = x
    
    def _arreglar(self, k: Node) -> None:
        # Bucle que se ejecuta mientras se rompa la regla de no tener dos rojos seguidos
        while k.parent and k.parent.color == 1:
            # Caso donde el padre de k es un hijo izquierdo
            if k.parent == k.parent.parent.left:
                # El tío es el hijo derecho del abuelo
                u = k.parent.parent.right
                # Regla 1: Si el tío es rojo, solo cambiamos colores
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    # Sube al abuelo para seguir revisando el árbol
                    k = k.parent.parent
                else:
                    # Regla 2: Forma de triángulo, requiere rotación previa
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    # Regla 3: Forma de línea, requiere cambio de color y rotación
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._right_rotate(k.parent.parent)
            # El padre de k es un hijo derecho
            else:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._left_rotate(k.parent.parent)
            # Si llega hasta arriba, se detiene el proceso 
            if k == self.root:
                break
        # La raíz siempre debe ser negra para mantener el equilibrio
        self.root.color = 0

    def insert(self, process: Process) -> None:
        # Crea y configura el nuevo nodo con color rojo inicial 
        nuevo_nodo = Node(process)
        nuevo_nodo.parent = None
        nuevo_nodo.left = self.nodo_fantasma
        nuevo_nodo.right = self.nodo_fantasma
        nuevo_nodo.color = 1

        padre = None
        actual = self.root

        # Recorrido estándar de búsqueda para encontrar la posición de inserción
        while actual != self.nodo_fantasma:
            padre = actual
            if nuevo_nodo.process.vruntime < actual.process.vruntime:
                actual = actual.left
            else:
                actual = actual.right

        # Asigna el padre al nuevo nodo
        nuevo_nodo.parent = padre
        # Si el árbol estaba vacío, el nuevo nodo se convierte en raíz
        if padre is None:
            self.root = nuevo_nodo
        # Decide si el nuevo nodo va a la izquierda o derecha del padre
        elif nuevo_nodo.process.vruntime < padre.process.vruntime:
            padre.left = nuevo_nodo
        else:
            padre.right = nuevo_nodo

        # Si el nodo es raíz, lo vuelve negro y termina
        if nuevo_nodo.parent is None:
            nuevo_nodo.color = 0
            return

        # Si no tiene abuelo, no se requiere balanceo adicional
        if nuevo_nodo.parent.parent is None:
            return

        # Inicia el algoritmo para reparar las propiedades del árbol 
        self._arreglar(nuevo_nodo)

    def search(self, vruntime: float) -> tuple:
        # Inicia la búsqueda desde la raíz del árbol
        actual = self.root
        # Contador para registrar la eficiencia del acceso a memoria
        comparaciones = 0

        # Navega por el árbol hasta encontrar el dato o llegar a una hoja vacía
        while actual != self.nodo_fantasma:
            comparaciones += 1
            # Si los valores coinciden, retorna el nodo y el conteo de pasos
            if vruntime == actual.process.vruntime:
                return actual, comparaciones
            
            # Decide el camino a seguir basándose en el vruntime
            if vruntime < actual.process.vruntime:
                actual = actual.left
            else:
                actual = actual.right

        # Si no se encuentra, devuelve None y el total de pasos realizados
        return None, comparaciones