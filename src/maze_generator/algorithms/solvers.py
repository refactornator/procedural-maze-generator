"""Maze solving algorithms."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Set, Dict
import heapq
from collections import deque
import math

from ..maze import Maze, Cell, Direction


class MazeSolver(ABC):
    """Abstract base class for maze solving algorithms."""

    @abstractmethod
    def solve(self, maze: Maze) -> List[Cell]:
        """Solve the maze and return the path from start to end."""
        pass

    def _reconstruct_path(self, end_cell: Cell) -> List[Cell]:
        """Reconstruct the path from start to end using parent pointers."""
        path = []
        current = end_cell
        while current:
            path.append(current)
            current = current.parent
        return list(reversed(path))

    def _get_accessible_neighbors(self, maze: Maze, cell: Cell) -> List[Cell]:
        """Get neighbors that are accessible (no wall between them)."""
        neighbors = []
        for direction in Direction:
            if not cell.has_wall(direction):
                dx, dy = direction.delta
                neighbor = maze.get_cell(cell.x + dx, cell.y + dy)
                if neighbor:
                    neighbors.append(neighbor)
        return neighbors


class BreadthFirstSearchSolver(MazeSolver):
    """Solve mazes using Breadth-First Search algorithm."""

    def solve(self, maze: Maze) -> List[Cell]:
        """Solve the maze using BFS."""
        if not maze.start or not maze.end:
            return []

        maze.reset_solution()
        
        queue = deque([maze.start])
        maze.start.distance = 0
        visited = {maze.start}
        
        while queue:
            current = queue.popleft()
            
            if current == maze.end:
                path = self._reconstruct_path(current)
                maze.solution_path = path
                return path
            
            for neighbor in self._get_accessible_neighbors(maze, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.distance = current.distance + 1
                    neighbor.parent = current
                    queue.append(neighbor)
        
        return []


class DepthFirstSearchSolver(MazeSolver):
    """Solve mazes using Depth-First Search algorithm."""

    def solve(self, maze: Maze) -> List[Cell]:
        """Solve the maze using DFS."""
        if not maze.start or not maze.end:
            return []

        maze.reset_solution()
        
        stack = [maze.start]
        visited = {maze.start}
        
        while stack:
            current = stack.pop()
            
            if current == maze.end:
                path = self._reconstruct_path(current)
                maze.solution_path = path
                return path
            
            for neighbor in self._get_accessible_neighbors(maze, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.parent = current
                    stack.append(neighbor)
        
        return []


class DijkstraSolver(MazeSolver):
    """Solve mazes using Dijkstra's algorithm."""

    def solve(self, maze: Maze) -> List[Cell]:
        """Solve the maze using Dijkstra's algorithm."""
        if not maze.start or not maze.end:
            return []

        maze.reset_solution()
        
        # Priority queue: (distance, cell)
        pq = [(0, maze.start)]
        maze.start.distance = 0
        visited = set()
        
        while pq:
            current_distance, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == maze.end:
                path = self._reconstruct_path(current)
                maze.solution_path = path
                return path
            
            for neighbor in self._get_accessible_neighbors(maze, current):
                if neighbor not in visited:
                    new_distance = current_distance + 1
                    
                    if neighbor.distance is None or new_distance < neighbor.distance:
                        neighbor.distance = new_distance
                        neighbor.parent = current
                        heapq.heappush(pq, (new_distance, neighbor))
        
        return []


class AStarSolver(MazeSolver):
    """Solve mazes using A* algorithm."""

    def solve(self, maze: Maze) -> List[Cell]:
        """Solve the maze using A* algorithm."""
        if not maze.start or not maze.end:
            return []

        maze.reset_solution()
        
        def heuristic(cell: Cell) -> float:
            """Manhattan distance heuristic."""
            return abs(cell.x - maze.end.x) + abs(cell.y - maze.end.y)
        
        # Priority queue: (f_score, cell)
        pq = [(heuristic(maze.start), maze.start)]
        maze.start.distance = 0
        g_scores = {maze.start: 0}
        f_scores = {maze.start: heuristic(maze.start)}
        visited = set()
        
        while pq:
            current_f, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == maze.end:
                path = self._reconstruct_path(current)
                maze.solution_path = path
                return path
            
            for neighbor in self._get_accessible_neighbors(maze, current):
                if neighbor in visited:
                    continue
                
                tentative_g = g_scores[current] + 1
                
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    neighbor.parent = current
                    neighbor.distance = tentative_g
                    g_scores[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor)
                    f_scores[neighbor] = f_score
                    heapq.heappush(pq, (f_score, neighbor))
        
        return []


class WallFollowerSolver(MazeSolver):
    """Solve mazes using the wall follower (right-hand rule) algorithm."""

    def solve(self, maze: Maze) -> List[Cell]:
        """Solve the maze using wall follower algorithm."""
        if not maze.start or not maze.end:
            return []

        maze.reset_solution()
        
        current = maze.start
        path = [current]
        visited_states = set()
        
        # Start facing north
        facing = Direction.NORTH
        
        while current != maze.end:
            # Create a state tuple to detect loops
            state = (current.x, current.y, facing)
            if state in visited_states:
                # We're in a loop, this algorithm won't work for this maze
                return []
            visited_states.add(state)
            
            # Try to turn right and move
            right_direction = self._turn_right(facing)
            if not current.has_wall(right_direction):
                # Turn right and move
                facing = right_direction
                dx, dy = facing.delta
                next_cell = maze.get_cell(current.x + dx, current.y + dy)
                if next_cell:
                    current = next_cell
                    path.append(current)
                    continue
            
            # Try to move forward
            if not current.has_wall(facing):
                dx, dy = facing.delta
                next_cell = maze.get_cell(current.x + dx, current.y + dy)
                if next_cell:
                    current = next_cell
                    path.append(current)
                    continue
            
            # Turn left
            facing = self._turn_left(facing)
        
        maze.solution_path = path
        return path

    def _turn_right(self, direction: Direction) -> Direction:
        """Turn right from the current direction."""
        turns = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
        }
        return turns[direction]

    def _turn_left(self, direction: Direction) -> Direction:
        """Turn left from the current direction."""
        turns = {
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH,
        }
        return turns[direction]
