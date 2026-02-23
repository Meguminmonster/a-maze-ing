"""
Paquete mazegen.
Proporciona la clase MazeGenerator y sus estructuras de datos.
"""

from mazegen.generator import MazeGenerator
from mazegen.maze import Maze
from mazegen.cell import Cell

# __all__ define qué se exporta cuando alguien hace `from mazegen import *`
__all__ = ['MazeGenerator', 'Maze', 'Cell']
