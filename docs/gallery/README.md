# Maze Gallery

Visual examples showcasing different algorithms and solving methods.

## Generation Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| **DFS** | Long winding passages | ![DFS](algorithms/dfs_maze_example.svg) |
| **Kruskal** | Uniform distribution | ![Kruskal](algorithms/kruskal_maze_example.svg) |
| **Prim** | Short passages, more branching | ![Prim](algorithms/prim_maze_example.svg) |

## Solving Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| **A*** | Optimal with heuristics | ![A*](solutions/astar_solution_example.svg) |
| **Dijkstra** | Guaranteed shortest path | <details><summary>View Solution</summary><pre>┌───────────────────────────┐<br>│ Dijkstra's Algorithm Solution (37 steps) │<br>├───────────────────────────┤<br>│ █████████████████████████ │<br>│ █S█·······█···········  █ │<br>│ █·█·█████·█·█████████·███ │<br>│ █·█·····█···█   █   █···█ │<br>│ █·█████·█████ █ ███ ███·█ │<br>│ █·····█·█     █       █·█ │<br>│ █████·█·█ ███████ █████·█ │<br>│ █   █···█ █       █·····█ │<br>│ █ █ █ ███ ███████ █·█████ │<br>│ █ █ █     █     █ █·····█ │<br>│ ███ █████ █ ███ ███████·█ │<br>│ █ █ █     █ █   █     █·█ │<br>│ █ ███ ███ █ █ █ █████ █·█ │<br>│ █     █   █ █ █       █·█ │<br>│ █████ █ ███ █ █████████·█ │<br>│ █     █ █   █         █·█ │<br>│ █ █████ █ ███ █████████·█ │<br>│ █ █     █ █   █       █·█ │<br>│ █ █ █████ █ ███ █████ █·█ │<br>│ █   █     █     █     █·█ │<br>│ █████ █████████ █████ █·█ │<br>│ █                     █E█ │<br>│ █████████████████████████ │<br>└───────────────────────────┘</pre></details> |
| **BFS** | Level-by-level exploration | <details><summary>View Solution</summary><pre>┌───────────────────────────┐<br>│ BFS Solution (37 steps)   │<br>├───────────────────────────┤<br>│ █████████████████████████ │<br>│ █S█·······█···········  █ │<br>│ █·█·█████·█·█████████·███ │<br>│ █·█·····█···█   █   █···█ │<br>│ █·█████·█████ █ ███ ███·█ │<br>│ █·····█·█     █       █·█ │<br>│ █████·█·█ ███████ █████·█ │<br>│ █                     █E█ │<br>│ █████████████████████████ │<br>└───────────────────────────┘</pre></details> |

## Algorithm Comparison

[Side-by-side comparison](comparisons/algorithm_comparison.md) of different algorithms using the same seed.

## Output Formats

| Format | Description | Example |
|--------|-------------|---------|
| **ASCII** | Text-based, universal | <details><summary>View ASCII</summary><pre>+-+-+-+-+-+-+-+-+-+-+<br>|S ·|       | | |   |<br>+-+ +-+ +-+-+ + +-+ +<br>|· ·        |       |<br>+ +-+-+-+-+-+ +-+-+ +<br>|· · ·  | | |   |   |<br>+ + + +-+ + + +-+-+-+<br>| | |· ·  |         |<br>+ + +-+ +-+-+-+ + + +<br>| | | |·|  · ·  | | |<br>+-+-+ + +-+ + +-+-+-+<br>|      · · ·|·|  · ·|<br>+ + +-+-+-+-+ +-+ + +<br>| |       |  ·|· ·|·|<br>+ + + + +-+-+ + +-+ +<br>| | | | |    · ·|  E|<br>+-+-+-+-+-+-+-+-+-+-+</pre></details> |
| **SVG** | Scalable vector graphics | ![SVG](formats/svg_maze_example.svg) |
| **PNG** | High-quality images | [View](formats/png_maze_example.png) |

## Quick Start

Generate your own examples:

```bash
# Run interactive demo
python demo/run_demo.py

# Generate specific maze
maze-gen generate 15 12 --algorithm dfs --format png

# Solve a maze
maze-gen solve 12 10 --gen-algorithm kruskal --solve-algorithm astar
```

## Directory Structure

```
gallery/
├── algorithms/     # Generation examples
├── solutions/      # Solving examples
├── formats/        # Output format demos
└── comparisons/    # Algorithm comparisons
```
