#!/usr/bin/env python3
"""
Create placeholder images for the gallery when full dependencies aren't available.

This script creates simple placeholder images that show the maze structure
using basic text rendering, ensuring the gallery always has visual content.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from maze_generator import Maze
from maze_generator.algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
)
from maze_generator.algorithms.solvers import AStarSolver
from maze_generator.visualization import AsciiRenderer


def create_text_image(text: str, output_path: Path, width: int = 400, height: int = 300):
    """Create a properly proportioned SVG with ASCII art."""
    try:
        lines = text.split('\n')
        # Filter out empty lines and title lines
        maze_lines = [line for line in lines if line.strip() and not line.startswith('┌') and not line.startswith('│') and not line.startswith('├') and not line.startswith('└')]

        if not maze_lines:
            maze_lines = lines  # Fallback to all lines

        # Calculate proper dimensions based on content
        max_line_length = max(len(line) for line in maze_lines) if maze_lines else 50
        font_size = max(8, min(16, 400 // max_line_length))  # Responsive font size
        char_width = font_size * 0.6  # Monospace character width approximation
        line_height = font_size * 1.2

        # Calculate tight-fitting dimensions
        content_width = max_line_length * char_width + 20  # 10px padding each side
        content_height = len(maze_lines) * line_height + 40  # 20px padding top/bottom

        # Use calculated dimensions or provided ones, whichever is smaller
        svg_width = min(width, int(content_width))
        svg_height = min(height, int(content_height))

        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f8f9fa"/>
  <text x="10" y="{font_size + 10}" font-family="monospace" font-size="{font_size}" fill="#2c3e50">'''

        for i, line in enumerate(maze_lines[:30]):  # Limit to 30 lines
            # Escape XML characters
            escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            y_pos = (i + 1) * line_height + 10
            svg_content += f'\n    <tspan x="10" y="{y_pos}">{escaped_line}</tspan>'

        svg_content += '''
  </text>
</svg>'''

        # Save as SVG
        svg_path = output_path.with_suffix('.svg')
        with open(svg_path, 'w') as f:
            f.write(svg_content)

        return svg_path

    except Exception as e:
        print(f"Warning: Could not create image for {output_path}: {e}")
        return None


def create_placeholder_gallery():
    """Create placeholder images for the gallery."""
    print("🖼️  Creating Placeholder Gallery Images")
    print("=" * 45)
    
    gallery_dir = Path("docs/gallery")
    gallery_dir.mkdir(parents=True, exist_ok=True)
    
    # Create algorithm examples
    algorithms = [
        ("dfs", "Depth-First Search", DepthFirstSearchGenerator),
        ("kruskal", "Kruskal's Algorithm", KruskalGenerator),
        ("prim", "Prim's Algorithm", PrimGenerator),
    ]
    
    for algo_name, display_name, generator_class in algorithms:
        print(f"  Creating {display_name} placeholder...")
        
        # Generate maze
        maze = Maze(12, 8)
        generator = generator_class(seed=42)
        generator.generate(maze)
        
        # Create ASCII representation
        ascii_renderer = AsciiRenderer()
        ascii_output = ascii_renderer.render_with_border(maze, title=f"{display_name} Maze")
        
        # Create placeholder image
        image_path = gallery_dir / "algorithms" / f"{algo_name}_maze_example.png"
        image_path.parent.mkdir(exist_ok=True)
        
        created_path = create_text_image(ascii_output, image_path)
        if created_path:
            print(f"    ✅ Created: {created_path.relative_to(gallery_dir)}")
    
    # Create solution example
    print("  Creating solution placeholder...")
    maze = Maze(10, 8)
    maze.set_start(0, 0)
    maze.set_end(9, 7)
    
    generator = DepthFirstSearchGenerator(seed=123)
    generator.generate(maze)
    
    solver = AStarSolver()
    solution = solver.solve(maze)
    
    if solution:
        ascii_output = ascii_renderer.render_with_border(
            maze, show_solution=True, 
            title=f"A* Solution ({len(solution)} steps)"
        )
        
        image_path = gallery_dir / "solutions" / "astar_solution_example.png"
        image_path.parent.mkdir(exist_ok=True)
        
        created_path = create_text_image(ascii_output, image_path)
        if created_path:
            print(f"    ✅ Created: {created_path.relative_to(gallery_dir)}")
    
    # Create README example
    print("  Creating README placeholder...")
    maze = Maze(8, 6)
    maze.set_start(0, 0)
    maze.set_end(7, 5)
    
    generator = DepthFirstSearchGenerator(seed=42)
    generator.generate(maze)
    
    solver = AStarSolver()
    solver.solve(maze)
    
    ascii_output = ascii_renderer.render_compact(maze, show_solution=True)
    
    image_path = gallery_dir / "readme" / "readme_example.png"
    image_path.parent.mkdir(exist_ok=True)
    
    created_path = create_text_image(ascii_output, image_path, width=500, height=350)
    if created_path:
        print(f"    ✅ Created: {created_path.relative_to(gallery_dir)}")
    
    print("\n✅ Placeholder gallery created!")
    print("💡 These SVG placeholders will be replaced with high-quality PNG images")
    print("   when the full dependencies (matplotlib, PIL) are available.")


def main():
    """Create placeholder gallery."""
    try:
        create_placeholder_gallery()
        return 0
    except Exception as e:
        print(f"❌ Error creating placeholder gallery: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
