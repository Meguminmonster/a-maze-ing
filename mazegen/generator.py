import random
from typing import Tuple, Optional
from collections import deque

from app.errors import MazeGenerationError
from .maze import Maze


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

DIRS = [
    (0, -1, NORTH, SOUTH),
    (1, 0, EAST, WEST),
    (0, 1, SOUTH, NORTH),
    (-1, 0, WEST, EAST),
]


class MazeGenerator:
    """Generate a maze according to the given configuration parameters.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry_pos: Entrance coordinates as (x, y).
        exit_pos: Exit coordinates as (x, y).
        perfect: If True, maze has exactly one path between any two points.
        seed: Optional number that fixes the random generation for reproducibility.
        maze: The Maze object containing the cell grid.
        solution: List of (x, y) coordinates representing the shortest path.
    """
    def __init__(
        self,
        width: int,
        height: int,
        entry_pos: Tuple[int, int],
        exit_pos: Tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize the maze generator with the given configuration.

        Args:
            width: Number of columns.
            height: Number of rows.
            entry_pos: Entrance coordinates as (x, y).
            exit_pos: Exit coordinates as (x, y).
            perfect: If True, maze has exactly one path between any two points.
            seed: Optional number that fixes the random generation for reproducibility.
        """

        self.width = width
        self.height = height
        self.entry_pos = entry_pos
        self.exit_pos = exit_pos
        self.perfect = perfect
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        self.maze = Maze(width, height)
        self.solution: list[tuple[int, int]] = []

    def generate(self) -> Maze:
        """Generate the maze reserving space for the 42 pattern.

        Returns:
            A Maze instance with the generated cell grid.
        Raises:
            MazeGenerationError: If entry or exit is inside the 42 pattern.
        """
        self._reserve_42_pattern()

        sx, sy = self.entry_pos
        ex, ey = self.exit_pos

        if self.maze.get_cell(sx, sy).is_42_block:
            raise MazeGenerationError("Entry is inside the 42 pattern.")
        if self.maze.get_cell(ex, ey).is_42_block:
            raise MazeGenerationError("Exit is inside the 42 pattern.")

        self.maze.get_cell(sx, sy).walls = 15

        self._carve_passages(sx, sy)

        if not self.perfect:
            self._add_cycles()

        self._open_entry_exit()
        self.solution = self._solve_bfs()

        return self.maze

    def _reserve_42_pattern(self) -> None:
        """ Defines and reserves 42 pattern.

        Raises: 
            MazeGenerationError: If maze too small for 42 pattern.
        """
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
                    cell.walls = 15

    def _carve_passages(self, cx: int, cy: int) -> None:
        """Carve passages through the maze using recursive DFS.

        Args:
            cx: Column index of the current cell.
            cy: Row index of the current cell.
        """
        cell = self.maze.get_cell(cx, cy)
        if cell is None or cell.is_42_block:
            return

        cell.visited = True
        dirs = DIRS[:]
        random.shuffle(dirs)

        for dx, dy, w, ow in dirs:
            nx, ny = cx + dx, cy + dy
            neighbor = self.maze.get_cell(nx, ny)

            if neighbor and not neighbor.visited and not neighbor.is_42_block:
                cell.break_wall(w)
                neighbor.break_wall(ow)
                self._carve_passages(nx, ny)

    def _add_cycles(self, attempts: int = 20) -> None:
        for _ in range(attempts):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            cell = self.maze.get_cell(x, y)

            if cell.is_42_block:
                continue

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

    def _solve_bfs(self) -> list[tuple[int, int]]:
        start = self.entry_pos
        goal = self.exit_pos

        queue = deque([start])
        visited = {start: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                break

            for dx, dy, w, _ in DIRS:
                nx, ny = x + dx, y + dy
                cell = self.maze.get_cell(x, y)
                neigh = self.maze.get_cell(nx, ny)

                if neigh is None:
                    continue

                if cell.has_wall(w):
                    continue

                if (nx, ny) not in visited:
                    visited[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        if goal not in visited:
            return []

        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = visited[cur]
        path.append(start)
        path.reverse()

        return path
