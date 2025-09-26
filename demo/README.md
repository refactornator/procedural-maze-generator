# Procedural Maze Generator - Demo

This directory contains comprehensive demonstrations of the Procedural Maze Generator, showcasing all features including the advanced output directory management system.

## 🚀 Quick Start

### Interactive Python Demo
```bash
# Full interactive demo with explanations
python demo/interactive_demo.py

# Quick demo without pauses
python demo/interactive_demo.py --quick
```

### Shell Script Demo
```bash
# Full demo with colored output
./demo/demo.sh

# Quick demo
./demo/demo.sh --quick

# No pauses between commands
./demo/demo.sh --no-pause
```

## 📁 Demo Contents

### Scripts
- **`interactive_demo.py`** - Comprehensive Python demo with step-by-step explanations
- **`demo.sh`** - Shell script demo with colored output and progress indicators
- **`generate_samples.py`** - Generate sample outputs for documentation

### Configuration Files
- **`configs/demo_config.yaml`** - Optimized settings for demonstrations
- **`configs/presentation_config.yaml`** - Settings for presentations and screenshots

### Sample Outputs
- **`samples/`** - Pre-generated sample mazes and outputs
- **`readme_examples/`** - Examples specifically for README documentation

## 🎯 What the Demo Shows

### Core Features
- ✨ **Multiple Generation Algorithms**: DFS, Kruskal, Prim, Wilson
- 🧭 **Various Solving Algorithms**: A*, Dijkstra, BFS, DFS, Wall Follower
- 🎨 **Multiple Output Formats**: ASCII, PNG, JPEG, SVG
- 📏 **Customizable Sizes**: From small 5x5 to large 50x50+ mazes

### Output Directory Management
- 📂 **Automatic Directory Creation**: Organized folder structure
- 🗂️ **File Organization Options**:
  - By algorithm (dfs/, kruskal/, prim/)
  - By date (2024-12-26/, 2024-12-27/)
  - Timestamped filenames
  - Auto-numbered sequences
- 🧹 **Maintenance Features**:
  - Temporary file cleanup
  - Disk space monitoring
  - Directory statistics
  - File listing and management

### Advanced Features
- ⚡ **Performance Benchmarking**: Compare algorithm speeds
- 🎛️ **Configuration Management**: YAML/JSON settings
- 🖥️ **Interactive Visualization**: Real-time pygame display
- 📊 **Statistics and Analysis**: Path lengths, generation times

## 📋 Demo Walkthrough

### 1. Basic Maze Generation
```bash
# Generate a simple maze
maze-gen generate 12 8 --algorithm dfs --format ascii

# Save to file
maze-gen generate 15 10 --algorithm kruskal --format png --output maze.png
```

### 2. Output Directory Setup
```bash
# Initialize organized output structure
maze-gen output init --directory demo_output

# Show directory information
maze-gen output info --directory demo_output
```

### 3. Organized File Generation
```bash
# Generate mazes organized by algorithm
maze-gen generate 12 8 --algorithm dfs --format png --output-dir demo_output --organize-by-algorithm
maze-gen generate 12 8 --algorithm kruskal --format png --output-dir demo_output --organize-by-algorithm

# Generate with timestamps
maze-gen generate 10 6 --algorithm prim --format png --output-dir demo_output --timestamped
```

### 4. Maze Solving
```bash
# Generate and solve a maze
maze-gen solve 15 12 --gen-algorithm dfs --solve-algorithm astar --format png --output-dir demo_output --show-visited

# Compare different solvers
maze-gen solve 10 8 --gen-algorithm kruskal --solve-algorithm dijkstra --format ascii
maze-gen solve 10 8 --gen-algorithm kruskal --solve-algorithm bfs --format ascii
```

### 5. File Management
```bash
# List generated files
maze-gen output list --directory demo_output --type images

# Show directory statistics
maze-gen output info --directory demo_output

# Clean temporary files
maze-gen output clean --directory demo_output --temp-only
```

## 🎨 Sample Outputs

### ASCII Art Maze
```
+---+---+---+---+---+---+---+---+---+---+---+---+
|S      |           |                   |       |
+ +---+ +---+---+ + + +---+---+---+---+ + +---+ +
| |   |         | | | |               | | |   | |
+ + + +---+---+ + + + + +---+---+---+ + + + + + +
| | |         | | | | |             | | | | | | |
+ + +---+---+ + + + + +---+---+---+ + + + + + + +
| |         | | | | |             | | | | | | | |
+ +---+---+ + + + + +---+---+---+ + + + + + + + +
|         | | | | |             | | | | | | | | |
+---+---+ + + + + +---+---+---+ + + + + + + + + +
|       | | | | |             | | | | | | | | | |
+ +---+ + + + + +---+---+---+ + + + + + + + + + E
| |   | | | | |             | | | | | | | | | | |
+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Directory Structure
```
demo_output/
├── README.txt
├── images/
│   ├── dfs/
│   │   ├── maze_dfs_001.png
│   │   └── maze_dfs_002.png
│   ├── kruskal/
│   │   └── maze_kruskal_001.png
│   └── maze_20241226_143022.png
├── ascii/
│   ├── 2024-12-26/
│   │   └── daily_maze.txt
│   └── solution_output.txt
├── svg/
│   └── vector_maze.svg
└── temp/
    └── (temporary files)
```

## 🔧 Customization

### Using Custom Configuration
```bash
# Use demo configuration
export MAZE_CONFIG=demo/configs/demo_config.yaml
maze-gen generate 15 12 --algorithm dfs --format png

# Use presentation configuration
export MAZE_CONFIG=demo/configs/presentation_config.yaml
maze-gen generate 12 10 --algorithm kruskal --format svg
```

### Custom Output Directory
```bash
# Specify custom output directory
maze-gen generate 20 15 --algorithm prim --format png --output-dir my_custom_mazes --organize-by-date
```

## 🎬 Creating Your Own Demo

### 1. Generate Sample Files
```bash
python demo/generate_samples.py
```

### 2. Run Benchmarks
```bash
maze-gen benchmark 20 20 --iterations 10 > benchmark_results.txt
```

### 3. Create Algorithm Comparison
```bash
for algo in dfs kruskal prim; do
    maze-gen generate 15 12 --algorithm $algo --format png --output comparison_${algo}.png --seed 42
done
```

## 📚 Additional Resources

- **Main README**: `../README.md` - Complete project documentation
- **Examples**: `../examples/` - Detailed code examples
- **Configuration**: `../config/` - Configuration file templates
- **Tests**: `../tests/` - Test suite for verification

## 🤝 Contributing

Found an issue with the demo or have suggestions for improvements?
1. Check existing issues on GitHub
2. Create a new issue with the "demo" label
3. Submit a pull request with improvements

## 📄 License

This demo is part of the Procedural Maze Generator project and is licensed under the MIT License.
