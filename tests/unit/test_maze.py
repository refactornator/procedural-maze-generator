"""Unit tests for the maze module."""

import pytest
from maze_generator.maze import Maze, Cell, Direction


class TestDirection:
    """Test the Direction enum."""
    
    def test_direction_values(self):
        """Test that directions have correct delta values."""
        assert Direction.NORTH.delta == (0, -1)
        assert Direction.SOUTH.delta == (0, 1)
        assert Direction.EAST.delta == (1, 0)
        assert Direction.WEST.delta == (-1, 0)
    
    def test_opposite_directions(self):
        """Test that opposite directions are correct."""
        assert Direction.NORTH.opposite == Direction.SOUTH
        assert Direction.SOUTH.opposite == Direction.NORTH
        assert Direction.EAST.opposite == Direction.WEST
        assert Direction.WEST.opposite == Direction.EAST


class TestCell:
    """Test the Cell class."""
    
    def test_cell_creation(self):
        """Test cell creation with default values."""
        cell = Cell(5, 10)
        assert cell.x == 5
        assert cell.y == 10
        assert not cell.visited
        assert not cell.is_start
        assert not cell.is_end
        assert cell.distance is None
        assert cell.parent is None
        assert len(cell.walls) == 4
    
    def test_cell_walls(self):
        """Test cell wall operations."""
        cell = Cell(0, 0)
        
        # Initially all walls should be present
        for direction in Direction:
            assert cell.has_wall(direction)
        
        # Remove a wall
        cell.remove_wall(Direction.NORTH)
        assert not cell.has_wall(Direction.NORTH)
        assert cell.has_wall(Direction.SOUTH)
        
        # Add wall back
        cell.add_wall(Direction.NORTH)
        assert cell.has_wall(Direction.NORTH)
    
    def test_cell_neighbors_coords(self):
        """Test getting neighbor coordinates."""
        cell = Cell(1, 1)
        neighbors = cell.get_neighbors_coords(3, 3)
        
        expected = [(1, 0), (1, 2), (2, 1), (0, 1)]  # N, S, E, W
        assert len(neighbors) == 4
        for coord in expected:
            assert coord in neighbors
    
    def test_cell_neighbors_coords_boundary(self):
        """Test neighbor coordinates at maze boundaries."""
        # Corner cell
        cell = Cell(0, 0)
        neighbors = cell.get_neighbors_coords(3, 3)
        assert len(neighbors) == 2  # Only south and east
        
        # Edge cell
        cell = Cell(1, 0)
        neighbors = cell.get_neighbors_coords(3, 3)
        assert len(neighbors) == 3  # South, east, west
    
    def test_cell_equality(self):
        """Test cell equality comparison."""
        cell1 = Cell(1, 2)
        cell2 = Cell(1, 2)
        cell3 = Cell(2, 1)
        
        assert cell1 == cell2
        assert cell1 != cell3
        assert hash(cell1) == hash(cell2)
        assert hash(cell1) != hash(cell3)


class TestMaze:
    """Test the Maze class."""
    
    def test_maze_creation(self):
        """Test maze creation with valid dimensions."""
        maze = Maze(10, 15)
        assert maze.width == 10
        assert maze.height == 15
        assert len(maze.grid) == 15
        assert len(maze.grid[0]) == 10
        assert maze.start is None
        assert maze.end is None
        assert len(maze.solution_path) == 0
    
    def test_maze_invalid_dimensions(self):
        """Test maze creation with invalid dimensions."""
        with pytest.raises(ValueError):
            Maze(0, 5)
        
        with pytest.raises(ValueError):
            Maze(5, -1)
    
    def test_get_cell(self):
        """Test getting cells from the maze."""
        maze = Maze(5, 5)
        
        # Valid coordinates
        cell = maze.get_cell(2, 3)
        assert cell is not None
        assert cell.x == 2
        assert cell.y == 3
        
        # Invalid coordinates
        assert maze.get_cell(-1, 0) is None
        assert maze.get_cell(0, -1) is None
        assert maze.get_cell(5, 0) is None
        assert maze.get_cell(0, 5) is None
    
    def test_get_neighbors(self):
        """Test getting neighboring cells."""
        maze = Maze(3, 3)
        center_cell = maze.get_cell(1, 1)
        neighbors = maze.get_neighbors(center_cell)
        
        assert len(neighbors) == 4
        expected_coords = [(1, 0), (1, 2), (2, 1), (0, 1)]
        actual_coords = [(cell.x, cell.y) for cell in neighbors]
        
        for coord in expected_coords:
            assert coord in actual_coords
    
    def test_get_unvisited_neighbors(self):
        """Test getting unvisited neighboring cells."""
        maze = Maze(3, 3)
        center_cell = maze.get_cell(1, 1)
        
        # Initially all neighbors are unvisited
        unvisited = maze.get_unvisited_neighbors(center_cell)
        assert len(unvisited) == 4
        
        # Mark one neighbor as visited
        neighbor = maze.get_cell(1, 0)
        neighbor.visited = True
        
        unvisited = maze.get_unvisited_neighbors(center_cell)
        assert len(unvisited) == 3
        assert neighbor not in unvisited
    
    def test_remove_wall_between(self):
        """Test removing walls between adjacent cells."""
        maze = Maze(3, 3)
        cell1 = maze.get_cell(1, 1)
        cell2 = maze.get_cell(1, 0)  # North of cell1
        
        # Initially both cells have walls
        assert cell1.has_wall(Direction.NORTH)
        assert cell2.has_wall(Direction.SOUTH)
        
        # Remove wall between them
        result = maze.remove_wall_between(cell1, cell2)
        assert result is True
        
        # Walls should be removed from both cells
        assert not cell1.has_wall(Direction.NORTH)
        assert not cell2.has_wall(Direction.SOUTH)
    
    def test_remove_wall_between_non_adjacent(self):
        """Test removing walls between non-adjacent cells."""
        maze = Maze(3, 3)
        cell1 = maze.get_cell(0, 0)
        cell2 = maze.get_cell(2, 2)  # Not adjacent
        
        result = maze.remove_wall_between(cell1, cell2)
        assert result is False
    
    def test_set_start_end(self):
        """Test setting start and end positions."""
        maze = Maze(5, 5)
        
        # Set start position
        result = maze.set_start(1, 2)
        assert result is True
        assert maze.start is not None
        assert maze.start.x == 1
        assert maze.start.y == 2
        assert maze.start.is_start is True
        
        # Set end position
        result = maze.set_end(3, 4)
        assert result is True
        assert maze.end is not None
        assert maze.end.x == 3
        assert maze.end.y == 4
        assert maze.end.is_end is True
        
        # Set invalid positions
        assert maze.set_start(-1, 0) is False
        assert maze.set_end(5, 5) is False
    
    def test_reset_methods(self):
        """Test maze reset methods."""
        maze = Maze(3, 3)
        
        # Set up some state
        cell = maze.get_cell(1, 1)
        cell.visited = True
        cell.distance = 5
        cell.parent = maze.get_cell(0, 0)
        maze.solution_path = [cell]
        
        # Reset solution
        maze.reset_solution()
        assert len(maze.solution_path) == 0
        assert cell.distance is None
        assert cell.parent is None
        assert cell.visited is True  # Should not be reset
        
        # Reset visited
        maze.reset_visited()
        assert cell.visited is False
    
    def test_get_random_cell(self):
        """Test getting a random cell."""
        maze = Maze(5, 5)
        cell = maze.get_random_cell()
        
        assert cell is not None
        assert 0 <= cell.x < 5
        assert 0 <= cell.y < 5
    
    def test_maze_iteration(self):
        """Test iterating over maze cells."""
        maze = Maze(2, 3)
        cells = list(maze)
        
        assert len(cells) == 6  # 2 * 3
        
        # Check that all cells are present
        expected_coords = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
        actual_coords = [(cell.x, cell.y) for cell in cells]
        
        for coord in expected_coords:
            assert coord in actual_coords
    
    def test_maze_repr(self):
        """Test maze string representation."""
        maze = Maze(10, 5)
        repr_str = repr(maze)
        assert "Maze(10x5)" in repr_str
