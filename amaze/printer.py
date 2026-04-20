"""ASCII terminal renderer for the A-Maze-ing project.

Wall bit encoding (from the subject):
    Bit 0 (1) = North
    Bit 1 (2) = East
    Bit 2 (4) = South
    Bit 3 (8) = West

How the ASCII grid works:
    We render each cell as a 3x3 block of characters.
    We draw top + left walls for every cell, then close the right/bottom border.

        +---+---+
        |       |    <- North wall drawn, no East wall between cells
        +   +---+
        |   |        <- No South wall on left, East wall on right
        +---+---+
"""

from typing import Optional

# ANSI colour codes for terminal output
RESET = "\033[0m"
COLOURS = {
    "white":  "\033[97m",
    "cyan":   "\033[96m",
    "yellow": "\033[93m",
    "green":  "\033[92m",
    "red":    "\033[91m",
    "blue":   "\033[94m",
}

# Bit masks for wall directions
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

# Characters used to draw the maze
WALL_H = "---"   # horizontal wall segment
WALL_V = "|"     # vertical wall segment
CORNER = "+"
OPEN_H = "   "   # no horizontal wall
OPEN_V = " "     # no vertical wall


def _has_wall(cell_value: int, direction: int) -> bool:
    """Return True if the given wall bit is set in the cell value.

    Args:
        cell_value: Hex digit (0-15) encoding the cell's walls.
        direction: One of NORTH, EAST, SOUTH, WEST bitmasks.

    Returns:
        True if the wall is closed (bit is 1).
    """
    return bool(cell_value & direction)


def render_maze(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: Optional[list[tuple[int, int]]] = None,
    wall_colour: str = "white",
) -> str:
    """Build a full ASCII string representation of the maze.

    Args:
        grid: 2D list [row][col] of cell values (each 0-15).
        entry: (x, y) coordinates of the entry cell.
        exit_: (x, y) coordinates of the exit cell.
        path: Optional list of (x, y) cells forming the solution path.
        wall_colour: Colour name for walls (from COLOURS dict).

    Returns:
        A multi-line string ready to be printed to the terminal.
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    path_set: set[tuple[int, int]] = set(path) if path else set()
    col = COLOURS.get(wall_colour, COLOURS["white"])

    lines: list[str] = []

    for row in range(height):
        top_line = ""
        mid_line = ""

        for col_idx in range(width):
            cell = grid[row][col_idx]
            cell_pos = (col_idx, row)  # (x, y)

            # --- TOP row of this cell (corner + north wall) ---
            top_line += col + CORNER + RESET
            if _has_wall(cell, NORTH):
                top_line += col + WALL_H + RESET
            else:
                top_line += OPEN_H

            # --- MIDDLE row of this cell (west wall + cell content) ---
            if _has_wall(cell, WEST):
                mid_line += col + WALL_V + RESET
            else:
                mid_line += OPEN_V

            # Decide what character to put inside the cell
            if cell_pos == entry:
                mid_line += COLOURS["green"] + " E " + RESET
            elif cell_pos == exit_:
                mid_line += COLOURS["red"] + " X " + RESET
            elif cell_pos in path_set:
                mid_line += COLOURS["cyan"] + " · " + RESET
            else:
                mid_line += "   "

        # Close the right border
        top_line += col + CORNER + RESET
        if _has_wall(grid[row][width - 1], EAST):
            mid_line += col + WALL_V + RESET
        else:
            mid_line += OPEN_V

        lines.append(top_line)
        lines.append(mid_line)

    # Draw the bottom border of the last row
    bottom_line = ""
    for col_idx in range(width):
        cell = grid[height - 1][col_idx]
        bottom_line += col + CORNER + RESET
        if _has_wall(cell, SOUTH):
            bottom_line += col + WALL_H + RESET
        else:
            bottom_line += OPEN_H
    bottom_line += col + CORNER + RESET
    lines.append(bottom_line)

    return "\n".join(lines)


def print_menu() -> None:
    """Print the interactive menu options to the terminal."""
    print("\n=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze wall colour")
    print("4. Quit")
    print("Choice? (1-4): ", end="", flush=True)


def rotate_colour(current: str) -> str:
    """Return the next colour in the rotation list.

    Args:
        current: The current wall colour name.

    Returns:
        The next colour name in the cycle.
    """
    colour_list = list(COLOURS.keys())
    idx = colour_list.index(current) if current in colour_list else 0
    return colour_list[(idx + 1) % len(colour_list)]


def write_output_file(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[str],
    filepath: str,
) -> None:
    """Write the maze to a file in the required hexadecimal format.

    Format:
        - One row of hex digits per line (no spaces).
        - An empty line.
        - Entry coordinates (x,y).
        - Exit coordinates (x,y).
        - The shortest path as a string of N/E/S/W letters.

    Args:
        grid: 2D list [row][col] of cell values (each 0-15).
        entry: (x, y) entry coordinates.
        exit_: (x, y) exit coordinates.
        path: List of direction strings ('N', 'E', 'S', 'W').
        filepath: Destination file path.

    Raises:
        OSError: If the file cannot be written.
    """
    with open(filepath, "w") as f:
        for row in grid:
            # Each cell is one hex digit (uppercase)
            f.write("".join(format(cell, "X") for cell in row) + "\n")
        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write("".join(path) + "\n")
