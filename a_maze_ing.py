import sys
from app.errors import ConfigError, MazeError
from app.parser import MazeConfig, parse_config
from app.printer import (
    print_menu,
    render_maze,
    rotate_colour,
    write_output_file,
)
from mazegen.generator import MazeGenerator


def _coords_to_directions(coords: list[tuple[int, int]]) -> list[str]:
    """Convert a list of coordinates into a list of direction strings.

    Args:
        coords: List of (x, y) coordinates representing the solution path.
    Returns:
        List of direction strings (N, S, E, W).
    """
    if not coords or len(coords) < 2:
        return []

    dirs = []
    for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
        if x2 == x1 + 1 and y2 == y1:
            dirs.append("E")
        elif x2 == x1 - 1 and y2 == y1:
            dirs.append("W")
        elif y2 == y1 + 1 and x2 == x1:
            dirs.append("S")
        elif y2 == y1 - 1 and x2 == x1:
            dirs.append("N")
    return dirs


def run(config: MazeConfig) -> None:
    """Generate the maze, save it to a file, and handle the interactive menu.

    Args:
        config: MazeConfig instance with the maze parameters.
    Raises:
        OSError: If the output file cannot be written.
    """
    wall_colour = "white"
    show_path = False

    gen = MazeGenerator(
        width=config.width,
        height=config.height,
        entry_pos=config.entry,
        exit_pos=config.exit,
        perfect=config.perfect,
        seed=config.seed,
    )

    maze = gen.generate()
    grid = [[cell.walls for cell in row] for row in maze.grid]
    solution = gen.solution

    try:
        write_output_file(
            grid=grid,
            entry=config.entry,
            exit_=config.exit,
            path=_coords_to_directions(solution),
            filepath=config.output_file,
        )
        print(f"Maze saved to '{config.output_file}'.")
    except OSError as e:
        print(f"Warning: could not write output file: {e}", file=sys.stderr)

    while True:
        path_coords = solution if show_path else None

        print("\033[2J\033[H", end="")
        print(
            render_maze(
                grid=grid,
                entry=config.entry,
                exit_=config.exit,
                path=path_coords,
                wall_colour=wall_colour,
            )
        )

        print_menu()
        choice = input().strip()

        if choice == "1":
            gen = MazeGenerator(
                width=config.width,
                height=config.height,
                entry_pos=config.entry,
                exit_pos=config.exit,
                perfect=config.perfect,
                seed=None,
            )
            maze = gen.generate()
            grid = [[cell.walls for cell in row] for row in maze.grid]
            solution = gen.solution
            show_path = False

            try:
                write_output_file(
                    grid=grid,
                    entry=config.entry,
                    exit_=config.exit,
                    path=_coords_to_directions(solution),
                    filepath=config.output_file,
                )
            except OSError as e:
                print(f"Warning: could not write file: {e}", file=sys.stderr)

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            wall_colour = rotate_colour(wall_colour)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def main() -> None:
    """Parse command-line arguments, load the configuration and run the maze.

    Raises:
        ConfigError: If the configuration file is missing or invalid.
        MazeError: If the maze cannot be generated with the given parameters.
        KeyboardInterrupt: If the user cancels the operation.
    """
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
