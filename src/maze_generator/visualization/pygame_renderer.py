"""Pygame-based interactive maze visualization."""

from typing import Optional, Tuple, List, Callable
import pygame
import sys
from enum import Enum

from ..maze import Maze, Cell, Direction


class RenderMode(Enum):
    """Different rendering modes for the pygame renderer."""
    NORMAL = "normal"
    GENERATION = "generation"
    SOLVING = "solving"


class PygameRenderer:
    """Interactive maze renderer using pygame."""

    def __init__(self, cell_size: int = 20, wall_width: int = 2):
        """Initialize the pygame renderer."""
        pygame.init()
        
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = False
        
        # Color definitions
        self.colors = {
            'background': (255, 255, 255),  # White
            'wall': (0, 0, 0),              # Black
            'path': (255, 255, 255),        # White
            'start': (0, 255, 0),           # Green
            'end': (255, 0, 0),             # Red
            'solution': (0, 0, 255),        # Blue
            'visited': (255, 255, 0),       # Yellow
            'current': (255, 165, 0),       # Orange
            'frontier': (128, 0, 128),      # Purple
        }

    def initialize_display(self, maze: Maze, title: str = "Maze Visualization") -> None:
        """Initialize the pygame display window."""
        width = maze.width * self.cell_size + self.wall_width
        height = maze.height * self.cell_size + self.wall_width
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.running = True

    def render_maze(self, maze: Maze, show_solution: bool = False, 
                   show_visited: bool = False, current_cell: Optional[Cell] = None,
                   frontier_cells: Optional[List[Cell]] = None) -> None:
        """Render the maze on the pygame surface."""
        if not self.screen:
            return
        
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Draw cells
        for cell in maze:
            self._draw_cell(cell, maze, show_visited, current_cell, frontier_cells)
        
        # Draw solution path if requested
        if show_solution and maze.solution_path:
            self._draw_solution_path(maze.solution_path)
        
        # Draw walls
        for cell in maze:
            self._draw_walls(cell)
        
        pygame.display.flip()

    def _draw_cell(self, cell: Cell, maze: Maze, show_visited: bool = False,
                   current_cell: Optional[Cell] = None, 
                   frontier_cells: Optional[List[Cell]] = None) -> None:
        """Draw a single cell."""
        x = cell.x * self.cell_size
        y = cell.y * self.cell_size
        
        # Determine cell color
        color = self.colors['path']
        
        if cell == current_cell:
            color = self.colors['current']
        elif frontier_cells and cell in frontier_cells:
            color = self.colors['frontier']
        elif cell.is_start:
            color = self.colors['start']
        elif cell.is_end:
            color = self.colors['end']
        elif show_visited and cell.visited:
            color = self.colors['visited']
        
        # Draw cell rectangle
        pygame.draw.rect(self.screen, color, 
                        (x, y, self.cell_size, self.cell_size))

    def _draw_walls(self, cell: Cell) -> None:
        """Draw walls for a cell."""
        x = cell.x * self.cell_size
        y = cell.y * self.cell_size
        
        # Draw walls based on cell's wall configuration
        if cell.has_wall(Direction.NORTH):
            pygame.draw.line(self.screen, self.colors['wall'],
                           (x, y), (x + self.cell_size, y), self.wall_width)
        
        if cell.has_wall(Direction.SOUTH):
            pygame.draw.line(self.screen, self.colors['wall'],
                           (x, y + self.cell_size), 
                           (x + self.cell_size, y + self.cell_size), 
                           self.wall_width)
        
        if cell.has_wall(Direction.WEST):
            pygame.draw.line(self.screen, self.colors['wall'],
                           (x, y), (x, y + self.cell_size), self.wall_width)
        
        if cell.has_wall(Direction.EAST):
            pygame.draw.line(self.screen, self.colors['wall'],
                           (x + self.cell_size, y), 
                           (x + self.cell_size, y + self.cell_size), 
                           self.wall_width)

    def _draw_solution_path(self, path: List[Cell]) -> None:
        """Draw the solution path."""
        if len(path) < 2:
            return
        
        # Draw path as connected lines
        points = []
        for cell in path:
            center_x = cell.x * self.cell_size + self.cell_size // 2
            center_y = cell.y * self.cell_size + self.cell_size // 2
            points.append((center_x, center_y))
        
        if len(points) > 1:
            pygame.draw.lines(self.screen, self.colors['solution'], 
                            False, points, self.wall_width * 2)
        
        # Draw path markers
        for point in points:
            pygame.draw.circle(self.screen, self.colors['solution'], 
                             point, self.cell_size // 4)

    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    # Space key can be used to pause/resume animations
                    return True
        return True

    def show_static(self, maze: Maze, show_solution: bool = False,
                   show_visited: bool = False, title: str = "Maze") -> None:
        """Display a static maze until user closes the window."""
        self.initialize_display(maze, title)
        
        while self.running:
            if not self.handle_events():
                break
            
            self.render_maze(maze, show_solution, show_visited)
            self.clock.tick(60)  # 60 FPS
        
        self.cleanup()

    def animate_generation(self, maze: Maze, generator_callback: Callable,
                          delay_ms: int = 50, title: str = "Maze Generation") -> None:
        """Animate the maze generation process."""
        self.initialize_display(maze, title)
        
        # This would need to be integrated with the generation algorithms
        # to provide step-by-step visualization
        while self.running:
            if not self.handle_events():
                break
            
            # Call the generator callback to get the next step
            current_cell, frontier_cells, is_complete = generator_callback()
            
            self.render_maze(maze, current_cell=current_cell, 
                           frontier_cells=frontier_cells)
            
            if is_complete:
                # Show final result for a moment
                pygame.time.wait(1000)
                break
            
            pygame.time.wait(delay_ms)
        
        self.cleanup()

    def animate_solving(self, maze: Maze, solver_callback: Callable,
                       delay_ms: int = 100, title: str = "Maze Solving") -> None:
        """Animate the maze solving process."""
        self.initialize_display(maze, title)
        
        while self.running:
            if not self.handle_events():
                break
            
            # Call the solver callback to get the next step
            current_cell, visited_cells, path, is_complete = solver_callback()
            
            # Update maze state for visualization
            for cell in maze:
                cell.visited = cell in visited_cells
            
            self.render_maze(maze, show_visited=True, current_cell=current_cell)
            
            if is_complete and path:
                maze.solution_path = path
                self.render_maze(maze, show_solution=True, show_visited=True)
                pygame.time.wait(2000)  # Show solution for 2 seconds
                break
            
            pygame.time.wait(delay_ms)
        
        self.cleanup()

    def save_screenshot(self, filename: str) -> None:
        """Save the current display as an image."""
        if self.screen:
            pygame.image.save(self.screen, filename)

    def cleanup(self) -> None:
        """Clean up pygame resources."""
        self.running = False
        pygame.quit()

    def __del__(self):
        """Ensure cleanup on object destruction."""
        if pygame.get_init():
            self.cleanup()
