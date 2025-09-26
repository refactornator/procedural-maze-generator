#!/usr/bin/env python3
"""
Test script to verify that core functionality works without optional dependencies.

This script tests that the maze generator can work with minimal dependencies,
which is important for CI environments and users who don't need all features.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_core_imports():
    """Test that core modules can be imported."""
    print("Testing core imports...")
    
    try:
        from maze_generator import Maze, Cell, Direction
        print("✅ Core maze classes imported successfully")
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False
    
    try:
        from maze_generator.algorithms.generators import DepthFirstSearchGenerator
        from maze_generator.algorithms.solvers import AStarSolver
        print("✅ Core algorithms imported successfully")
    except ImportError as e:
        print(f"❌ Algorithm import failed: {e}")
        return False
    
    try:
        from maze_generator.visualization import AsciiRenderer
        print("✅ ASCII renderer imported successfully")
    except ImportError as e:
        print(f"❌ ASCII renderer import failed: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic maze generation and solving without optional dependencies."""
    print("Testing basic functionality...")
    
    try:
        from maze_generator import Maze
        from maze_generator.algorithms.generators import DepthFirstSearchGenerator
        from maze_generator.algorithms.solvers import AStarSolver
        from maze_generator.visualization import AsciiRenderer
        
        # Create a small maze
        maze = Maze(5, 5)
        maze.set_start(0, 0)
        maze.set_end(4, 4)
        
        # Generate maze
        generator = DepthFirstSearchGenerator(seed=42)
        generator.generate(maze)
        print("✅ Maze generation successful")
        
        # Solve maze
        solver = AStarSolver()
        solution = solver.solve(maze)
        print(f"✅ Maze solving successful (solution length: {len(solution)})")
        
        # Render as ASCII
        renderer = AsciiRenderer()
        ascii_output = renderer.render_compact(maze, show_solution=True)
        print("✅ ASCII rendering successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_optional_imports():
    """Test optional imports and report what's available."""
    print("Testing optional imports...")
    
    optional_modules = [
        ("matplotlib", "maze_generator.visualization.matplotlib_renderer", "MatplotlibRenderer"),
        ("PIL", "maze_generator.visualization.image_exporter", "ImageExporter"),
        ("pygame", "maze_generator.visualization.pygame_renderer", "PygameRenderer"),
    ]
    
    available = []
    missing = []
    
    for dep_name, module_path, class_name in optional_modules:
        try:
            module_parts = module_path.split('.')
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            available.append(dep_name)
            print(f"✅ {dep_name} available")
        except ImportError:
            missing.append(dep_name)
            print(f"⚠️  {dep_name} not available (optional)")
    
    print(f"\nSummary: {len(available)} optional dependencies available, {len(missing)} missing")
    return True


def test_cli_entry_point():
    """Test that the CLI entry point is properly installed."""
    print("Testing CLI entry point...")
    
    try:
        from maze_generator.cli import MazeGeneratorCLI
        cli = MazeGeneratorCLI()
        print("✅ CLI class imported successfully")
        
        # Test parser creation
        parser = cli.create_parser()
        print("✅ CLI parser created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False


def main():
    """Run all minimal import tests."""
    print("🧪 Minimal Import Test Suite")
    print("=" * 40)
    print("Testing that core functionality works without optional dependencies")
    print()
    
    tests = [
        ("Core Imports", test_core_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Optional Imports", test_optional_imports),
        ("CLI Entry Point", test_cli_entry_point),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} | {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n✅ All tests passed! Core functionality works without optional dependencies.")
        return 0
    else:
        print(f"\n❌ {len(results) - passed} tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
