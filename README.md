# Procedural Maze Generator

A comprehensive Python library for generating and solving mazes using various algorithms, with multiple visualization options and export formats.

## Features

### 🎯 **Maze Generation Algorithms**
- **Depth-First Search (DFS)** - Classic recursive backtracking
- **Kruskal's Algorithm** - Minimum spanning tree approach
- **Prim's Algorithm** - Growing tree method
- **Wilson's Algorithm** - Loop-erased random walk

### 🧭 **Maze Solving Algorithms**
- **A\*** - Optimal pathfinding with heuristics
- **Dijkstra's Algorithm** - Guaranteed shortest path
- **Breadth-First Search (BFS)** - Level-by-level exploration
- **Depth-First Search (DFS)** - Deep exploration
- **Wall Follower** - Right-hand rule navigation

### 🎨 **Visualization Options**
- **ASCII Art** - Terminal-friendly text output
- **Matplotlib** - High-quality static images
- **Pygame** - Interactive real-time visualization
- **Image Export** - PNG, JPEG, SVG formats

### 🛠️ **Key Features**
- Multiple output formats (PNG, JPEG, SVG, ASCII)
- Configurable maze dimensions and visual parameters
- Reproducible results with seed support
- Command-line interface for easy usage
- Comprehensive API for programmatic use
- Performance benchmarking tools
- Extensive test coverage

## Installation

### From PyPI (when published)
```bash
pip install procedural-maze-generator
```

### From Source
```bash
git clone https://github.com/yourusername/procedural-maze-generator.git
cd procedural-maze-generator
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/yourusername/procedural-maze-generator.git
cd procedural-maze-generator
pip install -e ".[dev]"
```

## Quick Start

### Command Line Usage

Generate a simple maze:
```bash
maze-gen generate 20 20 --algorithm dfs --format png --output maze.png
```

Generate and solve a maze:
```bash
maze-gen solve 25 25 --gen-algorithm kruskal --solve-algorithm astar --format ascii
```

Interactive visualization:
```bash
maze-gen interactive 15 15 --algorithm prim
```

Benchmark algorithms:
```bash
maze-gen benchmark 20 20 --iterations 10
```

Manage output directories:
```bash
maze-gen output init --directory my_mazes
maze-gen output list --type images
maze-gen output clean --temp-only
maze-gen output info
```

### Python API Usage

```python
from maze_generator import Maze
from maze_generator.algorithms.generators import DepthFirstSearchGenerator
from maze_generator.algorithms.solvers import AStarSolver
from maze_generator.visualization import MatplotlibRenderer

# Create and generate a maze
maze = Maze(20, 20)
generator = DepthFirstSearchGenerator(seed=42)
generator.generate(maze)

# Set start and end points
maze.set_start(0, 0)
maze.set_end(19, 19)

# Solve the maze
solver = AStarSolver()
solution = solver.solve(maze)

# Visualize the result
renderer = MatplotlibRenderer()
renderer.show(maze, show_solution=True)
```

## Documentation

### Command Line Interface

The `maze-gen` command provides several subcommands:

#### Generate Command
```bash
maze-gen generate WIDTH HEIGHT [OPTIONS]
```

Options:
- `--algorithm, -a`: Generation algorithm (dfs, kruskal, prim, wilson)
- `--seed, -s`: Random seed for reproducible results
- `--output, -o`: Output file path
- `--format, -f`: Output format (png, jpg, svg, ascii, matplotlib)
- `--cell-size`: Cell size in pixels (default: 20)
- `--wall-width`: Wall width in pixels (default: 2)
- `--title`: Title for the maze
- `--start X Y`: Start position coordinates
- `--end X Y`: End position coordinates

#### Solve Command
```bash
maze-gen solve WIDTH HEIGHT [OPTIONS]
```

Additional options:
- `--gen-algorithm`: Algorithm for maze generation
- `--solve-algorithm`: Algorithm for maze solving
- `--show-visited`: Show visited cells during solving

#### Interactive Command
```bash
maze-gen interactive WIDTH HEIGHT [OPTIONS]
```

#### Benchmark Command
```bash
maze-gen benchmark WIDTH HEIGHT [OPTIONS]
```

Options:
- `--iterations, -i`: Number of benchmark iterations

#### Output Management Command
```bash
maze-gen output SUBCOMMAND [OPTIONS]
```

Subcommands:
- `init`: Initialize output directory structure
- `list`: List files in output directory
- `clean`: Clean output directory (with confirmation)
- `info`: Show output directory information

Options:
- `--directory, -d`: Output directory path
- `--type, -t`: File type to list (images, ascii, svg, animations, benchmarks)
- `--temp-only`: Clean only temporary files
- `--max-age`: Maximum age in hours for temp files (default: 24)

### Python API

#### Core Classes

**Maze**: The main maze data structure
```python
maze = Maze(width, height)
maze.set_start(x, y)
maze.set_end(x, y)
```

**Cell**: Individual maze cell
```python
cell = maze.get_cell(x, y)
cell.has_wall(Direction.NORTH)
cell.remove_wall(Direction.EAST)
```

#### Generation Algorithms

All generators inherit from `MazeGenerator`:
```python
from maze_generator.algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
    WilsonGenerator
)

generator = DepthFirstSearchGenerator(seed=42)
generator.generate(maze)
```

#### Solving Algorithms

All solvers inherit from `MazeSolver`:
```python
from maze_generator.algorithms.solvers import (
    AStarSolver,
    DijkstraSolver,
    BreadthFirstSearchSolver,
    DepthFirstSearchSolver
)

solver = AStarSolver()
path = solver.solve(maze)
```

#### Visualization

**ASCII Renderer**:
```python
from maze_generator.visualization import AsciiRenderer

renderer = AsciiRenderer()
renderer.print_maze(maze, show_solution=True)
renderer.save_to_file(maze, "maze.txt")
```

**Matplotlib Renderer**:
```python
from maze_generator.visualization import MatplotlibRenderer

renderer = MatplotlibRenderer(cell_size=30, wall_width=3)
renderer.show(maze, show_solution=True)
renderer.save_image(maze, "maze.png", dpi=300)
```

**Image Exporter**:
```python
from maze_generator.visualization import ImageExporter

exporter = ImageExporter(cell_size=25)
exporter.export_png(maze, "maze.png", show_solution=True)
exporter.export_svg(maze, "maze.svg", title="My Maze")
```

#### Output Directory Management

The application includes comprehensive output directory management:

```python
from maze_generator.utils import OutputManager

# Create output manager
manager = OutputManager("my_output_dir")

# Initialize directory structure
manager.initialize_output_structure()

# Get organized output paths
path = manager.organize_by_algorithm("dfs", "maze.png", "images")
timestamped_path = manager.get_timestamped_filename("maze", "png", "images")
auto_path = manager.get_auto_filename("maze", "png", "images")

# Clean up temporary files
cleaned = manager.cleanup_temp_files(max_age_hours=24)

# Get directory information
usage = manager.get_disk_usage()
file_lists = manager.list_output_files()
```

## Configuration

Create a configuration file at `~/.maze_generator/config.yaml`:

```yaml
visualization:
  cell_size: 25
  wall_width: 3
  colors:
    wall: '#000000'
    path: '#FFFFFF'
    start: '#00FF00'
    end: '#FF0000'
    solution: '#0000FF'

generation:
  default_algorithm: 'dfs'
  default_width: 20
  default_height: 20
  animation_delay_ms: 50

solving:
  default_algorithm: 'astar'
  animation_delay_ms: 100
  show_visited: true

export:
  default_format: 'png'
  default_dpi: 300
  jpeg_quality: 95
```

## Examples

See the `examples/` directory for more detailed usage examples:

- `basic_usage.py` - Simple maze generation and solving
- `custom_visualization.py` - Custom colors and styling
- `animation_example.py` - Animated maze generation
- `batch_processing.py` - Generate multiple mazes
- `performance_comparison.py` - Algorithm benchmarking

## Algorithm Details

### Generation Algorithms

**Depth-First Search (DFS)**
- Creates mazes with long, winding passages
- Low branching factor
- Fast generation
- Good for creating challenging mazes

**Kruskal's Algorithm**
- Creates mazes with shorter passages
- Higher branching factor
- Uniform spanning tree approach
- Good balance of difficulty and solvability

**Prim's Algorithm**
- Similar to Kruskal's but grows from a single point
- Creates tree-like structures
- Medium branching factor
- Reliable and efficient

**Wilson's Algorithm**
- Uses loop-erased random walks
- Creates unbiased spanning trees
- Slower than other algorithms
- Produces very uniform mazes

### Solving Algorithms

**A\* (A-Star)**
- Optimal pathfinding with Manhattan distance heuristic
- Fast and efficient
- Guaranteed shortest path
- Best general-purpose solver

**Dijkstra's Algorithm**
- Guaranteed shortest path
- No heuristic needed
- Slower than A* but more thorough
- Good for analysis and verification

**Breadth-First Search (BFS)**
- Level-by-level exploration
- Guaranteed shortest path
- Simple implementation
- Good for educational purposes

**Depth-First Search (DFS)**
- Deep exploration strategy
- Not guaranteed to find shortest path
- Fast execution
- May find very long paths

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=maze_generator --cov-report=html
```

Run specific test categories:
```bash
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic maze generation algorithms
- Built with Python's scientific computing ecosystem
- Thanks to the open-source community for excellent libraries

## Changelog

### Version 1.0.0
- Initial release
- Multiple generation and solving algorithms
- Comprehensive visualization options
- Command-line interface
- Full test coverage
- Complete documentation
