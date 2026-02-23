"""Módulo que contiene la estructura de datos del laberinto."""

from typing import List, Optional
from mazegen.cell import Cell


class Maze:
    """
    Estructura de datos que almacena la cuadrícula del laberinto.

    Attributes:
        width (int): Ancho del laberinto.
        height (int): Alto del laberinto.
        grid (List[List[Cell]]): Matriz bidimensional de celdas.
    """

    def __init__(self, width: int, height: int) -> None:
        """Inicializa la cuadrícula del laberinto."""
        self.width: int = width
        self.height: int = height
        self.grid: List[List[Cell]] = self._create_grid()

    def _create_grid(self) -> List[List[Cell]]:
        """Crea la matriz de celdas con todas las paredes cerradas."""
        return [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """
        Devuelve la celda en las coordenadas dadas,
        o None si está fuera de límites.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
