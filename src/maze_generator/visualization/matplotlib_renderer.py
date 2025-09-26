"""Matplotlib-based maze visualization."""

from typing import Optional, Tuple, List
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import numpy as np

from ..maze import Maze, Cell, Direction


class MatplotlibRenderer:
    """Render mazes using matplotlib."""

    def __init__(self, cell_size: int = 20, wall_width: int = 2):
        """Initialize the renderer with display parameters."""
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.colors = {
            'wall': '#000000',
            'path': '#FFFFFF',
            'start': '#00FF00',
            'end': '#FF0000',
            'solution': '#0000FF',
            'visited': '#FFFF00',
        }

    def render(self, maze: Maze, show_solution: bool = False, 
               show_visited: bool = False, title: str = "Maze") -> plt.Figure:
        """Render the maze and return the matplotlib figure."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        
        # Set up the plot
        ax.set_xlim(0, maze.width * self.cell_size)
        ax.set_ylim(0, maze.height * self.cell_size)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')
        
        # Fill background
        ax.add_patch(patches.Rectangle(
            (0, 0), maze.width * self.cell_size, maze.height * self.cell_size,
            facecolor=self.colors['path'], edgecolor='none'
        ))
        
        # Draw cells
        for cell in maze:
            self._draw_cell(ax, cell, maze, show_visited)
        
        # Draw solution path if requested
        if show_solution and maze.solution_path:
            self._draw_solution_path(ax, maze.solution_path)
        
        # Draw walls
        for cell in maze:
            self._draw_walls(ax, cell)
        
        plt.tight_layout()
        return fig

    def _draw_cell(self, ax: plt.Axes, cell: Cell, maze: Maze, show_visited: bool) -> None:
        """Draw a single cell."""
        x = cell.x * self.cell_size
        y = (maze.height - cell.y - 1) * self.cell_size  # Flip Y coordinate
        
        color = self.colors['path']
        
        # Color special cells
        if cell.is_start:
            color = self.colors['start']
        elif cell.is_end:
            color = self.colors['end']
        elif show_visited and cell.visited:
            color = self.colors['visited']
        
        ax.add_patch(patches.Rectangle(
            (x, y), self.cell_size, self.cell_size,
            facecolor=color, edgecolor='none'
        ))

    def _draw_walls(self, ax: plt.Axes, cell: Cell) -> None:
        """Draw walls for a cell."""
        x = cell.x * self.cell_size
        y = (cell.y) * self.cell_size  # Don't flip for walls
        
        # Draw walls based on cell's wall configuration
        if cell.has_wall(Direction.NORTH):
            ax.plot([x, x + self.cell_size], 
                   [y + self.cell_size, y + self.cell_size],
                   color=self.colors['wall'], linewidth=self.wall_width)
        
        if cell.has_wall(Direction.SOUTH):
            ax.plot([x, x + self.cell_size], [y, y],
                   color=self.colors['wall'], linewidth=self.wall_width)
        
        if cell.has_wall(Direction.WEST):
            ax.plot([x, x], [y, y + self.cell_size],
                   color=self.colors['wall'], linewidth=self.wall_width)
        
        if cell.has_wall(Direction.EAST):
            ax.plot([x + self.cell_size, x + self.cell_size], 
                   [y, y + self.cell_size],
                   color=self.colors['wall'], linewidth=self.wall_width)

    def _draw_solution_path(self, ax: plt.Axes, path: List[Cell]) -> None:
        """Draw the solution path."""
        if len(path) < 2:
            return
        
        # Create path coordinates
        x_coords = []
        y_coords = []
        
        for cell in path:
            x_coords.append(cell.x * self.cell_size + self.cell_size // 2)
            y_coords.append(cell.y * self.cell_size + self.cell_size // 2)
        
        # Draw the path
        ax.plot(x_coords, y_coords, color=self.colors['solution'], 
               linewidth=self.wall_width * 2, alpha=0.8, zorder=10)
        
        # Draw path markers
        ax.scatter(x_coords, y_coords, color=self.colors['solution'], 
                  s=self.cell_size, alpha=0.6, zorder=11)

    def save_image(self, maze: Maze, filename: str, show_solution: bool = False,
                   show_visited: bool = False, dpi: int = 300) -> None:
        """Save the maze as an image file."""
        fig = self.render(maze, show_solution, show_visited)
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig)

    def show(self, maze: Maze, show_solution: bool = False, 
             show_visited: bool = False) -> None:
        """Display the maze in a window."""
        fig = self.render(maze, show_solution, show_visited)
        plt.show()

    def create_animation_frames(self, maze: Maze, generation_steps: List[Maze]) -> List[plt.Figure]:
        """Create animation frames for maze generation process."""
        frames = []
        for i, step_maze in enumerate(generation_steps):
            title = f"Maze Generation - Step {i + 1}/{len(generation_steps)}"
            fig = self.render(step_maze, title=title)
            frames.append(fig)
        return frames
