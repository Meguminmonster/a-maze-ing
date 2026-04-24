class MazeError(Exception):
    """Base errors"""
    pass


class ConfigError(MazeError):
    """File is invalid or missing."""
    pass


class MazeGenerationError(MazeError):
    """Impossible parameters or similar"""
    pass
