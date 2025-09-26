"""Maze generation algorithms."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Set, Optional, Tuple
import random
from collections import deque

from ..maze import Maze, Cell, Direction


class MazeGenerator(ABC):
    """Abstract base class for maze generation algorithms."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize the generator with an optional random seed."""
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    @abstractmethod
    def generate(self, maze: Maze) -> None:
        """Generate a maze using the specific algorithm."""
        pass

    def _reset_maze(self, maze: Maze) -> None:
        """Reset the maze to its initial state with all walls intact."""
        maze.reset_visited()
        for cell in maze:
            cell.walls = {Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST}


class DepthFirstSearchGenerator(MazeGenerator):
    """Generate mazes using Depth-First Search (Recursive Backtracking) algorithm."""

    def generate(self, maze: Maze) -> None:
        """Generate a maze using DFS algorithm."""
        self._reset_maze(maze)
        
        # Start from a random cell
        current = maze.get_random_cell()
        current.visited = True
        stack = [current]
        
        while stack:
            current = stack[-1]
            unvisited_neighbors = maze.get_unvisited_neighbors(current)
            
            if unvisited_neighbors:
                # Choose a random unvisited neighbor
                next_cell = random.choice(unvisited_neighbors)
                next_cell.visited = True
                
                # Remove wall between current and next cell
                maze.remove_wall_between(current, next_cell)
                
                # Add next cell to stack
                stack.append(next_cell)
            else:
                # Backtrack
                stack.pop()


class RecursiveBacktrackingGenerator(DepthFirstSearchGenerator):
    """Alias for DepthFirstSearchGenerator for clarity."""
    pass


class PrimGenerator(MazeGenerator):
    """Generate mazes using Prim's algorithm."""

    def generate(self, maze: Maze) -> None:
        """Generate a maze using Prim's algorithm."""
        self._reset_maze(maze)
        
        # Start with a random cell
        start_cell = maze.get_random_cell()
        start_cell.visited = True
        
        # Add all walls of the starting cell to the wall list
        walls = []
        for direction in Direction:
            dx, dy = direction.delta
            neighbor = maze.get_cell(start_cell.x + dx, start_cell.y + dy)
            if neighbor:
                walls.append((start_cell, neighbor, direction))
        
        while walls:
            # Pick a random wall from the list
            wall_index = random.randint(0, len(walls) - 1)
            current_cell, neighbor_cell, direction = walls.pop(wall_index)
            
            # If only one of the cells is visited
            if current_cell.visited != neighbor_cell.visited:
                # Make the unvisited cell part of the maze
                if not neighbor_cell.visited:
                    neighbor_cell.visited = True
                    maze.remove_wall_between(current_cell, neighbor_cell)
                    
                    # Add the neighboring walls of the new cell
                    for new_direction in Direction:
                        dx, dy = new_direction.delta
                        new_neighbor = maze.get_cell(neighbor_cell.x + dx, neighbor_cell.y + dy)
                        if new_neighbor and not new_neighbor.visited:
                            walls.append((neighbor_cell, new_neighbor, new_direction))


class KruskalGenerator(MazeGenerator):
    """Generate mazes using Kruskal's algorithm with Union-Find."""

    def generate(self, maze: Maze) -> None:
        """Generate a maze using Kruskal's algorithm."""
        self._reset_maze(maze)
        
        # Initialize Union-Find data structure
        parent = {}
        rank = {}
        
        def find(cell: Cell) -> Cell:
            if cell not in parent:
                parent[cell] = cell
                rank[cell] = 0
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]
        
        def union(cell1: Cell, cell2: Cell) -> bool:
            root1 = find(cell1)
            root2 = find(cell2)
            
            if root1 == root2:
                return False
            
            if rank[root1] < rank[root2]:
                parent[root1] = root2
            elif rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root2] = root1
                rank[root1] += 1
            
            return True
        
        # Create list of all possible edges (walls between adjacent cells)
        edges = []
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell:
                    # Add edge to right neighbor
                    if x < maze.width - 1:
                        right_neighbor = maze.get_cell(x + 1, y)
                        if right_neighbor:
                            edges.append((cell, right_neighbor))
                    
                    # Add edge to bottom neighbor
                    if y < maze.height - 1:
                        bottom_neighbor = maze.get_cell(x, y + 1)
                        if bottom_neighbor:
                            edges.append((cell, bottom_neighbor))
        
        # Shuffle edges randomly
        random.shuffle(edges)
        
        # Process edges in random order
        for cell1, cell2 in edges:
            if union(cell1, cell2):
                maze.remove_wall_between(cell1, cell2)


class WilsonGenerator(MazeGenerator):
    """Generate mazes using Wilson's algorithm (Loop-Erased Random Walk)."""

    def generate(self, maze: Maze) -> None:
        """Generate a maze using Wilson's algorithm."""
        self._reset_maze(maze)
        
        # Start with a random cell as part of the maze
        start_cell = maze.get_random_cell()
        start_cell.visited = True
        
        # Get list of unvisited cells
        unvisited = [cell for cell in maze if not cell.visited]
        
        while unvisited:
            # Start a random walk from a random unvisited cell
            current = random.choice(unvisited)
            path = [current]
            
            # Perform random walk until we hit a visited cell
            while not current.visited:
                neighbors = maze.get_neighbors(current)
                if neighbors:
                    next_cell = random.choice(neighbors)
                    
                    # If we've been to this cell before in this walk, erase the loop
                    if next_cell in path:
                        loop_start = path.index(next_cell)
                        path = path[:loop_start + 1]
                        current = next_cell
                    else:
                        path.append(next_cell)
                        current = next_cell
                else:
                    break
            
            # Add the path to the maze
            for i in range(len(path) - 1):
                path[i].visited = True
                maze.remove_wall_between(path[i], path[i + 1])
                if path[i] in unvisited:
                    unvisited.remove(path[i])
            
            # Update unvisited list
            unvisited = [cell for cell in unvisited if not cell.visited]
