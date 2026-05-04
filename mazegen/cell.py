class Cell:
    """Represents a single cell in the maze grid.

    Each cell tracks its position, which of its four walls are intact,
    whether it has been visited during generation, and whether it belongs
    to the '42' decorative pattern.

    Attributes:
        x: Column index of the cell.
        y: Row index of the cell.
        walls: Bitmask of closed walls (N=1, E=2, S=4, W=8).
        visited: True if the cell has been carved during generation.
        is_42_block: True if the cell is part of the '42' pattern.
    """


    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell with all walls intact.

        Args:
            x: Column index.
            y: Row index.
        """
        self.x: int = x
        self.y: int = y
        self.walls: int = 15
        self.visited: bool = False
        self.is_42_block: bool = False

    def break_wall(self, direction_bit: int) -> None:
        """Remove a wall in the given direction.

        Args:
            direction_bit: Wall to remove, as a bitmask constant (N=1, E=2, S=4, W=8).
        """
        self.walls &= ~direction_bit

    def has_wall(self, direction_bit: int) -> bool:
        """Check if there is a wall in the given direction.

        Args:
            direction_bit: Wall to check, as a bitmask constant (N=1, E=2, S=4, W=8).
        Returns:
            True if the wall exists, False otherwise.
        """
        return bool(self.walls & direction_bit)

    def open_wall_with(self, neighbor: "Cell", direction: int) -> None:
        """Open the shared wall between this cell and its neighbor.

        Args:
            neighbor: Adjacent cell sharing the wall to remove.
            direction: Wall direction to open, as a bitmask constant (N=1, E=2, S=4, W=8).
        """
        opposite = {1: 4, 2: 8, 4: 1, 8: 2}[direction]
        self.break_wall(direction)
        neighbor.break_wall(opposite)

    def __repr__(self) -> str:
        return f"Cell({self.x},{self.y}, walls={self.walls:04b})"
