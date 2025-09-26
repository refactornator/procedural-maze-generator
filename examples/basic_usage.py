#!/usr/bin/env python3
"""
Basic usage example for the Procedural Maze Generator.

This example demonstrates:
- Creating a maze
- Generating it with different algorithms
- Solving it with different algorithms
- Visualizing the results
"""

from maze_generator import Maze
from maze_generator.algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
)
from maze_generator.algorithms.solvers import (
    AStarSolver,
    BreadthFirstSearchSolver,
    DijkstraSolver,
)
from maze_generator.visualization import (
    AsciiRenderer,
    MatplotlibRenderer,
    ImageExporter,
)


def main():
    """Demonstrate basic maze generation and solving."""
    print("Procedural Maze Generator - Basic Usage Example")
    print("=" * 50)
    
    # Create a maze
    width, height = 15, 10
    maze = Maze(width, height)
    
    # Set start and end positions
    maze.set_start(0, 0)
    maze.set_end(width - 1, height - 1)
    
    print(f"Created {width}x{height} maze")
    print(f"Start: ({maze.start.x}, {maze.start.y})")
    print(f"End: ({maze.end.x}, {maze.end.y})")
    print()
    
    # Try different generation algorithms
    generators = {
        "Depth-First Search": DepthFirstSearchGenerator(seed=42),
        "Kruskal's Algorithm": KruskalGenerator(seed=42),
        "Prim's Algorithm": PrimGenerator(seed=42),
    }
    
    for name, generator in generators.items():
        print(f"Generating maze with {name}...")
        
        # Generate the maze
        generator.generate(maze)
        
        # Solve with A*
        solver = AStarSolver()
        solution = solver.solve(maze)
        
        print(f"Solution found with {len(solution)} steps")
        
        # Display ASCII version
        print("\nASCII Representation:")
        renderer = AsciiRenderer()
        print(renderer.render_compact(maze, show_solution=True))
        print()
        
        # Save as image
        exporter = ImageExporter(cell_size=30, wall_width=2)
        filename = f"maze_{name.lower().replace(' ', '_').replace("'", '')}.png"
        exporter.export_png(maze, filename, show_solution=True, 
                           title=f"Maze - {name}")
        print(f"Saved image: {filename}")
        print("-" * 50)


def compare_solvers():
    """Compare different solving algorithms on the same maze."""
    print("\nSolver Comparison")
    print("=" * 30)
    
    # Create and generate a maze
    maze = Maze(12, 8)
    maze.set_start(0, 0)
    maze.set_end(11, 7)
    
    generator = DepthFirstSearchGenerator(seed=123)
    generator.generate(maze)
    
    # Try different solvers
    solvers = {
        "A* Algorithm": AStarSolver(),
        "Dijkstra's Algorithm": DijkstraSolver(),
        "Breadth-First Search": BreadthFirstSearchSolver(),
    }
    
    for name, solver in solvers.items():
        solution = solver.solve(maze)
        print(f"{name:20} | Solution length: {len(solution):2d} steps")
    
    print()


def visualization_examples():
    """Demonstrate different visualization options."""
    print("Visualization Examples")
    print("=" * 30)
    
    # Create a small maze for demonstration
    maze = Maze(8, 6)
    maze.set_start(0, 0)
    maze.set_end(7, 5)
    
    generator = PrimGenerator(seed=456)
    generator.generate(maze)
    
    solver = AStarSolver()
    solution = solver.solve(maze)
    
    print("1. ASCII Visualization:")
    ascii_renderer = AsciiRenderer()
    ascii_renderer.print_maze(maze, show_solution=True, 
                             title="Sample Maze with Solution")
    
    print("\n2. Compact ASCII:")
    print(ascii_renderer.render_compact(maze, show_solution=True))
    
    print("\n3. Exporting to different formats...")
    
    # Export to different image formats
    exporter = ImageExporter(cell_size=25, wall_width=2)
    
    formats = [
        ("PNG", "sample_maze.png", exporter.export_png),
        ("JPEG", "sample_maze.jpg", exporter.export_jpg),
        ("SVG", "sample_maze.svg", exporter.export_svg),
    ]
    
    for format_name, filename, export_func in formats:
        export_func(maze, filename, show_solution=True, 
                   title=f"Sample Maze ({format_name})")
        print(f"   Exported {format_name}: {filename}")
    
    # Save ASCII to file
    ascii_renderer.save_to_file(maze, "sample_maze.txt", 
                               show_solution=True, 
                               title="Sample Maze (ASCII)")
    print("   Exported ASCII: sample_maze.txt")


if __name__ == "__main__":
    main()
    compare_solvers()
    visualization_examples()
    
    print("\nExample completed! Check the generated files:")
    print("- maze_*.png (generated maze images)")
    print("- sample_maze.* (visualization examples)")
    print("\nTry running with matplotlib visualization:")
    print("python -c \"from examples.basic_usage import *; ")
    print("from maze_generator.visualization import MatplotlibRenderer; ")
    print("maze = Maze(10, 10); ")
    print("DepthFirstSearchGenerator().generate(maze); ")
    print("maze.set_start(0, 0); maze.set_end(9, 9); ")
    print("AStarSolver().solve(maze); ")
    print("MatplotlibRenderer().show(maze, show_solution=True)\"")
