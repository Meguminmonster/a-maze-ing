"""Módulo principal para la generación de laberintos."""

import random
from typing import Tuple, Optional
from mazegen.maze import Maze


class MazeGenerator:
    """Genera el laberinto aplicando el algoritmo Recursive Backtracker."""

    def __init__(
        self, width: int, height: int, entry_pos: Tuple[int, int],
        exit_pos: Tuple[int, int], perfect: bool = True,
        seed: Optional[int] = None
    ) -> None:
        """Inicializa el generador con los parámetros requeridos."""
        self.width: int = width
        self.height: int = height
        self.entry_pos: Tuple[int, int] = entry_pos
        self.exit_pos: Tuple[int, int] = exit_pos
        self.perfect: bool = perfect
        self.seed: Optional[int] = seed
        self.maze: Maze = Maze(width, height)

        if self.seed is not None:
            random.seed(self.seed)

    def generate(self) -> Maze:
        """Ejecuta el algoritmo principal de generación de laberintos."""
        self._reserve_42_pattern()

        start_x, start_y = self.entry_pos
        self._carve_passages(start_x, start_y)

        self._open_entry_exit()

        return self.maze

    def _reserve_42_pattern(self) -> None:
        """Marca las celdas centrales para formar un '42' cerrado."""
        pattern = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        p_height = len(pattern)
        p_width = len(pattern[0])

        if self.width < p_width + 2 or self.height < p_height + 2:
            print("Error: El tamaño del laberinto es demasiado pequeño "
                  "para el patrón '42'.")
            return

        start_x = (self.width - p_width) // 2
        start_y = (self.height - p_height) // 2

        for y in range(p_height):
            for x in range(p_width):
                if pattern[y][x] == 1:
                    cell = self.maze.get_cell(start_x + x, start_y + y)
                    if cell:
                        cell.is_42_block = True
                        cell.visited = True

    def _open_entry_exit(self) -> None:
        """Abre la pared externa para la entrada y la salida."""
        for px, py in [self.entry_pos, self.exit_pos]:
            cell = self.maze.get_cell(px, py)
            if not cell:
                continue

            if py == 0:
                cell.break_wall(1)  # Borde superior: rompemos Norte (1)
            elif py == self.height - 1:
                cell.break_wall(4)  # Borde inferior: rompemos Sur (4)
            elif px == 0:
                cell.break_wall(8)  # Borde izquierdo: rompemos Oeste (8)
            elif px == self.width - 1:
                cell.break_wall(2)  # Borde derecho: rompemos Este (2)

    def _carve_passages(self, cx: int, cy: int) -> None:
        """Esculpe los pasillos usando Recursive Backtracking."""
        current_cell = self.maze.get_cell(cx, cy)
        if not current_cell:
            return
        current_cell.visited = True

        directions = [
            (0, -1, 1, 4),  # Norte
            (1, 0, 2, 8),   # Este
            (0, 1, 4, 1),   # Sur
            (-1, 0, 8, 2)   # Oeste
        ]
        random.shuffle(directions)

        for dx, dy, wall_bit, opp_wall_bit in directions:
            nx, ny = cx + dx, cy + dy
            neighbor = self.maze.get_cell(nx, ny)

            if (neighbor and not neighbor.visited and
                    not getattr(neighbor, 'is_42_block', False)):
                current_cell.break_wall(wall_bit)
                neighbor.break_wall(opp_wall_bit)
                self._carve_passages(nx, ny)
