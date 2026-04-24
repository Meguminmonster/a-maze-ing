import random
from typing import Tuple, Optional
from mazegen.maze import Maze
from mazegen.errors import MazeGenerationError


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

OPPOSITE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}

DIRS = [
    (0, -1, NORTH, SOUTH),
    (1, 0, EAST, WEST),
    (0, 1, SOUTH, NORTH),
    (-1, 0, WEST, EAST),
]


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry_pos: Tuple[int, int],
        exit_pos: Tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:

        self.width = width
        self.height = height
        self.entry_pos = entry_pos
        self.exit_pos = exit_pos
        self.perfect = perfect
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        self.maze = Maze(width, height)

    def generate(self) -> Maze:

        self._reserve_42_pattern()

        sx, sy = self.entry_pos
        self._carve_passages(sx, sy)

        if not self.perfect:
            self._add_cycles()

        self._open_entry_exit()

        return self.maze

    def _reserve_42_pattern(self) -> None:

        pattern = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        ph = len(pattern)
        pw = len(pattern[0])

        if self.width < pw + 2 or self.height < ph + 2:
            raise MazeGenerationError("Maze too small for 42 pattern.")

        ox = (self.width - pw) // 2
        oy = (self.height - ph) // 2

        for y in range(ph):
            for x in range(pw):
                if pattern[y][x] == 1:
                    cell = self.maze.get_cell(ox + x, oy + y)
                    cell.is_42_block = True
                    cell.visited = True
                    cell.walls = 15

    def _carve_passages(self, cx: int, cy: int) -> None:

        cell = self.maze.get_cell(cx, cy)
        cell.visited = True

        dirs = DIRS[:]
        random.shuffle(dirs)

        for dx, dy, w, ow in dirs:
            nx, ny = cx + dx, cy + dy
            neighbor = self.maze.get_cell(nx, ny)

            if (
                neighbor
                and not neighbor.visited
                and not neighbor.is_42_block
            ):
                cell.break_wall(w)
                neighbor.break_wall(ow)
                self._carve_passages(nx, ny)

    def _add_cycles(self, attempts: int = 20) -> None:

        for _ in range(attempts):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            cell = self.maze.get_cell(x, y)

            dx, dy, w, ow = random.choice(DIRS)
            nx, ny = x + dx, y + dy
            neighbor = self.maze.get_cell(nx, ny)

            if neighbor and not neighbor.is_42_block:
                cell.break_wall(w)
                neighbor.break_wall(ow)

    def _open_entry_exit(self) -> None:

        for (x, y) in [self.entry_pos, self.exit_pos]:
            cell = self.maze.get_cell(x, y)

            if y == 0:
                cell.break_wall(NORTH)
            elif y == self.height - 1:
                cell.break_wall(SOUTH)
            elif x == 0:
                cell.break_wall(WEST)
            elif x == self.width - 1:
                cell.break_wall(EAST)
