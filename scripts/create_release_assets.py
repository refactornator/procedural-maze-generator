#!/usr/bin/env python3
"""
Create release assets with demo outputs.

This script generates a comprehensive package of demo outputs
that can be attached to GitHub releases for easy access.
"""

import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime


def create_demo_package():
    """Create a comprehensive demo package for releases."""
    print("📦 Creating Demo Release Package")
    print("=" * 40)
    
    # Create package directory
    package_dir = Path("release_assets")
    package_dir.mkdir(exist_ok=True)
    
    # Generate fresh samples
    print("🎨 Generating fresh demo samples...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "demo/generate_gallery_samples.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Gallery samples generated successfully")
        else:
            print("⚠️  Gallery generation had issues, continuing...")
    except Exception as e:
        print(f"⚠️  Could not generate gallery: {e}")
    
    # Create demo package
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"maze_generator_demos_{timestamp}"
    package_path = package_dir / f"{package_name}.zip"
    
    print(f"📁 Creating package: {package_name}.zip")
    
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add gallery files
        gallery_dir = Path("docs/gallery")
        if gallery_dir.exists():
            for file_path in gallery_dir.rglob("*"):
                if file_path.is_file():
                    arc_path = f"{package_name}/gallery/{file_path.relative_to(gallery_dir)}"
                    zf.write(file_path, arc_path)
                    print(f"  📄 Added: {arc_path}")
        
        # Add demo scripts
        demo_dir = Path("demo")
        if demo_dir.exists():
            for script in ["interactive_demo.py", "demo.sh", "run_demo.py"]:
                script_path = demo_dir / script
                if script_path.exists():
                    arc_path = f"{package_name}/scripts/{script}"
                    zf.write(script_path, arc_path)
                    print(f"  📄 Added: {arc_path}")
        
        # Add examples
        examples_dir = Path("examples")
        if examples_dir.exists():
            for example in examples_dir.glob("*.py"):
                arc_path = f"{package_name}/examples/{example.name}"
                zf.write(example, arc_path)
                print(f"  📄 Added: {arc_path}")
        
        # Add README and documentation
        for doc in ["README.md", "LICENSE"]:
            doc_path = Path(doc)
            if doc_path.exists():
                arc_path = f"{package_name}/{doc}"
                zf.write(doc_path, arc_path)
                print(f"  📄 Added: {arc_path}")
        
        # Add package info
        info_content = f"""# Maze Generator Demo Package

Generated: {datetime.now().isoformat()}
Version: 1.0.0

## Contents

- `gallery/` - Visual examples and documentation
- `scripts/` - Demo scripts (Python and shell)
- `examples/` - Code examples
- `README.md` - Main documentation
- `LICENSE` - License information

## Quick Start

1. Install the maze generator: `pip install procedural-maze-generator`
2. Run interactive demo: `python scripts/interactive_demo.py`
3. Try examples: `python examples/basic_usage.py`
4. View gallery: Open `gallery/README.md`

## Links

- GitHub: https://github.com/yourusername/procedural-maze-generator
- Documentation: See README.md
- Issues: https://github.com/yourusername/procedural-maze-generator/issues
"""
        
        zf.writestr(f"{package_name}/PACKAGE_INFO.md", info_content)
        print(f"  📄 Added: {package_name}/PACKAGE_INFO.md")
    
    print(f"\n✅ Package created: {package_path}")
    print(f"📊 Package size: {package_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    return package_path


def create_quick_start_guide():
    """Create a quick start guide with embedded examples."""
    print("\n📖 Creating Quick Start Guide")
    
    guide_content = """# 🚀 Procedural Maze Generator - Quick Start

Welcome to the Procedural Maze Generator! This guide will get you up and running in minutes.

## 📦 Installation

```bash
pip install procedural-maze-generator
```

## 🎯 Basic Usage

### Generate a Simple Maze

```bash
# ASCII output
maze-gen generate 10 8 --algorithm dfs --format ascii

# Save as PNG image
maze-gen generate 15 12 --algorithm kruskal --format png --output my_maze.png
```

### Solve a Maze

```bash
# Generate and solve in one command
maze-gen solve 12 10 --gen-algorithm prim --solve-algorithm astar --format ascii
```

### Interactive Demo

```bash
# Run the comprehensive demo
python -c "from maze_generator.demo import run_interactive_demo; run_interactive_demo()"
```

## 🎨 Example Output

Here's what you can expect:

### ASCII Maze
```
+---+---+---+---+---+---+---+---+
|S      |           |           |
+ +---+ +---+---+ + +---+---+ + +
| |   |         | |         | | |
+ + + +---+---+ + +---+---+ + + +
| | |         | |         | | | |
+ + +---+---+ + +---+---+ + + + +
| |         | |         | | | | |
+ +---+---+ + +---+---+ + + + + +
|         | |         | | | | | |
+---+---+ + +---+---+ + + + + + E
|       | |         | | | | | | |
+---+---+---+---+---+---+---+---+
```

### Available Algorithms

**Generation:**
- DFS (Depth-First Search) - Long winding passages
- Kruskal - Uniform distribution
- Prim - Shorter passages, more branching
- Wilson - Unbiased, uniform distribution

**Solving:**
- A* - Optimal with heuristics
- Dijkstra - Guaranteed shortest path
- BFS - Level-by-level exploration
- DFS - Deep exploration
- Wall Follower - Simple rule-based

## 📁 Output Management

```bash
# Initialize organized output directory
maze-gen output init --directory my_mazes

# Generate with organization
maze-gen generate 15 12 --algorithm dfs --output-dir my_mazes --organize-by-algorithm

# List generated files
maze-gen output list --directory my_mazes --type images
```

## 🎬 Advanced Features

### Animated Generation
```python
from maze_generator.demo import create_animated_demo
create_animated_demo()
```

### Custom Visualization
```python
from maze_generator import Maze
from maze_generator.algorithms.generators import KruskalGenerator
from maze_generator.visualization import ImageExporter

maze = Maze(20, 15)
generator = KruskalGenerator(seed=42)
generator.generate(maze)

exporter = ImageExporter(cell_size=30, wall_width=3)
exporter.export_png(maze, "custom_maze.png", title="My Custom Maze")
```

## 🔧 Configuration

Create a `maze_config.yaml` file:

```yaml
visualization:
  cell_size: 25
  wall_width: 2
  colors:
    wall: '#2c3e50'
    path: '#ecf0f1'
    start: '#27ae60'
    end: '#e74c3c'
    solution: '#3498db'

generation:
  default_algorithm: 'kruskal'
  default_width: 15
  default_height: 12
```

## 🆘 Getting Help

```bash
# General help
maze-gen --help

# Command-specific help
maze-gen generate --help
maze-gen solve --help
maze-gen output --help
```

## 🌟 Next Steps

1. **Explore Examples**: Check out the `examples/` directory
2. **Run Demos**: Try `python demo/interactive_demo.py`
3. **Read Documentation**: See the full README.md
4. **Join Community**: Report issues and contribute on GitHub

---

Happy maze generating! 🎯
"""
    
    guide_path = Path("release_assets/QUICK_START.md")
    guide_path.parent.mkdir(exist_ok=True)
    
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    print(f"✅ Quick start guide created: {guide_path}")
    return guide_path


def main():
    """Create all release assets."""
    try:
        # Create demo package
        package_path = create_demo_package()
        
        # Create quick start guide
        guide_path = create_quick_start_guide()
        
        print("\n" + "=" * 50)
        print("🎉 Release Assets Created Successfully!")
        print("=" * 50)
        print(f"📦 Demo Package: {package_path}")
        print(f"📖 Quick Start: {guide_path}")
        print("\n💡 Usage:")
        print("1. Attach the demo package to GitHub releases")
        print("2. Include the quick start guide in release notes")
        print("3. Update README with links to gallery images")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error creating release assets: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
