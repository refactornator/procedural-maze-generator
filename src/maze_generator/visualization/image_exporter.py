"""Image export utilities for maze visualization."""

from typing import Optional, Tuple, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import os

from ..maze import Maze, Cell, Direction


class ImageExporter:
    """Export mazes to various image formats."""

    def __init__(self, cell_size: int = 20, wall_width: int = 2):
        """Initialize the image exporter."""
        self.cell_size = cell_size
        self.wall_width = wall_width
        
        # Color definitions (RGB tuples)
        self.colors = {
            'background': (255, 255, 255),  # White
            'wall': (0, 0, 0),              # Black
            'path': (255, 255, 255),        # White
            'start': (0, 255, 0),           # Green
            'end': (255, 0, 0),             # Red
            'solution': (0, 0, 255),        # Blue
            'visited': (255, 255, 0),       # Yellow
            'border': (128, 128, 128),      # Gray
        }

    def export_png(self, maze: Maze, filename: str, show_solution: bool = False,
                   show_visited: bool = False, add_border: bool = True,
                   title: Optional[str] = None) -> None:
        """Export maze as PNG image."""
        image = self._create_image(maze, show_solution, show_visited, 
                                 add_border, title)
        image.save(filename, 'PNG')

    def export_jpg(self, maze: Maze, filename: str, show_solution: bool = False,
                   show_visited: bool = False, add_border: bool = True,
                   title: Optional[str] = None, quality: int = 95) -> None:
        """Export maze as JPEG image."""
        image = self._create_image(maze, show_solution, show_visited, 
                                 add_border, title)
        # Convert to RGB if necessary (JPEG doesn't support transparency)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(filename, 'JPEG', quality=quality)

    def export_svg(self, maze: Maze, filename: str, show_solution: bool = False,
                   show_visited: bool = False, add_border: bool = True,
                   title: Optional[str] = None) -> None:
        """Export maze as SVG vector image."""
        width = maze.width * self.cell_size
        height = maze.height * self.cell_size
        
        if add_border:
            width += 2 * self.wall_width
            height += 2 * self.wall_width
        
        # Title space
        title_height = 30 if title else 0
        total_height = height + title_height
        
        svg_content = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{width}" height="{total_height}" '
            f'xmlns="http://www.w3.org/2000/svg">',
        ]
        
        # Background
        svg_content.append(
            f'<rect width="{width}" height="{total_height}" '
            f'fill="rgb{self.colors["background"]}" />'
        )
        
        # Title
        if title:
            svg_content.append(
                f'<text x="{width//2}" y="20" text-anchor="middle" '
                f'font-family="Arial" font-size="16" font-weight="bold">{title}</text>'
            )
        
        y_offset = title_height
        
        # Draw cells
        for cell in maze:
            self._add_cell_to_svg(svg_content, cell, maze, show_visited, y_offset)
        
        # Draw solution path
        if show_solution and maze.solution_path:
            self._add_solution_to_svg(svg_content, maze.solution_path, y_offset)
        
        # Draw walls
        for cell in maze:
            self._add_walls_to_svg(svg_content, cell, y_offset)
        
        svg_content.append('</svg>')
        
        with open(filename, 'w') as f:
            f.write('\n'.join(svg_content))

    def _create_image(self, maze: Maze, show_solution: bool = False,
                     show_visited: bool = False, add_border: bool = True,
                     title: Optional[str] = None) -> Image.Image:
        """Create a PIL Image of the maze."""
        # Calculate image dimensions
        width = maze.width * self.cell_size
        height = maze.height * self.cell_size
        
        if add_border:
            width += 2 * self.wall_width
            height += 2 * self.wall_width
        
        # Title space
        title_height = 30 if title else 0
        total_height = height + title_height
        
        # Create image
        image = Image.new('RGB', (width, total_height), self.colors['background'])
        draw = ImageDraw.Draw(image)
        
        # Draw title
        if title:
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except (OSError, IOError):
                font = ImageFont.load_default()
            
            text_bbox = draw.textbbox((0, 0), title, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            draw.text((text_x, 5), title, fill=self.colors['wall'], font=font)
        
        y_offset = title_height
        border_offset = self.wall_width if add_border else 0
        
        # Draw cells
        for cell in maze:
            self._draw_cell_on_image(draw, cell, maze, show_visited, 
                                   y_offset, border_offset)
        
        # Draw solution path
        if show_solution and maze.solution_path:
            self._draw_solution_on_image(draw, maze.solution_path, 
                                       y_offset, border_offset)
        
        # Draw walls
        for cell in maze:
            self._draw_walls_on_image(draw, cell, y_offset, border_offset)
        
        # Draw border
        if add_border:
            border_rect = [0, y_offset, width - 1, height + y_offset - 1]
            draw.rectangle(border_rect, outline=self.colors['border'], 
                         width=self.wall_width)
        
        return image

    def _draw_cell_on_image(self, draw: ImageDraw.ImageDraw, cell: Cell, 
                           maze: Maze, show_visited: bool, y_offset: int,
                           border_offset: int) -> None:
        """Draw a single cell on the image."""
        x = cell.x * self.cell_size + border_offset
        y = cell.y * self.cell_size + y_offset + border_offset
        
        # Determine cell color
        color = self.colors['path']
        if cell.is_start:
            color = self.colors['start']
        elif cell.is_end:
            color = self.colors['end']
        elif show_visited and cell.visited:
            color = self.colors['visited']
        
        # Draw cell rectangle
        draw.rectangle([x, y, x + self.cell_size - 1, y + self.cell_size - 1],
                      fill=color)

    def _draw_walls_on_image(self, draw: ImageDraw.ImageDraw, cell: Cell,
                            y_offset: int, border_offset: int) -> None:
        """Draw walls for a cell on the image."""
        x = cell.x * self.cell_size + border_offset
        y = cell.y * self.cell_size + y_offset + border_offset
        
        # Draw walls based on cell's wall configuration
        if cell.has_wall(Direction.NORTH):
            draw.line([x, y, x + self.cell_size - 1, y], 
                     fill=self.colors['wall'], width=self.wall_width)
        
        if cell.has_wall(Direction.SOUTH):
            draw.line([x, y + self.cell_size - 1, 
                      x + self.cell_size - 1, y + self.cell_size - 1],
                     fill=self.colors['wall'], width=self.wall_width)
        
        if cell.has_wall(Direction.WEST):
            draw.line([x, y, x, y + self.cell_size - 1],
                     fill=self.colors['wall'], width=self.wall_width)
        
        if cell.has_wall(Direction.EAST):
            draw.line([x + self.cell_size - 1, y, 
                      x + self.cell_size - 1, y + self.cell_size - 1],
                     fill=self.colors['wall'], width=self.wall_width)

    def _draw_solution_on_image(self, draw: ImageDraw.ImageDraw, 
                               path: List[Cell], y_offset: int,
                               border_offset: int) -> None:
        """Draw the solution path on the image."""
        if len(path) < 2:
            return
        
        # Create path coordinates
        points = []
        for cell in path:
            center_x = cell.x * self.cell_size + self.cell_size // 2 + border_offset
            center_y = cell.y * self.cell_size + self.cell_size // 2 + y_offset + border_offset
            points.append((center_x, center_y))
        
        # Draw path lines
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], 
                     fill=self.colors['solution'], width=self.wall_width * 2)
        
        # Draw path markers
        for point in points:
            radius = self.cell_size // 4
            draw.ellipse([point[0] - radius, point[1] - radius,
                         point[0] + radius, point[1] + radius],
                        fill=self.colors['solution'])

    def _add_cell_to_svg(self, svg_content: List[str], cell: Cell, maze: Maze,
                        show_visited: bool, y_offset: int) -> None:
        """Add a cell to SVG content."""
        x = cell.x * self.cell_size
        y = cell.y * self.cell_size + y_offset
        
        # Determine cell color
        color = self.colors['path']
        if cell.is_start:
            color = self.colors['start']
        elif cell.is_end:
            color = self.colors['end']
        elif show_visited and cell.visited:
            color = self.colors['visited']
        
        svg_content.append(
            f'<rect x="{x}" y="{y}" width="{self.cell_size}" '
            f'height="{self.cell_size}" fill="rgb{color}" />'
        )

    def _add_walls_to_svg(self, svg_content: List[str], cell: Cell, 
                         y_offset: int) -> None:
        """Add walls to SVG content."""
        x = cell.x * self.cell_size
        y = cell.y * self.cell_size + y_offset
        
        if cell.has_wall(Direction.NORTH):
            svg_content.append(
                f'<line x1="{x}" y1="{y}" x2="{x + self.cell_size}" y2="{y}" '
                f'stroke="rgb{self.colors["wall"]}" stroke-width="{self.wall_width}" />'
            )
        
        if cell.has_wall(Direction.SOUTH):
            svg_content.append(
                f'<line x1="{x}" y1="{y + self.cell_size}" '
                f'x2="{x + self.cell_size}" y2="{y + self.cell_size}" '
                f'stroke="rgb{self.colors["wall"]}" stroke-width="{self.wall_width}" />'
            )
        
        if cell.has_wall(Direction.WEST):
            svg_content.append(
                f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + self.cell_size}" '
                f'stroke="rgb{self.colors["wall"]}" stroke-width="{self.wall_width}" />'
            )
        
        if cell.has_wall(Direction.EAST):
            svg_content.append(
                f'<line x1="{x + self.cell_size}" y1="{y}" '
                f'x2="{x + self.cell_size}" y2="{y + self.cell_size}" '
                f'stroke="rgb{self.colors["wall"]}" stroke-width="{self.wall_width}" />'
            )

    def _add_solution_to_svg(self, svg_content: List[str], path: List[Cell],
                            y_offset: int) -> None:
        """Add solution path to SVG content."""
        if len(path) < 2:
            return
        
        # Create path string
        path_data = []
        for i, cell in enumerate(path):
            center_x = cell.x * self.cell_size + self.cell_size // 2
            center_y = cell.y * self.cell_size + self.cell_size // 2 + y_offset
            
            if i == 0:
                path_data.append(f'M {center_x} {center_y}')
            else:
                path_data.append(f'L {center_x} {center_y}')
        
        svg_content.append(
            f'<path d="{" ".join(path_data)}" stroke="rgb{self.colors["solution"]}" '
            f'stroke-width="{self.wall_width * 2}" fill="none" />'
        )
