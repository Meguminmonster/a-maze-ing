from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from app.errors import ConfigError

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


class MazeConfig(BaseModel):
    """Represents the configuration of the maze.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry: Entrance coordinates as (x, y).
        exit: Exit coordinates as (x, y).
        output_file: Path to the output text file.
        perfect: If True, maze has exactly one path between any two points.
        seed: Optional number that fixes the random generation for reproducibility.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None

    @field_validator("width")
    @classmethod
    def width_must_be_at_least_2(cls, v: int) -> int:
        if v < 2:
            raise ValueError("WIDTH must be at least 2")
        return v
    @field_validator("height")
    @classmethod
    def height_must_be_at_least_2(cls, v: int) -> int:
        if v < 2:
            raise ValueError("HEIGHT must be at least 2")
        return v
    @model_validator(mode="after")
    def validate_coordinates(self) -> "MazeConfig":
        if not (0 <= self.entry[0] < self.width and 
                0 <= self.entry[1] < self.height):
            raise ValueError(f"ENTRY {self.entry} outside the maze")
        return self

    

def parse_config(filepath: str) -> MazeConfig:
    """Read a configuration file and return a MazeConfig object.

    Args:
        filepath: Path to the configuration text file.
    Returns:
        A MazeConfig instance with the parsed maze settings.
    Raises:
        ConfigError: If the file is missing, malformed, or contains invalid values.
    """
    raw: dict[str, str] = {}

    try:
        with open(filepath, "r") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(
                        f"Line {line_number}: expected 'KEY=VALUE'"
                    )
                key, _, value = line.partition("=")
                raw[key.strip()] = value.strip()
    except FileNotFoundError:
        raise ConfigError(f"Configuration file not found: '{filepath}'")
    except OSError as e:
        raise ConfigError(f"Could not read configuration file: {e}")

    missing = REQUIRED_KEYS - raw.keys()
    if missing:
        raise ConfigError(f"Missing keys: {', '.join(sorted(missing))}")

    try:
        width = int(raw["WIDTH"])
        height = int(raw["HEIGHT"])

        entry_parts = raw["ENTRY"].split(",")
        exit_parts = raw["EXIT"].split(",")
        if len(entry_parts) != 2 or len(exit_parts) != 2:
            raise ConfigError("ENTRY and EXIT must be in 'x,y'")

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

    if width < 2 or height < 2:
        raise ConfigError("WIDTH and HEIGHT must be at least 2")
    if entry == exit_:
        raise ConfigError("ENTRY and EXIT coordinates must be different")
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ConfigError(f"ENTRY {entry} outside the maze ({width}x{height})")
    if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
        raise ConfigError(f"EXIT {exit_} outside the maze ({width}x{height})")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=raw["OUTPUT_FILE"],
        perfect=perfect,
        seed=seed,
    )
