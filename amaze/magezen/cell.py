class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: int = 15  # 1111 en binario (N, E, S, W cerrados)
        self.visited: bool = False
        self.is_42_block: bool = False

    def break_wall(self, direction_bit: int) -> None:
        self.walls &= ~direction_bit
