"""ASCII-based maze visualization for terminal output."""

from typing import List, Optional
from ..maze import Maze, Cell, Direction


class AsciiRenderer:
    """Render mazes as ASCII art for terminal display."""

    def __init__(self, wall_char: str = '█', path_char: str = ' ', 
                 start_char: str = 'S', end_char: str = 'E', 
                 solution_char: str = '·'):
        """Initialize the ASCII renderer with character mappings."""
        self.wall_char = wall_char
        self.path_char = path_char
        self.start_char = start_char
        self.end_char = end_char
        self.solution_char = solution_char

    def render(self, maze: Maze, show_solution: bool = False) -> str:
        """Render the maze as ASCII art."""
        # Calculate dimensions for ASCII representation
        # Each cell is represented by a 3x3 block in the ASCII grid
        ascii_width = maze.width * 2 + 1
        ascii_height = maze.height * 2 + 1
        
        # Initialize ASCII grid with walls
        grid = [[self.wall_char for _ in range(ascii_width)] 
                for _ in range(ascii_height)]
        
        # Fill in the paths
        for cell in maze:
            # Cell position in ASCII grid
            ascii_x = cell.x * 2 + 1
            ascii_y = cell.y * 2 + 1
            
            # Determine cell character
            char = self.path_char
            if cell.is_start:
                char = self.start_char
            elif cell.is_end:
                char = self.end_char
            elif show_solution and cell in maze.solution_path:
                char = self.solution_char
            
            grid[ascii_y][ascii_x] = char
            
            # Remove walls for accessible directions
            for direction in Direction:
                if not cell.has_wall(direction):
                    dx, dy = direction.delta
                    wall_x = ascii_x + dx
                    wall_y = ascii_y + dy
                    
                    if 0 <= wall_x < ascii_width and 0 <= wall_y < ascii_height:
                        wall_char = self.path_char
                        if show_solution and cell in maze.solution_path:
                            # Check if the neighbor is also in solution path
                            neighbor = maze.get_cell(cell.x + dx, cell.y + dy)
                            if neighbor and neighbor in maze.solution_path:
                                wall_char = self.solution_char
                        grid[wall_y][wall_x] = wall_char
        
        # Convert grid to string
        return '\n'.join(''.join(row) for row in grid)

    def render_with_border(self, maze: Maze, show_solution: bool = False, 
                          title: Optional[str] = None) -> str:
        """Render the maze with a decorative border and optional title."""
        maze_str = self.render(maze, show_solution)
        lines = maze_str.split('\n')
        
        # Calculate border width
        max_width = max(len(line) for line in lines)
        border_width = max_width + 4
        
        result = []
        
        # Top border
        result.append('┌' + '─' * (border_width - 2) + '┐')
        
        # Title if provided
        if title:
            title_line = f"│ {title.center(border_width - 4)} │"
            result.append(title_line)
            result.append('├' + '─' * (border_width - 2) + '┤')
        
        # Maze content
        for line in lines:
            padded_line = line.ljust(max_width)
            result.append(f"│ {padded_line} │")
        
        # Bottom border
        result.append('└' + '─' * (border_width - 2) + '┘')
        
        return '\n'.join(result)

    def render_compact(self, maze: Maze, show_solution: bool = False) -> str:
        """Render a more compact version of the maze."""
        lines = []
        
        # Top border
        top_line = '+'
        for x in range(maze.width):
            cell = maze.get_cell(x, 0)
            if cell and cell.has_wall(Direction.NORTH):
                top_line += '-+'
            else:
                top_line += ' +'
        lines.append(top_line)
        
        # Maze rows
        for y in range(maze.height):
            # Cell row
            cell_line = ''
            wall_line = '+'
            
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if not cell:
                    continue
                
                # Left wall
                if cell.has_wall(Direction.WEST):
                    cell_line += '|'
                else:
                    cell_line += ' '
                
                # Cell content
                if cell.is_start:
                    cell_line += self.start_char
                elif cell.is_end:
                    cell_line += self.end_char
                elif show_solution and cell in maze.solution_path:
                    cell_line += self.solution_char
                else:
                    cell_line += self.path_char
                
                # Bottom wall for next row
                if cell.has_wall(Direction.SOUTH):
                    wall_line += '-+'
                else:
                    wall_line += ' +'
            
            # Right border
            cell_line += '|'
            
            lines.append(cell_line)
            if y < maze.height - 1:  # Don't add wall line after last row
                lines.append(wall_line)
        
        # Bottom border
        bottom_line = '+'
        for x in range(maze.width):
            cell = maze.get_cell(x, maze.height - 1)
            if cell and cell.has_wall(Direction.SOUTH):
                bottom_line += '-+'
            else:
                bottom_line += ' +'
        lines.append(bottom_line)
        
        return '\n'.join(lines)

    def print_maze(self, maze: Maze, show_solution: bool = False, 
                   compact: bool = False, title: Optional[str] = None) -> None:
        """Print the maze to the console."""
        if compact:
            print(self.render_compact(maze, show_solution))
        elif title:
            print(self.render_with_border(maze, show_solution, title))
        else:
            print(self.render(maze, show_solution))

    def save_to_file(self, maze: Maze, filename: str, show_solution: bool = False,
                     compact: bool = False, title: Optional[str] = None) -> None:
        """Save the ASCII maze to a text file."""
        if compact:
            content = self.render_compact(maze, show_solution)
        elif title:
            content = self.render_with_border(maze, show_solution, title)
        else:
            content = self.render(maze, show_solution)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
