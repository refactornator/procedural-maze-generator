"""Core maze data structures and representations."""

from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Optional, Set, Dict, Iterator
from dataclasses import dataclass
import random


class Direction(Enum):
    """Enumeration for cardinal directions in the maze."""
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    @property
    def opposite(self) -> Direction:
        """Get the opposite direction."""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self]

    @property
    def delta(self) -> Tuple[int, int]:
        """Get the (dx, dy) offset for this direction."""
        return self.value


@dataclass
class Cell:
    """Represents a single cell in the maze grid."""
    x: int
    y: int
    walls: Set[Direction]
    visited: bool = False
    is_start: bool = False
    is_end: bool = False
    distance: Optional[int] = None
    parent: Optional[Cell] = None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST}
        self.visited = False
        self.is_start = False
        self.is_end = False
        self.distance = None
        self.parent = None

    def has_wall(self, direction: Direction) -> bool:
        """Check if the cell has a wall in the given direction."""
        return direction in self.walls

    def remove_wall(self, direction: Direction) -> None:
        """Remove a wall in the given direction."""
        self.walls.discard(direction)

    def add_wall(self, direction: Direction) -> None:
        """Add a wall in the given direction."""
        self.walls.add(direction)

    def get_neighbors_coords(self, width: int, height: int) -> List[Tuple[int, int]]:
        """Get coordinates of valid neighboring cells within maze bounds."""
        neighbors = []
        for direction in Direction:
            dx, dy = direction.delta
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
        return neighbors

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __lt__(self, other):
        """Less than comparison for priority queue."""
        if not isinstance(other, Cell):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        """Equality comparison."""
        if not isinstance(other, Cell):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y})"


class Maze:
    """Represents a maze with a grid of cells and walls."""

    def __init__(self, width: int, height: int):
        """Initialize a maze with the given dimensions."""
        if width < 1 or height < 1:
            raise ValueError("Maze dimensions must be positive")
        
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = []
        self.start: Optional[Cell] = None
        self.end: Optional[Cell] = None
        self.solution_path: List[Cell] = []
        
        # Initialize the grid with cells
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get the cell at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Get all valid neighboring cells."""
        neighbors = []
        for direction in Direction:
            dx, dy = direction.delta
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """Get all unvisited neighboring cells."""
        return [neighbor for neighbor in self.get_neighbors(cell) if not neighbor.visited]

    def remove_wall_between(self, cell1: Cell, cell2: Cell) -> bool:
        """Remove the wall between two adjacent cells."""
        if not self._are_adjacent(cell1, cell2):
            return False
        
        # Determine the direction from cell1 to cell2
        dx = cell2.x - cell1.x
        dy = cell2.y - cell1.y
        
        if dx == 1:  # cell2 is east of cell1
            cell1.remove_wall(Direction.EAST)
            cell2.remove_wall(Direction.WEST)
        elif dx == -1:  # cell2 is west of cell1
            cell1.remove_wall(Direction.WEST)
            cell2.remove_wall(Direction.EAST)
        elif dy == 1:  # cell2 is south of cell1
            cell1.remove_wall(Direction.SOUTH)
            cell2.remove_wall(Direction.NORTH)
        elif dy == -1:  # cell2 is north of cell1
            cell1.remove_wall(Direction.NORTH)
            cell2.remove_wall(Direction.SOUTH)
        
        return True

    def _are_adjacent(self, cell1: Cell, cell2: Cell) -> bool:
        """Check if two cells are adjacent."""
        dx = abs(cell1.x - cell2.x)
        dy = abs(cell1.y - cell2.y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def set_start(self, x: int, y: int) -> bool:
        """Set the start position of the maze."""
        cell = self.get_cell(x, y)
        if cell:
            if self.start:
                self.start.is_start = False
            self.start = cell
            cell.is_start = True
            return True
        return False

    def set_end(self, x: int, y: int) -> bool:
        """Set the end position of the maze."""
        cell = self.get_cell(x, y)
        if cell:
            if self.end:
                self.end.is_end = False
            self.end = cell
            cell.is_end = True
            return True
        return False

    def reset_solution(self) -> None:
        """Reset the solution path and cell distances."""
        self.solution_path = []
        for row in self.grid:
            for cell in row:
                cell.distance = None
                cell.parent = None

    def reset_visited(self) -> None:
        """Reset the visited status of all cells."""
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def get_random_cell(self) -> Cell:
        """Get a random cell from the maze."""
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return self.grid[y][x]

    def __iter__(self) -> Iterator[Cell]:
        """Iterate over all cells in the maze."""
        for row in self.grid:
            for cell in row:
                yield cell

    def __repr__(self) -> str:
        return f"Maze({self.width}x{self.height})"
