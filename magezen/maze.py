from typing import List, Optional
from .cell import Cell


class Maze:

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: List[List[Cell]] = self._create_grid()

    def _create_grid(self) -> List[List[Cell]]:

        return [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:

        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def neighbors(self, x: int, y: int) -> List[Cell]:

        result = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            cell = self.get_cell(x + dx, y + dy)
            if cell:
                result.append(cell)
        return result

    def __repr__(self) -> str:
        return f"Maze({self.width}x{self.height})"
