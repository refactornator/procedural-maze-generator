#!/usr/bin/env python3
"""
Generate sample outputs for the procedural maze generator demo.

This script creates various sample mazes and outputs to showcase
the capabilities of the maze generator.
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
from maze_generator.algorithms.solvers import (
    AStarSolver,
    BreadthFirstSearchSolver,
    DijkstraSolver,
)
from maze_generator.visualization import AsciiRenderer

# Optional imports for visualization
try:
    from maze_generator.visualization import ImageExporter, MatplotlibRenderer
    HAS_VISUALIZATION = True
except ImportError as e:
    print(f"Warning: Some visualization features unavailable: {e}")
    ImageExporter = None
    MatplotlibRenderer = None
    HAS_VISUALIZATION = False
from maze_generator.utils import OutputManager


def create_sample_directory():
    """Create the sample output directory."""
    samples_dir = Path("demo/samples")
    samples_dir.mkdir(parents=True, exist_ok=True)
    return samples_dir


def generate_ascii_samples(samples_dir: Path):
    """Generate ASCII art maze samples."""
    print("Generating ASCII samples...")
    
    ascii_dir = samples_dir / "ascii"
    ascii_dir.mkdir(exist_ok=True)
    
    renderer = AsciiRenderer()
    
    # Small maze for README
    maze = Maze(12, 8)
    maze.set_start(0, 0)
    maze.set_end(11, 7)
    
    generator = DepthFirstSearchGenerator(seed=42)
    generator.generate(maze)
    
    solver = AStarSolver()
    solution = solver.solve(maze)
    
    # Save different versions
    renderer.save_to_file(maze, str(ascii_dir / "small_maze.txt"), 
                         show_solution=False, title="Small DFS Maze")
    renderer.save_to_file(maze, str(ascii_dir / "small_maze_solved.txt"), 
                         show_solution=True, title="Small DFS Maze - Solved")
    
    # Medium maze
    maze = Maze(20, 15)
    maze.set_start(0, 0)
    maze.set_end(19, 14)
    
    generator = KruskalGenerator(seed=123)
    generator.generate(maze)
    
    solver.solve(maze)
    renderer.save_to_file(maze, str(ascii_dir / "medium_maze.txt"), 
                         show_solution=True, title="Medium Kruskal Maze")
    
    # Compact format
    compact_content = renderer.render_compact(maze, show_solution=True)
    with open(ascii_dir / "compact_maze.txt", 'w') as f:
        f.write("Compact Format Example\n")
        f.write("=" * 30 + "\n\n")
        f.write(compact_content)
    
    print(f"✓ ASCII samples saved to {ascii_dir}")


def generate_image_samples(samples_dir: Path):
    """Generate image samples."""
    print("Generating image samples...")

    if not HAS_VISUALIZATION or ImageExporter is None:
        print("Skipping image samples - ImageExporter not available")
        return

    images_dir = samples_dir / "images"
    images_dir.mkdir(exist_ok=True)

    exporter = ImageExporter(cell_size=25, wall_width=2)
    
    algorithms = [
        ("dfs", DepthFirstSearchGenerator, 42),
        ("kruskal", KruskalGenerator, 123),
        ("prim", PrimGenerator, 456),
    ]
    
    for algo_name, generator_class, seed in algorithms:
        # Create maze
        maze = Maze(16, 12)
        maze.set_start(0, 0)
        maze.set_end(15, 11)
        
        generator = generator_class(seed=seed)
        generator.generate(maze)
        
        # Solve maze
        solver = AStarSolver()
        solution = solver.solve(maze)
        
        # Export different formats
        title = f"{algo_name.upper()} Algorithm Maze"
        
        # PNG without solution
        exporter.export_png(maze, str(images_dir / f"{algo_name}_maze.png"), 
                           show_solution=False, title=title)
        
        # PNG with solution
        exporter.export_png(maze, str(images_dir / f"{algo_name}_maze_solved.png"), 
                           show_solution=True, title=f"{title} - Solved")
        
        # SVG version
        exporter.export_svg(maze, str(images_dir / f"{algo_name}_maze.svg"), 
                           show_solution=True, title=title)
    
    # Large maze example
    large_maze = Maze(30, 25)
    large_maze.set_start(0, 0)
    large_maze.set_end(29, 24)
    
    generator = DepthFirstSearchGenerator(seed=789)
    generator.generate(large_maze)
    
    solver = AStarSolver()
    solver.solve(large_maze)
    
    exporter_large = ImageExporter(cell_size=15, wall_width=1)
    exporter_large.export_png(large_maze, str(images_dir / "large_maze.png"), 
                             show_solution=True, title="Large DFS Maze (30x25)")
    
    print(f"✓ Image samples saved to {images_dir}")


def generate_directory_structure_example(samples_dir: Path):
    """Generate example directory structure."""
    print("Generating directory structure example...")
    
    structure_dir = samples_dir / "directory_structure"
    
    # Use OutputManager to create structure
    manager = OutputManager(structure_dir)
    manager.initialize_output_structure()
    
    # Create some example files in each directory
    example_files = {
        "images": ["dfs_maze_001.png", "kruskal_maze_002.png", "prim_maze_003.png"],
        "ascii": ["maze_20241226_143022.txt", "solution_output.txt"],
        "svg": ["vector_maze.svg", "large_maze_diagram.svg"],
        "benchmarks": ["performance_results.txt", "algorithm_comparison.csv"],
        "temp": ["temp_file_1.tmp", "processing_cache.tmp"]
    }
    
    for subdir, files in example_files.items():
        subdir_path = structure_dir / subdir
        for filename in files:
            (subdir_path / filename).touch()
    
    # Create algorithm subdirectories
    algo_dir = structure_dir / "images"
    for algo in ["dfs", "kruskal", "prim"]:
        algo_subdir = algo_dir / algo
        algo_subdir.mkdir(exist_ok=True)
        (algo_subdir / f"{algo}_example.png").touch()
    
    # Create date subdirectories
    date_dir = structure_dir / "ascii" / "2024-12-26"
    date_dir.mkdir(parents=True, exist_ok=True)
    (date_dir / "daily_maze.txt").touch()
    
    # Generate directory tree
    tree_output = []
    
    def generate_tree(path: Path, prefix: str = "", is_last: bool = True):
        if path.is_dir():
            tree_output.append(f"{prefix}{'└── ' if is_last else '├── '}{path.name}/")
            children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            for i, child in enumerate(children):
                child_is_last = i == len(children) - 1
                child_prefix = prefix + ("    " if is_last else "│   ")
                generate_tree(child, child_prefix, child_is_last)
        else:
            tree_output.append(f"{prefix}{'└── ' if is_last else '├── '}{path.name}")
    
    generate_tree(structure_dir)
    
    # Save tree to file
    with open(samples_dir / "directory_tree.txt", 'w') as f:
        f.write("Output Directory Structure Example\n")
        f.write("=" * 40 + "\n\n")
        f.write("\n".join(tree_output))
    
    print(f"✓ Directory structure example saved to {structure_dir}")


def generate_algorithm_comparison(samples_dir: Path):
    """Generate algorithm comparison samples."""
    print("Generating algorithm comparison...")
    
    comparison_dir = samples_dir / "algorithm_comparison"
    comparison_dir.mkdir(exist_ok=True)
    
    # Same maze generated with different algorithms
    algorithms = [
        ("DFS", DepthFirstSearchGenerator),
        ("Kruskal", KruskalGenerator),
        ("Prim", PrimGenerator),
    ]
    
    renderer = AsciiRenderer()
    exporter = ImageExporter(cell_size=20, wall_width=2)
    
    comparison_content = []
    comparison_content.append("Algorithm Comparison - Same Seed (42)")
    comparison_content.append("=" * 50)
    comparison_content.append("")
    
    for algo_name, generator_class in algorithms:
        maze = Maze(15, 10)
        maze.set_start(0, 0)
        maze.set_end(14, 9)
        
        generator = generator_class(seed=42)
        generator.generate(maze)
        
        # ASCII version
        ascii_maze = renderer.render_compact(maze)
        comparison_content.append(f"{algo_name} Algorithm:")
        comparison_content.append("-" * 20)
        comparison_content.append(ascii_maze)
        comparison_content.append("")
        
        # Image version
        exporter.export_png(maze, str(comparison_dir / f"{algo_name.lower()}_comparison.png"), 
                           title=f"{algo_name} Algorithm (seed=42)")
    
    # Save comparison file
    with open(comparison_dir / "algorithm_comparison.txt", 'w') as f:
        f.write("\n".join(comparison_content))
    
    print(f"✓ Algorithm comparison saved to {comparison_dir}")


def generate_solver_comparison(samples_dir: Path):
    """Generate solver comparison samples."""
    print("Generating solver comparison...")
    
    solver_dir = samples_dir / "solver_comparison"
    solver_dir.mkdir(exist_ok=True)
    
    # Create a maze to solve
    maze = Maze(12, 8)
    maze.set_start(0, 0)
    maze.set_end(11, 7)
    
    generator = DepthFirstSearchGenerator(seed=42)
    generator.generate(maze)
    
    solvers = [
        ("A*", AStarSolver),
        ("Dijkstra", DijkstraSolver),
        ("BFS", BreadthFirstSearchSolver),
    ]
    
    renderer = AsciiRenderer()
    exporter = ImageExporter(cell_size=25, wall_width=2)
    
    comparison_content = []
    comparison_content.append("Solver Algorithm Comparison")
    comparison_content.append("=" * 35)
    comparison_content.append("")
    comparison_content.append("Same maze solved with different algorithms:")
    comparison_content.append("")
    
    for solver_name, solver_class in solvers:
        # Create fresh maze copy for each solver
        test_maze = Maze(12, 8)
        test_maze.set_start(0, 0)
        test_maze.set_end(11, 7)
        
        generator = DepthFirstSearchGenerator(seed=42)
        generator.generate(test_maze)
        
        solver = solver_class()
        solution = solver.solve(test_maze)
        
        # ASCII version
        ascii_solution = renderer.render_compact(test_maze, show_solution=True)
        comparison_content.append(f"{solver_name} Solution (length: {len(solution)}):")
        comparison_content.append("-" * 30)
        comparison_content.append(ascii_solution)
        comparison_content.append("")
        
        # Image version
        exporter.export_png(test_maze, str(solver_dir / f"{solver_name.lower()}_solution.png"), 
                           show_solution=True, title=f"{solver_name} Solution")
    
    # Save comparison file
    with open(solver_dir / "solver_comparison.txt", 'w') as f:
        f.write("\n".join(comparison_content))
    
    print(f"✓ Solver comparison saved to {solver_dir}")


def generate_readme_examples():
    """Generate specific examples for README."""
    print("Generating README examples...")
    
    readme_dir = Path("demo/readme_examples")
    readme_dir.mkdir(parents=True, exist_ok=True)
    
    # Small maze for README header
    maze = Maze(16, 10)
    maze.set_start(0, 0)
    maze.set_end(15, 9)
    
    generator = DepthFirstSearchGenerator(seed=42)
    generator.generate(maze)
    
    solver = AStarSolver()
    solution = solver.solve(maze)
    
    # ASCII for README
    renderer = AsciiRenderer()
    ascii_content = renderer.render_compact(maze, show_solution=True)
    
    with open(readme_dir / "readme_maze.txt", 'w') as f:
        f.write(ascii_content)
    
    # Image for README
    exporter = ImageExporter(cell_size=30, wall_width=3)
    exporter.export_png(maze, str(readme_dir / "readme_maze.png"), 
                       show_solution=True, title="Procedural Maze Generator")
    
    print(f"✓ README examples saved to {readme_dir}")


def main():
    """Generate all sample outputs."""
    print("🎯 Generating Sample Outputs for Procedural Maze Generator")
    print("=" * 60)
    
    try:
        samples_dir = create_sample_directory()
        
        generate_ascii_samples(samples_dir)
        generate_image_samples(samples_dir)
        generate_directory_structure_example(samples_dir)
        generate_algorithm_comparison(samples_dir)
        generate_solver_comparison(samples_dir)
        generate_readme_examples()
        
        print("\n" + "=" * 60)
        print("✅ All sample outputs generated successfully!")
        print(f"📁 Samples are available in: {samples_dir.absolute()}")
        print("\nGenerated samples include:")
        print("• ASCII art mazes in various sizes")
        print("• PNG and SVG image outputs")
        print("• Algorithm comparison examples")
        print("• Solver comparison demonstrations")
        print("• Directory structure examples")
        print("• README-ready examples")
        
    except Exception as e:
        print(f"❌ Error generating samples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
