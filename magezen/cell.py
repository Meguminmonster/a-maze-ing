class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: int = 15
        self.visited: bool = False
        self.is_42_block: bool = False

    def break_wall(self, direction_bit: int) -> None:
        self.walls &= ~direction_bit

    def has_wall(self, direction_bit: int) -> bool:
        return bool(self.walls & direction_bit)

    def open_wall_with(self, neighbor: "Cell", direction: int) -> None:
        opposite = {1: 4, 2: 8, 4: 1, 8: 2}[direction]
        self.break_wall(direction)
        neighbor.break_wall(opposite)

    def __repr__(self) -> str:
        return f"Cell({self.x},{self.y}, walls={self.walls:04b})"
