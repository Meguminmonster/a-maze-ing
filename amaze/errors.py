"""Custom exceptions for the A-Maze-ing project."""


class MazeError(Exception):
    """Base exception for all maze-related errors."""

    pass


class ConfigError(MazeError):
    """Raised when the configuration file is invalid or missing."""

    pass


class MazeGenerationError(MazeError):
    """Raised when maze generation fails (e.g., impossible parameters)."""

    pass
