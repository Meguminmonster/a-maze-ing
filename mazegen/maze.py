from typing import List, Optional
from .cell import Cell


class Maze:
    """Represents the maze grid as a 2D array of cells.

    Attributes:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        grid: 2D list of Cell objects representing the maze.
    """
    def __init__(self, width: int, height: int) -> None:
        """Initialize the maze and build the cell grid.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        self.width: int = width
        self.height: int = height
        self.grid: List[List[Cell]] = self._create_grid()

    def _create_grid(self) -> List[List[Cell]]:

        return [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Recover an existing cell by its coordinates.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        Returns:
            The Cell at (x, y), or None if out of bounds.
        """

        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def neighbors(self, x: int, y: int) -> List[Cell]:
        """Return all valid adjacent cells in the four cardinal directions.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        Returns:
            List of neighboring Cell objects.
        """
        result = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            cell = self.get_cell(x + dx, y + dy)
            if cell:
                result.append(cell)
        return result

    def __repr__(self) -> str:
        return f"Maze({self.width}x{self.height})"
