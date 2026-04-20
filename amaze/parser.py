"""Parser for the A-Maze-ing configuration file."""

from dataclasses import dataclass
from typing import Optional

from app.errors import ConfigError

# Keys that MUST be present in the config file
REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


@dataclass
class MazeConfig:
    """Holds all configuration values for maze generation.

    Attributes:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
        output_file: Path to the output file.
        perfect: Whether the maze must have a single path.
        seed: Optional random seed for reproducibility.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def parse_config(filepath: str) -> MazeConfig:
    """Read and validate a KEY=VALUE configuration file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A MazeConfig dataclass with all parsed values.

    Raises:
        ConfigError: If the file is missing, malformed, or has invalid values.
    """
    raw: dict[str, str] = {}

    try:
        with open(filepath, "r") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(
                        f"Line {line_number}: expected 'KEY=VALUE', got: '{line}'"
                    )
                key, _, value = line.partition("=")
                raw[key.strip()] = value.strip()
    except FileNotFoundError:
        raise ConfigError(f"Configuration file not found: '{filepath}'")
    except OSError as e:
        raise ConfigError(f"Could not read configuration file: {e}")

    # Check that all required keys are present
    missing = REQUIRED_KEYS - raw.keys()
    if missing:
        raise ConfigError(f"Missing required keys in config: {', '.join(sorted(missing))}")

    try:
        width = int(raw["WIDTH"])
        height = int(raw["HEIGHT"])

        entry_parts = raw["ENTRY"].split(",")
        exit_parts = raw["EXIT"].split(",")
        if len(entry_parts) != 2 or len(exit_parts) != 2:
            raise ConfigError("ENTRY and EXIT must be in 'x,y' format, e.g. ENTRY=0,0")

        entry = (int(entry_parts[0]), int(entry_parts[1]))
        exit_ = (int(exit_parts[0]), int(exit_parts[1]))

    except ValueError as e:
        raise ConfigError(f"Invalid number in configuration: {e}")

    perfect_raw = raw["PERFECT"].strip().lower()
    if perfect_raw not in ("true", "false"):
        raise ConfigError("PERFECT must be 'True' or 'False'")
    perfect = perfect_raw == "true"

    seed: Optional[int] = None
    if "SEED" in raw:
        try:
            seed = int(raw["SEED"])
        except ValueError:
            raise ConfigError(f"SEED must be an integer, got: '{raw['SEED']}'")

    # Validate logical constraints
    if width < 2 or height < 2:
        raise ConfigError("WIDTH and HEIGHT must be at least 2")
    if entry == exit_:
        raise ConfigError("ENTRY and EXIT coordinates must be different")
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ConfigError(f"ENTRY {entry} is outside the maze bounds ({width}x{height})")
    if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
        raise ConfigError(f"EXIT {exit_} is outside the maze bounds ({width}x{height})")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=raw["OUTPUT_FILE"],
        perfect=perfect,
        seed=seed,
    )
