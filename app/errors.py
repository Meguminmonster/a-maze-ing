class MazeError(Exception):
    """Base exception for all maze-related erros."""
    pass


class ConfigError(MazeError):
    """Raised when the configuration file is invalid or missing."""
    pass


class MazeGenerationError(MazeError):
    """Raised when maze generation fails due to impossible parameters."""
    pass
