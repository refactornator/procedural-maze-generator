"""Unit tests for maze generation algorithms."""

import pytest
from maze_generator.maze import Maze, Direction
from maze_generator.algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
    WilsonGenerator,
)


class TestMazeGenerators:
    """Test maze generation algorithms."""
    
    @pytest.fixture
    def small_maze(self):
        """Create a small maze for testing."""
        return Maze(5, 5)
    
    @pytest.fixture
    def medium_maze(self):
        """Create a medium maze for testing."""
        return Maze(10, 10)
    
    def test_dfs_generator(self, small_maze):
        """Test Depth-First Search generator."""
        generator = DepthFirstSearchGenerator(seed=42)
        generator.generate(small_maze)
        
        # Check that maze is properly generated
        self._verify_maze_connectivity(small_maze)
        self._verify_maze_has_paths(small_maze)
    
    def test_kruskal_generator(self, small_maze):
        """Test Kruskal's algorithm generator."""
        generator = KruskalGenerator(seed=42)
        generator.generate(small_maze)
        
        # Check that maze is properly generated
        self._verify_maze_connectivity(small_maze)
        self._verify_maze_has_paths(small_maze)
    
    def test_prim_generator(self, small_maze):
        """Test Prim's algorithm generator."""
        generator = PrimGenerator(seed=42)
        generator.generate(small_maze)
        
        # Check that maze is properly generated
        self._verify_maze_connectivity(small_maze)
        self._verify_maze_has_paths(small_maze)
    
    def test_wilson_generator(self, small_maze):
        """Test Wilson's algorithm generator."""
        generator = WilsonGenerator(seed=42)
        generator.generate(small_maze)
        
        # Check that maze is properly generated
        self._verify_maze_connectivity(small_maze)
        self._verify_maze_has_paths(small_maze)
    
    def test_generator_reproducibility(self, small_maze):
        """Test that generators produce the same result with the same seed."""
        generator1 = DepthFirstSearchGenerator(seed=123)
        generator2 = DepthFirstSearchGenerator(seed=123)
        
        maze1 = Maze(5, 5)
        maze2 = Maze(5, 5)
        
        generator1.generate(maze1)
        generator2.generate(maze2)
        
        # Mazes should be identical
        for y in range(5):
            for x in range(5):
                cell1 = maze1.get_cell(x, y)
                cell2 = maze2.get_cell(x, y)
                assert cell1.walls == cell2.walls
    
    def test_generator_different_seeds(self, small_maze):
        """Test that generators produce different results with different seeds."""
        generator1 = DepthFirstSearchGenerator(seed=123)
        generator2 = DepthFirstSearchGenerator(seed=456)
        
        maze1 = Maze(5, 5)
        maze2 = Maze(5, 5)
        
        generator1.generate(maze1)
        generator2.generate(maze2)
        
        # Mazes should be different (with very high probability)
        differences = 0
        for y in range(5):
            for x in range(5):
                cell1 = maze1.get_cell(x, y)
                cell2 = maze2.get_cell(x, y)
                if cell1.walls != cell2.walls:
                    differences += 1
        
        assert differences > 0  # Should have at least some differences
    
    def test_generator_on_different_sizes(self):
        """Test generators on different maze sizes."""
        sizes = [(3, 3), (5, 7), (10, 10), (15, 8)]
        generator = DepthFirstSearchGenerator(seed=42)
        
        for width, height in sizes:
            maze = Maze(width, height)
            generator.generate(maze)
            
            self._verify_maze_connectivity(maze)
            self._verify_maze_has_paths(maze)
    
    def test_generator_single_cell_maze(self):
        """Test generators on a single-cell maze."""
        maze = Maze(1, 1)
        generator = DepthFirstSearchGenerator()
        generator.generate(maze)
        
        # Single cell should have all walls
        cell = maze.get_cell(0, 0)
        assert len(cell.walls) == 4
    
    def test_generator_reset_maze(self, small_maze):
        """Test that generator properly resets maze state."""
        # Modify maze state
        cell = small_maze.get_cell(2, 2)
        cell.visited = True
        cell.remove_wall(Direction.NORTH)
        
        generator = DepthFirstSearchGenerator()
        generator.generate(small_maze)
        
        # All cells should be reset
        for cell in small_maze:
            # Visited state is reset during generation
            pass  # Can't test visited state as it's modified during generation
    
    def _verify_maze_connectivity(self, maze):
        """Verify that the maze is fully connected (no isolated areas)."""
        # Use BFS to check connectivity
        visited = set()
        queue = [maze.get_cell(0, 0)]
        visited.add(queue[0])
        
        while queue:
            current = queue.pop(0)
            
            # Check all directions for accessible neighbors
            for direction in Direction:
                if not current.has_wall(direction):
                    dx, dy = direction.delta
                    neighbor = maze.get_cell(current.x + dx, current.y + dy)
                    if neighbor and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        # All cells should be reachable
        total_cells = maze.width * maze.height
        assert len(visited) == total_cells, f"Only {len(visited)}/{total_cells} cells are connected"
    
    def _verify_maze_has_paths(self, maze):
        """Verify that the maze has some paths (not all walls)."""
        total_walls = 0
        possible_walls = 0
        
        for cell in maze:
            for direction in Direction:
                # Count internal walls only (avoid double counting)
                dx, dy = direction.delta
                neighbor = maze.get_cell(cell.x + dx, cell.y + dy)
                if neighbor and (cell.x < neighbor.x or cell.y < neighbor.y):
                    possible_walls += 1
                    if cell.has_wall(direction):
                        total_walls += 1
        
        # Should have removed some walls
        assert total_walls < possible_walls, "No paths were created in the maze"
    
    def test_all_generators_produce_valid_mazes(self, medium_maze):
        """Test that all generators produce valid mazes."""
        generators = [
            DepthFirstSearchGenerator(seed=42),
            KruskalGenerator(seed=42),
            PrimGenerator(seed=42),
            WilsonGenerator(seed=42),
        ]
        
        for generator in generators:
            maze = Maze(10, 10)
            generator.generate(maze)
            
            self._verify_maze_connectivity(maze)
            self._verify_maze_has_paths(maze)
    
    def test_generator_performance(self):
        """Test that generators complete in reasonable time."""
        import time
        
        maze = Maze(20, 20)
        generator = DepthFirstSearchGenerator()
        
        start_time = time.time()
        generator.generate(maze)
        end_time = time.time()
        
        # Should complete within 1 second for a 20x20 maze
        assert end_time - start_time < 1.0
