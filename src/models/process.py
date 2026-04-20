class Process:
    """
    Representa un proceso del sistema operativo, almacenando su identificador 
    y su tiempo de ejecución virtual (vruntime) para la planificación.
    """
    def __init__(self, pid: int, vruntime: float):
        # Asigna el identificador unico del proceso
        self.pid = pid
        # Asigna el tiempo de ejecución virtual utilizado como llave de ordenamiento
        self.vruntime = vruntime