#!/usr/bin/env python3
"""
Performance comparison example for maze generation and solving algorithms.

This example benchmarks different algorithms and provides performance insights.
"""

import time
import statistics
from typing import Dict, List, Tuple

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
    DepthFirstSearchSolver,
)
from maze_generator.utils.performance import Timer, benchmark_function


def benchmark_generators(sizes: List[Tuple[int, int]], iterations: int = 10) -> Dict:
    """Benchmark maze generation algorithms."""
    print("Benchmarking Maze Generation Algorithms")
    print("=" * 50)
    
    generators = {
        "Depth-First Search": DepthFirstSearchGenerator,
        "Kruskal's Algorithm": KruskalGenerator,
        "Prim's Algorithm": PrimGenerator,
        "Wilson's Algorithm": WilsonGenerator,
    }
    
    results = {}
    
    for size_name, (width, height) in [("Small", (10, 10)), ("Medium", (25, 25)), ("Large", (50, 50))]:
        print(f"\n{size_name} Maze ({width}x{height}):")
        print("-" * 30)
        
        size_results = {}
        
        for name, generator_class in generators.items():
            def generate_maze():
                maze = Maze(width, height)
                generator = generator_class(seed=42)
                generator.generate(maze)
                return maze
            
            # Benchmark the generator
            stats = benchmark_function(generate_maze, iterations=iterations)
            size_results[name] = stats
            
            print(f"{name:20} | "
                  f"Avg: {stats['avg']:.4f}s | "
                  f"Min: {stats['min']:.4f}s | "
                  f"Max: {stats['max']:.4f}s")
        
        results[size_name] = size_results
        
        # Find fastest for this size
        fastest = min(size_results.items(), key=lambda x: x[1]['avg'])
        print(f"\nFastest: {fastest[0]} ({fastest[1]['avg']:.4f}s average)")
    
    return results


def benchmark_solvers(maze_size: Tuple[int, int] = (20, 20), iterations: int = 10) -> Dict:
    """Benchmark maze solving algorithms."""
    print(f"\n\nBenchmarking Maze Solving Algorithms ({maze_size[0]}x{maze_size[1]})")
    print("=" * 50)
    
    solvers = {
        "A* Algorithm": AStarSolver,
        "Dijkstra's Algorithm": DijkstraSolver,
        "Breadth-First Search": BreadthFirstSearchSolver,
        "Depth-First Search": DepthFirstSearchSolver,
    }
    
    # Create a consistent maze for all solvers
    base_maze = Maze(maze_size[0], maze_size[1])
    generator = DepthFirstSearchGenerator(seed=42)
    generator.generate(base_maze)
    base_maze.set_start(0, 0)
    base_maze.set_end(maze_size[0] - 1, maze_size[1] - 1)
    
    results = {}
    solution_lengths = {}
    
    for name, solver_class in solvers.items():
        def solve_maze():
            # Create a fresh copy of the maze for each solve
            maze = Maze(maze_size[0], maze_size[1])
            generator = DepthFirstSearchGenerator(seed=42)
            generator.generate(maze)
            maze.set_start(0, 0)
            maze.set_end(maze_size[0] - 1, maze_size[1] - 1)
            
            solver = solver_class()
            solution = solver.solve(maze)
            return len(solution)
        
        # Benchmark the solver
        stats = benchmark_function(solve_maze, iterations=iterations)
        results[name] = stats
        
        # Get solution length (should be consistent)
        solver = solver_class()
        solution = solver.solve(base_maze)
        solution_lengths[name] = len(solution)
        
        print(f"{name:20} | "
              f"Avg: {stats['avg']:.4f}s | "
              f"Solution: {len(solution):2d} steps")
    
    # Find fastest solver
    fastest = min(results.items(), key=lambda x: x[1]['avg'])
    print(f"\nFastest: {fastest[0]} ({fastest[1]['avg']:.4f}s average)")
    
    # Find optimal solutions
    min_length = min(solution_lengths.values())
    optimal_solvers = [name for name, length in solution_lengths.items() if length == min_length]
    print(f"Optimal solution length: {min_length} steps")
    print(f"Optimal solvers: {', '.join(optimal_solvers)}")
    
    return results


def memory_usage_analysis():
    """Analyze memory usage of different algorithms."""
    print("\n\nMemory Usage Analysis")
    print("=" * 30)
    
    try:
        import psutil
        import os
        
        def get_memory_usage():
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024  # MB
        
        sizes = [(10, 10), (25, 25), (50, 50), (100, 100)]
        
        for width, height in sizes:
            print(f"\nMaze size: {width}x{height}")
            
            initial_memory = get_memory_usage()
            
            # Test DFS generator
            maze = Maze(width, height)
            generator = DepthFirstSearchGenerator()
            generator.generate(maze)
            
            after_generation = get_memory_usage()
            
            # Test A* solver
            maze.set_start(0, 0)
            maze.set_end(width - 1, height - 1)
            solver = AStarSolver()
            solution = solver.solve(maze)
            
            after_solving = get_memory_usage()
            
            print(f"  Generation: +{after_generation - initial_memory:.2f} MB")
            print(f"  Solving:    +{after_solving - after_generation:.2f} MB")
            print(f"  Total:      +{after_solving - initial_memory:.2f} MB")
            
            # Clean up
            del maze, generator, solver, solution
    
    except ImportError:
        print("psutil not available - skipping memory analysis")
        print("Install with: pip install psutil")


def scalability_test():
    """Test algorithm scalability with increasing maze sizes."""
    print("\n\nScalability Test")
    print("=" * 25)
    
    sizes = [(5, 5), (10, 10), (20, 20), (30, 30), (40, 40)]
    
    print("Size     | DFS Gen  | A* Solve | Total   ")
    print("-" * 40)
    
    for width, height in sizes:
        # Test generation
        with Timer() as gen_timer:
            maze = Maze(width, height)
            generator = DepthFirstSearchGenerator(seed=42)
            generator.generate(maze)
        
        # Test solving
        maze.set_start(0, 0)
        maze.set_end(width - 1, height - 1)
        
        with Timer() as solve_timer:
            solver = AStarSolver()
            solution = solver.solve(maze)
        
        total_time = gen_timer.elapsed_time + solve_timer.elapsed_time
        
        print(f"{width:2d}x{height:2d}   | "
              f"{gen_timer.elapsed_time:.4f}s | "
              f"{solve_timer.elapsed_time:.4f}s | "
              f"{total_time:.4f}s")


def algorithm_characteristics():
    """Analyze characteristics of different algorithms."""
    print("\n\nAlgorithm Characteristics Analysis")
    print("=" * 40)
    
    maze_size = (20, 20)
    iterations = 20
    
    generators = {
        "DFS": DepthFirstSearchGenerator,
        "Kruskal": KruskalGenerator,
        "Prim": PrimGenerator,
    }
    
    print("Algorithm | Avg Path | Std Dev | Branching")
    print("-" * 45)
    
    for name, generator_class in generators.items():
        path_lengths = []
        
        for i in range(iterations):
            maze = Maze(maze_size[0], maze_size[1])
            generator = generator_class(seed=i)
            generator.generate(maze)
            
            maze.set_start(0, 0)
            maze.set_end(maze_size[0] - 1, maze_size[1] - 1)
            
            solver = AStarSolver()
            solution = solver.solve(maze)
            path_lengths.append(len(solution))
        
        avg_length = statistics.mean(path_lengths)
        std_dev = statistics.stdev(path_lengths)
        
        # Calculate branching factor (rough estimate)
        # Count cells with multiple exits
        maze = Maze(maze_size[0], maze_size[1])
        generator = generator_class(seed=42)
        generator.generate(maze)
        
        branching_points = 0
        total_cells = 0
        
        for cell in maze:
            exits = sum(1 for direction in [d for d in cell.walls if d not in cell.walls])
            if exits > 2:  # More than 2 exits = branching point
                branching_points += 1
            total_cells += 1
        
        branching_factor = branching_points / total_cells
        
        print(f"{name:9} | {avg_length:8.1f} | {std_dev:7.2f} | {branching_factor:8.3f}")


def main():
    """Run all performance benchmarks."""
    print("Procedural Maze Generator - Performance Analysis")
    print("=" * 55)
    
    # Benchmark generators
    gen_results = benchmark_generators([(10, 10), (25, 25), (50, 50)])
    
    # Benchmark solvers
    solver_results = benchmark_solvers((20, 20))
    
    # Memory analysis
    memory_usage_analysis()
    
    # Scalability test
    scalability_test()
    
    # Algorithm characteristics
    algorithm_characteristics()
    
    print("\n" + "=" * 55)
    print("Performance analysis complete!")
    print("\nKey Takeaways:")
    print("- DFS is typically fastest for generation")
    print("- A* provides optimal solutions efficiently")
    print("- Memory usage scales roughly O(n²) with maze size")
    print("- Different algorithms create mazes with different characteristics")


if __name__ == "__main__":
    main()
