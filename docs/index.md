---
layout: default
title: Home
---

# 🎯 Procedural Maze Generator

A comprehensive Python library for generating and solving mazes using various algorithms, with multiple visualization options and export formats.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Demo](https://img.shields.io/badge/demo-interactive-orange.svg)](gallery/)

## 🚀 Quick Start

```bash
# Install
pip install procedural-maze-generator

# Generate a maze
maze-gen generate 15 12 --algorithm dfs --format ascii

# Solve a maze
maze-gen solve 12 10 --gen-algorithm kruskal --solve-algorithm astar --format png
```

## 🎨 Gallery

Explore our comprehensive collection of maze examples:

### Generation Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| **DFS** | Depth-First Search - Creates long winding passages | [View Example](gallery/algorithms/dfs_maze_example.svg) |
| **Kruskal** | Uniform distribution of passages | [View Example](gallery/algorithms/kruskal_maze_example.svg) |
| **Prim** | Shorter passages with more branching | [View Example](gallery/algorithms/prim_maze_example.svg) |

### Solving Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| **A*** | Optimal pathfinding with heuristics | [View Solution](gallery/solutions/astar_solution_example.svg) |

[**🎨 View Full Gallery →**](gallery/)

## 🔧 Features

- **4 Generation Algorithms**: DFS, Kruskal, Prim, Wilson
- **5 Solving Algorithms**: A*, Dijkstra, BFS, DFS, Wall Follower
- **Multiple Output Formats**: ASCII, PNG, JPEG, SVG
- **Advanced Output Management**: Organized directories, timestamped files
- **Interactive Demos**: Comprehensive demonstration system
- **High-Quality Visualizations**: Customizable colors and styling

## 📊 Demo System

Our demo system provides multiple ways to explore the maze generator:

- **Interactive Python Demo**: Step-by-step guided tour
- **Shell Script Demo**: Automated demonstration with colored output
- **Gallery Examples**: Permanent visual documentation
- **CI/CD Integration**: Automated sample generation

## 🤝 Community

- **GitHub Repository**: [View Source Code](https://github.com/refactornator/procedural-maze-generator)
- **Issue Tracker**: [Report Bugs or Request Features](https://github.com/refactornator/procedural-maze-generator/issues)
- **Showcase**: [Share Your Amazing Mazes](https://github.com/refactornator/procedural-maze-generator/issues/new?template=showcase.md)

## 📚 Documentation

- [**Gallery**](gallery/) - Visual examples and comparisons
- [**Demo Visibility**](DEMO_VISIBILITY.html) - How we make outputs accessible
- [**GitHub Repository**](https://github.com/refactornator/procedural-maze-generator) - Full documentation and source code

---

*Generate amazing mazes with the power of algorithms! 🎯*
