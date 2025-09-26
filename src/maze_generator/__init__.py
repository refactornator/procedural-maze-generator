"""Procedural Maze Generator - A comprehensive maze generation and solving library."""

from .maze import Maze, Cell, Direction
from .algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
    RecursiveBacktrackingGenerator,
)
from .algorithms.solvers import (
    AStarSolver,
    DijkstraSolver,
    BreadthFirstSearchSolver,
    DepthFirstSearchSolver,
)

__version__ = "1.0.0"
__author__ = "Maze Generator Team"
__email__ = "team@mazegenerator.com"

__all__ = [
    "Maze",
    "Cell",
    "Direction",
    "DepthFirstSearchGenerator",
    "KruskalGenerator", 
    "PrimGenerator",
    "RecursiveBacktrackingGenerator",
    "AStarSolver",
    "DijkstraSolver",
    "BreadthFirstSearchSolver",
    "DepthFirstSearchSolver",
]
