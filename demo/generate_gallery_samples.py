#!/usr/bin/env python3
"""
Generate permanent sample outputs for the repository gallery.

This script creates high-quality sample outputs that are committed to the
repository for documentation and showcase purposes.
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
    WilsonGenerator,
)
from maze_generator.algorithms.solvers import (
    AStarSolver,
    DijkstraSolver,
    BreadthFirstSearchSolver,
)
from maze_generator.visualization import AsciiRenderer

# Optional imports
try:
    from maze_generator.visualization import ImageExporter
    HAS_IMAGE_EXPORT = True
except ImportError:
    print("Warning: ImageExporter not available - skipping image generation")
    ImageExporter = None
    HAS_IMAGE_EXPORT = False


def create_gallery_structure():
    """Create the gallery directory structure."""
    gallery_dir = Path("docs/gallery")
    gallery_dir.mkdir(parents=True, exist_ok=True)
    
    subdirs = ["algorithms", "solutions", "formats", "comparisons", "animations"]
    for subdir in subdirs:
        (gallery_dir / subdir).mkdir(exist_ok=True)
    
    return gallery_dir


def generate_algorithm_examples(gallery_dir: Path):
    """Generate examples for each algorithm."""
    print("Generating algorithm examples...")
    
    algorithms = [
        ("dfs", "Depth-First Search", DepthFirstSearchGenerator),
        ("kruskal", "Kruskal's Algorithm", KruskalGenerator),
        ("prim", "Prim's Algorithm", PrimGenerator),
        ("wilson", "Wilson's Algorithm", WilsonGenerator),
    ]
    
    # Standard maze size for comparison
    width, height = 15, 12
    seed = 42  # Fixed seed for reproducible examples
    
    for algo_name, display_name, generator_class in algorithms:
        print(f"  Creating {display_name} example...")
        
        # Generate maze
        maze = Maze(width, height)
        generator = generator_class(seed=seed)
        generator.generate(maze)
        
        # ASCII output
        ascii_renderer = AsciiRenderer()
        ascii_output = ascii_renderer.render_with_border(maze, title=f"{display_name} Maze")
        
        ascii_file = gallery_dir / "algorithms" / f"{algo_name}_maze.txt"
        with open(ascii_file, 'w') as f:
            f.write(ascii_output)
        
        # Image output (if available)
        if HAS_IMAGE_EXPORT:
            exporter = ImageExporter(cell_size=25, wall_width=2)
            image_file = gallery_dir / "algorithms" / f"{algo_name}_maze_example.png"
            exporter.export_png(maze, str(image_file), 
                              title=f"{display_name} Maze",
                              add_border=True)


def generate_solution_examples(gallery_dir: Path):
    """Generate examples of different solving algorithms."""
    print("Generating solution examples...")
    
    # Create a maze to solve
    maze = Maze(12, 10)
    maze.set_start(0, 0)
    maze.set_end(11, 9)
    
    generator = DepthFirstSearchGenerator(seed=123)
    generator.generate(maze)
    
    solvers = [
        ("astar", "A* Algorithm", AStarSolver),
        ("dijkstra", "Dijkstra's Algorithm", DijkstraSolver),
        ("bfs", "Breadth-First Search", BreadthFirstSearchSolver),
    ]
    
    for solver_name, display_name, solver_class in solvers:
        print(f"  Creating {display_name} solution...")
        
        # Solve maze
        solver = solver_class()
        solution = solver.solve(maze)
        
        if solution:
            # ASCII output with solution
            ascii_renderer = AsciiRenderer()
            ascii_output = ascii_renderer.render_with_border(
                maze, show_solution=True,
                title=f"{display_name} Solution ({len(solution)} steps)"
            )
            
            ascii_file = gallery_dir / "solutions" / f"{solver_name}_solution.txt"
            with open(ascii_file, 'w') as f:
                f.write(ascii_output)
            
            # Image output (if available)
            if HAS_IMAGE_EXPORT:
                exporter = ImageExporter(cell_size=30, wall_width=2)
                image_file = gallery_dir / "solutions" / f"{solver_name}_solution_example.png"
                exporter.export_png(maze, str(image_file),
                                  show_solution=True,
                                  show_visited=True,
                                  title=f"{display_name} Solution",
                                  add_border=True)


def generate_format_examples(gallery_dir: Path):
    """Generate examples of different output formats."""
    print("Generating format examples...")
    
    # Create a showcase maze
    maze = Maze(10, 8)
    maze.set_start(0, 0)
    maze.set_end(9, 7)
    
    generator = KruskalGenerator(seed=789)
    generator.generate(maze)
    
    # Solve it
    solver = AStarSolver()
    solver.solve(maze)
    
    # ASCII format
    ascii_renderer = AsciiRenderer()
    
    # Compact ASCII
    compact_ascii = ascii_renderer.render_compact(maze, show_solution=True)
    with open(gallery_dir / "formats" / "ascii_compact_example.txt", 'w') as f:
        f.write("# Compact ASCII Format\n\n")
        f.write(compact_ascii)
    
    # Detailed ASCII
    detailed_ascii = ascii_renderer.render_with_border(maze, show_solution=True,
                                                     title="Detailed ASCII Format")
    with open(gallery_dir / "formats" / "ascii_detailed_example.txt", 'w') as f:
        f.write(detailed_ascii)
    
    # Image formats (if available)
    if HAS_IMAGE_EXPORT:
        exporter = ImageExporter(cell_size=35, wall_width=3)
        
        # PNG format
        exporter.export_png(maze, str(gallery_dir / "formats" / "png_maze_example.png"),
                          show_solution=True, title="PNG Format Example", add_border=True)
        
        # SVG format
        exporter.export_svg(maze, str(gallery_dir / "formats" / "svg_maze_example.svg"),
                          show_solution=True, title="SVG Format Example", add_border=True)
        
        # JPEG format
        exporter.export_jpg(maze, str(gallery_dir / "formats" / "jpeg_maze_example.jpg"),
                          show_solution=True, title="JPEG Format Example", add_border=True)


def generate_comparison_examples(gallery_dir: Path):
    """Generate side-by-side algorithm comparisons."""
    print("Generating comparison examples...")
    
    algorithms = [
        ("DFS", DepthFirstSearchGenerator),
        ("Kruskal", KruskalGenerator),
        ("Prim", PrimGenerator),
    ]
    
    # Use same seed for fair comparison
    seed = 456
    width, height = 12, 8
    
    comparison_text = "# Algorithm Comparison\n\n"
    comparison_text += f"All mazes generated with seed {seed} for fair comparison.\n"
    comparison_text += f"Size: {width}x{height}\n\n"
    
    for algo_name, generator_class in algorithms:
        maze = Maze(width, height)
        generator = generator_class(seed=seed)
        generator.generate(maze)
        
        ascii_renderer = AsciiRenderer()
        ascii_output = ascii_renderer.render_compact(maze)
        
        comparison_text += f"## {algo_name} Algorithm\n\n"
        comparison_text += "```\n"
        comparison_text += ascii_output
        comparison_text += "\n```\n\n"
        
        # Individual image (if available)
        if HAS_IMAGE_EXPORT:
            exporter = ImageExporter(cell_size=25, wall_width=2)
            image_file = gallery_dir / "comparisons" / f"comparison_{algo_name.lower()}.png"
            exporter.export_png(maze, str(image_file),
                              title=f"{algo_name} Algorithm",
                              add_border=True)
    
    # Save comparison text
    with open(gallery_dir / "comparisons" / "algorithm_comparison.md", 'w') as f:
        f.write(comparison_text)


def generate_readme_examples(gallery_dir: Path):
    """Generate specific examples for README documentation."""
    print("Generating README examples...")
    
    readme_dir = gallery_dir / "readme"
    readme_dir.mkdir(exist_ok=True)
    
    # Small example for README
    maze = Maze(8, 6)
    maze.set_start(0, 0)
    maze.set_end(7, 5)
    
    generator = DepthFirstSearchGenerator(seed=42)
    generator.generate(maze)
    
    solver = AStarSolver()
    solver.solve(maze)
    
    # ASCII for README
    ascii_renderer = AsciiRenderer()
    readme_ascii = ascii_renderer.render_compact(maze, show_solution=True)
    
    with open(readme_dir / "readme_example.txt", 'w') as f:
        f.write("# README Example Maze\n\n")
        f.write("```\n")
        f.write(readme_ascii)
        f.write("\n```\n")
    
    # Small image for README (if available)
    if HAS_IMAGE_EXPORT:
        exporter = ImageExporter(cell_size=40, wall_width=3)
        exporter.export_png(maze, str(readme_dir / "readme_example.png"),
                          show_solution=True,
                          title="Procedural Maze Generator",
                          add_border=True)


def create_gallery_index(gallery_dir: Path):
    """Create an index file for the gallery."""
    print("Creating gallery index...")
    
    index_content = """# 🎨 Maze Gallery Index

This directory contains visual examples and documentation for the Procedural Maze Generator.

## 📁 Directory Structure

- **`algorithms/`** - Examples of different generation algorithms
- **`solutions/`** - Examples of different solving algorithms  
- **`formats/`** - Examples of different output formats (ASCII, PNG, SVG, JPEG)
- **`comparisons/`** - Side-by-side algorithm comparisons
- **`readme/`** - Examples specifically for README documentation
- **`animations/`** - Animated GIFs (generated separately)

## 🔄 Regenerating Examples

To regenerate all gallery examples:

```bash
python demo/generate_gallery_samples.py
```

## 📊 Statistics

"""
    
    # Count files in each directory
    for subdir in ["algorithms", "solutions", "formats", "comparisons", "readme"]:
        subdir_path = gallery_dir / subdir
        if subdir_path.exists():
            file_count = len(list(subdir_path.glob("*")))
            index_content += f"- **{subdir}/**: {file_count} files\n"
    
    index_content += "\n---\n\n*Gallery generated automatically by the demo system*\n"
    
    with open(gallery_dir / "INDEX.md", 'w') as f:
        f.write(index_content)


def main():
    """Generate all gallery samples."""
    print("🎨 Generating Gallery Samples")
    print("=" * 40)
    
    # Create directory structure
    gallery_dir = create_gallery_structure()
    print(f"Gallery directory: {gallery_dir.absolute()}")
    
    try:
        # Generate all examples
        generate_algorithm_examples(gallery_dir)
        generate_solution_examples(gallery_dir)
        generate_format_examples(gallery_dir)
        generate_comparison_examples(gallery_dir)
        generate_readme_examples(gallery_dir)
        
        # Create index
        create_gallery_index(gallery_dir)
        
        print("\n" + "=" * 40)
        print("✅ Gallery generation complete!")
        print(f"📁 Gallery location: {gallery_dir.absolute()}")
        
        # List generated files
        print("\n📋 Generated files:")
        for file_path in sorted(gallery_dir.rglob("*")):
            if file_path.is_file():
                rel_path = file_path.relative_to(gallery_dir)
                print(f"  📄 {rel_path}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error generating gallery: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
