from typing import Optional

RESET = "\033[0m"
COLOURS = {
    "white":  "\033[97m",
    "cyan":   "\033[96m",
    "yellow": "\033[93m",
    "green":  "\033[92m",
    "red":    "\033[91m",
    "blue":   "\033[94m",
}

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

WALL_H = "---"
WALL_V = "|"
CORNER = "+"
OPEN_H = "   "
OPEN_V = " "


def _has_wall(cell_value: int, direction: int) -> bool:
    return bool(cell_value & direction)


def render_maze(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: Optional[list[tuple[int, int]]] = None,
    wall_colour: str = "white",
) -> str:
    if not grid or not grid[0]:
        return ""

    height = len(grid)
    width = len(grid[0])

    path_set: set[tuple[int, int]] = set(path) if path else set()
    colour = COLOURS.get(wall_colour, COLOURS["white"])

    lines: list[str] = []

    for row in range(height):
        top_line = ""
        mid_line = ""

        for col_idx in range(width):
            cell = grid[row][col_idx]
            cell_pos = (col_idx, row)

            top_line += colour + CORNER + RESET
            if _has_wall(cell, NORTH):
                top_line += colour + WALL_H + RESET
            else:
                top_line += OPEN_H

            if _has_wall(cell, WEST):
                mid_line += colour + WALL_V + RESET
            else:
                mid_line += OPEN_V

            if cell_pos == entry:
                mid_line += COLOURS["green"] + " E " + RESET
            elif cell_pos == exit_:
                mid_line += COLOURS["red"] + " X " + RESET
            elif cell_pos in path_set:
                mid_line += COLOURS["cyan"] + " · " + RESET
            else:
                mid_line += "   "

        top_line += colour + CORNER + RESET
        if _has_wall(grid[row][width - 1], EAST):
            mid_line += colour + WALL_V + RESET
        else:
            mid_line += OPEN_V

        lines.append(top_line)
        lines.append(mid_line)

    bottom_line = ""
    for col_idx in range(width):
        cell = grid[height - 1][col_idx]
        bottom_line += colour + CORNER + RESET
        if _has_wall(cell, SOUTH):
            bottom_line += colour + WALL_H + RESET
        else:
            bottom_line += OPEN_H
    bottom_line += colour + CORNER + RESET
    lines.append(bottom_line)

    return "\n".join(lines)


def print_menu() -> None:
    print("\n=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze wall colour")
    print("4. Quit")
    print("Choice? (1-4): ", end="", flush=True)


def rotate_colour(current: str) -> str:
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
    with open(filepath, "w") as f:
        for row in grid:
            f.write("".join(f"{cell & 0xF:X}" for cell in row) + "\n")

        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write("".join(path) + "\n")
