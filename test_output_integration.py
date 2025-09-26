#!/usr/bin/env python3
"""
Test script to verify output directory integration works correctly.

This script tests the complete integration of the output directory management
system with the CLI and configuration.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_output_manager_basic():
    """Test basic output manager functionality."""
    print("Testing OutputManager basic functionality...")
    
    try:
        from maze_generator.utils.output_manager import OutputManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = OutputManager(Path(temp_dir) / "test_output")
            
            # Test initialization
            result = manager.initialize_output_structure()
            assert result, "Failed to initialize output structure"
            
            # Test directory creation
            assert manager.base_output_dir.exists(), "Base directory not created"
            
            # Test subdirectories
            for subdir in manager.subdirs.values():
                subdir_path = manager.base_output_dir / subdir
                assert subdir_path.exists(), f"Subdirectory {subdir} not created"
            
            # Test file path generation
            path = manager.get_output_path("test.png", "images")
            expected = manager.base_output_dir / "images" / "test.png"
            assert path == expected, f"Unexpected path: {path}"
            
            print("✓ OutputManager basic functionality works")
            return True
            
    except Exception as e:
        print(f"✗ OutputManager test failed: {e}")
        return False


def test_cli_integration():
    """Test CLI integration with output management."""
    print("Testing CLI integration...")
    
    try:
        from maze_generator.cli import MazeGeneratorCLI
        
        cli = MazeGeneratorCLI()
        
        # Test that CLI has output manager attribute
        assert hasattr(cli, 'output_manager'), "CLI missing output_manager attribute"
        
        # Test parser creation (should not raise exceptions)
        parser = cli.create_parser()
        assert parser is not None, "Failed to create parser"
        
        # Test that output command exists
        help_text = parser.format_help()
        assert 'output' in help_text, "Output command not found in help"
        
        print("✓ CLI integration works")
        return True
        
    except Exception as e:
        print(f"✗ CLI integration test failed: {e}")
        return False


def test_configuration_integration():
    """Test configuration integration."""
    print("Testing configuration integration...")
    
    try:
        from maze_generator.config import get_config
        
        config = get_config()
        
        # Test that export config has output directory settings
        assert hasattr(config.export, 'output_directory'), "Missing output_directory config"
        assert hasattr(config.export, 'organize_by_algorithm'), "Missing organize_by_algorithm config"
        assert hasattr(config.export, 'organize_by_date'), "Missing organize_by_date config"
        assert hasattr(config.export, 'auto_create_directories'), "Missing auto_create_directories config"
        
        # Test default values
        assert config.export.output_directory == 'output', "Unexpected default output directory"
        assert isinstance(config.export.organize_by_algorithm, bool), "organize_by_algorithm should be bool"
        
        print("✓ Configuration integration works")
        return True
        
    except Exception as e:
        print(f"✗ Configuration integration test failed: {e}")
        return False


def test_end_to_end_generation():
    """Test end-to-end maze generation with output management."""
    print("Testing end-to-end generation with output management...")
    
    try:
        from maze_generator import Maze
        from maze_generator.algorithms.generators import DepthFirstSearchGenerator
        from maze_generator.algorithms.solvers import AStarSolver
        from maze_generator.visualization import ImageExporter
        from maze_generator.utils.output_manager import OutputManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create output manager
            manager = OutputManager(Path(temp_dir) / "test_output")
            manager.initialize_output_structure()
            
            # Create and generate maze
            maze = Maze(5, 5)
            maze.set_start(0, 0)
            maze.set_end(4, 4)
            
            generator = DepthFirstSearchGenerator(seed=42)
            generator.generate(maze)
            
            # Solve maze
            solver = AStarSolver()
            solution = solver.solve(maze)
            assert len(solution) > 0, "No solution found"
            
            # Export using output manager
            exporter = ImageExporter(cell_size=20, wall_width=2)
            output_path = manager.get_output_path("test_maze.png", "images")
            
            exporter.export_png(maze, str(output_path), show_solution=True, title="Test Maze")
            
            # Verify file was created
            assert output_path.exists(), f"Output file not created: {output_path}"
            assert output_path.stat().st_size > 0, "Output file is empty"
            
            print("✓ End-to-end generation with output management works")
            return True
            
    except Exception as e:
        print(f"✗ End-to-end test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cli_output_commands():
    """Test CLI output management commands."""
    print("Testing CLI output commands...")
    
    try:
        from maze_generator.cli import MazeGeneratorCLI
        
        cli = MazeGeneratorCLI()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "cli_test_output"
            
            # Test output init command
            args = ['output', 'init', '--directory', str(output_dir)]
            
            # Parse arguments
            parser = cli.create_parser()
            parsed_args = parser.parse_args(args)
            
            # Run command
            cli.manage_output_directory(parsed_args)
            
            # Verify directory was created
            assert output_dir.exists(), "Output directory not created by CLI"
            
            # Verify subdirectories exist
            subdirs = ['images', 'ascii', 'svg', 'animations', 'benchmarks', 'temp']
            for subdir in subdirs:
                subdir_path = output_dir / subdir
                assert subdir_path.exists(), f"Subdirectory {subdir} not created"
            
            print("✓ CLI output commands work")
            return True
            
    except Exception as e:
        print(f"✗ CLI output commands test failed: {e}")
        return False


def main():
    """Run all integration tests."""
    print("Output Directory Integration Test")
    print("=" * 40)
    
    tests = [
        ("OutputManager Basic", test_output_manager_basic),
        ("CLI Integration", test_cli_integration),
        ("Configuration Integration", test_configuration_integration),
        ("End-to-End Generation", test_end_to_end_generation),
        ("CLI Output Commands", test_cli_output_commands),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:25} | {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 All integration tests passed!")
        print("Output directory management is working correctly.")
        return 0
    else:
        print(f"\n❌ {len(results) - passed} tests failed!")
        print("There are issues with the output directory integration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
