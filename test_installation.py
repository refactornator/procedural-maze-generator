#!/usr/bin/env python3
"""
Test script to verify that the Procedural Maze Generator is properly installed.

This script performs basic functionality tests to ensure the package works correctly.
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Core imports
        from maze_generator import Maze, Cell, Direction
        from maze_generator.maze import Maze as MazeClass
        
        # Algorithm imports
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
        
        # Visualization imports
        from maze_generator.visualization import (
            AsciiRenderer,
            MatplotlibRenderer,
            ImageExporter,
        )
        
        # Utility imports
        from maze_generator.config import ConfigManager
        from maze_generator.utils.performance import Timer
        
        print("✓ All imports successful")
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic maze generation and solving."""
    print("\nTesting basic functionality...")
    
    try:
        from maze_generator import Maze
        from maze_generator.algorithms.generators import DepthFirstSearchGenerator
        from maze_generator.algorithms.solvers import AStarSolver
        from maze_generator.visualization import AsciiRenderer
        
        # Create a small maze
        maze = Maze(5, 5)
        print("✓ Maze creation successful")
        
        # Generate the maze
        generator = DepthFirstSearchGenerator(seed=42)
        generator.generate(maze)
        print("✓ Maze generation successful")
        
        # Set start and end points
        maze.set_start(0, 0)
        maze.set_end(4, 4)
        print("✓ Start/end point setting successful")
        
        # Solve the maze
        solver = AStarSolver()
        solution = solver.solve(maze)
        print(f"✓ Maze solving successful (solution length: {len(solution)})")
        
        # Render as ASCII
        renderer = AsciiRenderer()
        ascii_maze = renderer.render_compact(maze, show_solution=True)
        print("✓ ASCII rendering successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False


def test_cli_import():
    """Test that CLI can be imported."""
    print("\nTesting CLI import...")
    
    try:
        from maze_generator.cli import MazeGeneratorCLI
        cli = MazeGeneratorCLI()
        print("✓ CLI import and instantiation successful")
        return True
        
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False


def test_configuration():
    """Test configuration system."""
    print("\nTesting configuration system...")
    
    try:
        from maze_generator.config import ConfigManager, MazeGeneratorConfig
        
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Test that config has expected attributes
        assert hasattr(config, 'visualization')
        assert hasattr(config, 'generation')
        assert hasattr(config, 'solving')
        assert hasattr(config, 'export')
        
        print("✓ Configuration system working")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_visualization_backends():
    """Test different visualization backends."""
    print("\nTesting visualization backends...")
    
    results = {}
    
    # Test ASCII renderer (should always work)
    try:
        from maze_generator.visualization import AsciiRenderer
        renderer = AsciiRenderer()
        results['ASCII'] = True
        print("✓ ASCII renderer available")
    except Exception as e:
        results['ASCII'] = False
        print(f"✗ ASCII renderer failed: {e}")
    
    # Test Matplotlib renderer
    try:
        from maze_generator.visualization import MatplotlibRenderer
        renderer = MatplotlibRenderer()
        results['Matplotlib'] = True
        print("✓ Matplotlib renderer available")
    except Exception as e:
        results['Matplotlib'] = False
        print(f"✗ Matplotlib renderer failed: {e}")
    
    # Test Pygame renderer
    try:
        from maze_generator.visualization import PygameRenderer
        renderer = PygameRenderer()
        results['Pygame'] = True
        print("✓ Pygame renderer available")
    except Exception as e:
        results['Pygame'] = False
        print(f"✗ Pygame renderer failed: {e}")
    
    # Test Image exporter
    try:
        from maze_generator.visualization import ImageExporter
        exporter = ImageExporter()
        results['ImageExporter'] = True
        print("✓ Image exporter available")
    except Exception as e:
        results['ImageExporter'] = False
        print(f"✗ Image exporter failed: {e}")
    
    return results


def test_algorithms():
    """Test all available algorithms."""
    print("\nTesting algorithms...")
    
    from maze_generator import Maze
    
    # Test generators
    generators = {
        'DFS': 'maze_generator.algorithms.generators.DepthFirstSearchGenerator',
        'Kruskal': 'maze_generator.algorithms.generators.KruskalGenerator',
        'Prim': 'maze_generator.algorithms.generators.PrimGenerator',
    }
    
    generator_results = {}
    for name, class_path in generators.items():
        try:
            module_path, class_name = class_path.rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            generator_class = getattr(module, class_name)
            
            maze = Maze(5, 5)
            generator = generator_class(seed=42)
            generator.generate(maze)
            
            generator_results[name] = True
            print(f"✓ {name} generator working")
            
        except Exception as e:
            generator_results[name] = False
            print(f"✗ {name} generator failed: {e}")
    
    # Test solvers
    solvers = {
        'A*': 'maze_generator.algorithms.solvers.AStarSolver',
        'Dijkstra': 'maze_generator.algorithms.solvers.DijkstraSolver',
        'BFS': 'maze_generator.algorithms.solvers.BreadthFirstSearchSolver',
        'DFS': 'maze_generator.algorithms.solvers.DepthFirstSearchSolver',
    }
    
    solver_results = {}
    for name, class_path in solvers.items():
        try:
            module_path, class_name = class_path.rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            solver_class = getattr(module, class_name)
            
            # Create a solvable maze
            maze = Maze(5, 5)
            from maze_generator.algorithms.generators import DepthFirstSearchGenerator
            gen = DepthFirstSearchGenerator(seed=42)
            gen.generate(maze)
            maze.set_start(0, 0)
            maze.set_end(4, 4)
            
            solver = solver_class()
            solution = solver.solve(maze)
            
            solver_results[name] = len(solution) > 0
            print(f"✓ {name} solver working (solution: {len(solution)} steps)")
            
        except Exception as e:
            solver_results[name] = False
            print(f"✗ {name} solver failed: {e}")
    
    return generator_results, solver_results


def main():
    """Run all tests."""
    print("Procedural Maze Generator - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("CLI Import", test_cli_import),
        ("Configuration", test_configuration),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Additional tests
    viz_results = test_visualization_backends()
    gen_results, solver_results = test_algorithms()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    print("\nCore Tests:")
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name:20} | {status}")
    
    print("\nVisualization Backends:")
    for backend, available in viz_results.items():
        status = "AVAILABLE" if available else "UNAVAILABLE"
        print(f"  {backend:20} | {status}")
    
    print("\nGeneration Algorithms:")
    for algo, working in gen_results.items():
        status = "WORKING" if working else "FAILED"
        print(f"  {algo:20} | {status}")
    
    print("\nSolving Algorithms:")
    for algo, working in solver_results.items():
        status = "WORKING" if working else "FAILED"
        print(f"  {algo:20} | {status}")
    
    # Overall result
    all_core_passed = all(results.values())
    essential_viz = viz_results.get('ASCII', False)
    essential_algos = (gen_results.get('DFS', False) and 
                      solver_results.get('A*', False))
    
    overall_success = all_core_passed and essential_viz and essential_algos
    
    print("\n" + "=" * 50)
    if overall_success:
        print("🎉 INSTALLATION TEST PASSED!")
        print("The Procedural Maze Generator is ready to use.")
        print("\nTry running:")
        print("  maze-gen generate 10 10 --format ascii")
        return 0
    else:
        print("❌ INSTALLATION TEST FAILED!")
        print("Some components are not working properly.")
        print("Please check the error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
