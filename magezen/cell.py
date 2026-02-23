"""Módulo para representar una celda individual del laberinto."""


class Cell:
    """
    Representa una celda en el laberinto.

    Attributes:
    x (int): Coordenada X (columna).
    y (int): Coordenada Y (fila).
    walls (int): Representación en bits de las paredes (N=1, E=2, S=4, W=8).
    visited (bool): Indicador para los algoritmos de generación.
    is_42_block (bool): Indica si la celda es parte del patrón reservado '42'.
    """

    def __init__(self, x: int, y: int) -> None:
        """Inicializa una celda con todas sus paredes cerradas."""
        self.x: int = x
        self.y: int = y
        self.walls: int = 15  # 1111 en binario (N, E, S, W cerrados)
        self.visited: bool = False
        self.is_42_block: bool = False

    def break_wall(self, direction_bit: int) -> None:
        """Rompe una pared específica de la celda."""
        self.walls &= ~direction_bit
