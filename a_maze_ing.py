"""A-Maze-ing: main entry point.

Usage:
    python3 a_maze_ing.py config.txt

This file is the only one the user interacts with directly.
It ties together the config parser (app/parser.py),
the maze generator (mazegen/generator.py, written by Student A),
and the display logic (app/printer.py).
"""

import sys
from app.errors import ConfigError, MazeError
from app.parser import MazeConfig, parse_config
from app.printer import (
    print_menu,
    render_maze,
    rotate_colour,
    write_output_file,
)


class MazeGenerator:
    """Temporary stub — replace with Student A's real class."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool = True,
        seed: int | None = None,
    ) -> None:
        """Initialise with maze parameters."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.perfect = perfect
        self.seed = seed
        # grid[row][col] = cell value (0-15)
        self.grid: list[list[int]] = []
        self.solution: list[str] = []

    def generate(self) -> None:
        """Generate the maze (stub: fills with fully-walled cells)."""
        # STUB — every cell has all 4 walls closed (value = 15 = 0b1111)
        self.grid = [[15] * self.width for _ in range(self.height)]
        self.solution = []

    def get_grid(self) -> list[list[int]]:
        """Return the 2D grid of cell values."""
        return self.grid

    def get_solution(self) -> list[str]:
        """Return the solution path as a list of 'N'/'E'/'S'/'W' strings."""
        return self.solution


def run(config: MazeConfig) -> None:
    """Main interactive loop: generate, display, and interact with the maze.

    Args:
        config: Parsed MazeConfig from the configuration file.
    """
    wall_colour = "white"
    show_path = False

    gen = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_=config.exit,
        perfect=config.perfect,
        seed=config.seed,
    )

    gen.generate()

    # Write the output file immediately after first generation
    try:
        write_output_file(
            grid=gen.get_grid(),
            entry=config.entry,
            exit_=config.exit,
            path=gen.get_solution(),
            filepath=config.output_file,
        )
        print(f"Maze saved to '{config.output_file}'.")
    except OSError as e:
        print(f"Warning: could not write output file: {e}", file=sys.stderr)

    while True:
        path_coords: list[tuple[int, int]] | None = None
        if show_path:
            path_coords = _solution_to_coords(config.entry, gen.get_solution())

        print("\033[2J\033[H", end="")
        print(
            render_maze(
                grid=gen.get_grid(),
                entry=config.entry,
                exit_=config.exit,
                path=path_coords,
                wall_colour=wall_colour,
            )
        )

        print_menu()
        choice = input().strip()

        if choice == "1":
            # Re-generate: keep same config but get a new random maze
            gen_new = MazeGenerator(
                width=config.width,
                height=config.height,
                entry=config.entry,
                exit_=config.exit,
                perfect=config.perfect,
                seed=None,
            )
            gen_new.generate()
            gen = gen_new
            show_path = False
            try:
                write_output_file(
                    grid=gen.get_grid(),
                    entry=config.entry,
                    exit_=config.exit,
                    path=gen.get_solution(),
                    filepath=config.output_file,
                )
            except OSError as e:
                print(
                    "Warning: could not write output "
                    f"file: {e}", file=sys.stderr
                    )

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            wall_colour = rotate_colour(wall_colour)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def _solution_to_coords(
    start: tuple[int, int],
    directions: list[str],
) -> list[tuple[int, int]]:
    """Convert a list of direction letters into a list of (x, y) coordinates.

    Args:
        start: The starting (x, y) position.
        directions: List of 'N', 'E', 'S', 'W' strings.

    Returns:
        List of (x, y) positions visited along the path, including the start.
    """
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    coords: list[tuple[int, int]] = [start]
    x, y = start
    for direction in directions:
        dx, dy = moves.get(direction, (0, 0))
        x += dx
        y += dy
        coords.append((x, y))
    return coords


def main() -> None:
    """Parse arguments, load config, and start the interactive loop."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        config = parse_config(config_path)
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        run(config)
    except MazeError as e:
        print(f"Maze error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
