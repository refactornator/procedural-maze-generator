#!/usr/bin/env python3
"""
Output Directory Management Demo

This example demonstrates the output directory management features
of the Procedural Maze Generator, including:
- Automatic directory structure creation
- File organization by algorithm and date
- Timestamped filenames
- Disk space monitoring
- Temporary file cleanup
"""

import os
import time
from pathlib import Path

from maze_generator import Maze
from maze_generator.algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
)
from maze_generator.algorithms.solvers import AStarSolver
from maze_generator.visualization import ImageExporter, AsciiRenderer
from maze_generator.utils.output_manager import OutputManager, OutputDirectoryError
from maze_generator.config import get_config


def demo_basic_output_management():
    """Demonstrate basic output directory management."""
    print("=== Basic Output Directory Management ===")
    
    # Create output manager with custom directory
    output_dir = Path.cwd() / "demo_output"
    manager = OutputManager(output_dir)
    
    print(f"Output directory: {manager.base_output_dir}")
    
    # Initialize directory structure
    if manager.initialize_output_structure():
        print("✓ Output directory structure created successfully")
    else:
        print("✗ Failed to create output directory structure")
        return
    
    # Show directory structure
    print("\nDirectory structure:")
    for root, dirs, files in os.walk(output_dir):
        level = root.replace(str(output_dir), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    # Check disk usage
    usage = manager.get_disk_usage()
    if usage:
        print(f"\nDisk usage:")
        print(f"  Total: {usage['total_gb']:.1f} GB")
        print(f"  Used:  {usage['used_gb']:.1f} GB ({usage['usage_percent']:.1f}%)")
        print(f"  Free:  {usage['free_gb']:.1f} GB")
    
    return manager


def demo_file_organization(manager):
    """Demonstrate different file organization methods."""
    print("\n=== File Organization Demo ===")
    
    # Create some sample mazes
    algorithms = {
        'dfs': DepthFirstSearchGenerator,
        'kruskal': KruskalGenerator,
        'prim': PrimGenerator,
    }
    
    exporter = ImageExporter(cell_size=20, wall_width=2)
    ascii_renderer = AsciiRenderer()
    
    for algo_name, generator_class in algorithms.items():
        print(f"\nGenerating maze with {algo_name.upper()} algorithm...")
        
        # Create and generate maze
        maze = Maze(10, 8)
        maze.set_start(0, 0)
        maze.set_end(9, 7)
        
        generator = generator_class(seed=42)
        generator.generate(maze)
        
        # Solve the maze
        solver = AStarSolver()
        solution = solver.solve(maze)
        
        # 1. Basic output path
        basic_path = manager.get_output_path(f"maze_{algo_name}.png", "images")
        exporter.export_png(maze, str(basic_path), show_solution=True, 
                           title=f"Maze - {algo_name.upper()}")
        print(f"  Basic output: {basic_path.relative_to(manager.base_output_dir)}")
        
        # 2. Organize by algorithm
        algo_path = manager.organize_by_algorithm(algo_name, f"maze_organized.png", "images")
        exporter.export_png(maze, str(algo_path), show_solution=True,
                           title=f"Organized Maze - {algo_name.upper()}")
        print(f"  By algorithm: {algo_path.relative_to(manager.base_output_dir)}")
        
        # 3. Timestamped filename
        timestamp_path = manager.get_timestamped_filename(f"maze_{algo_name}", "png", "images")
        exporter.export_png(maze, str(timestamp_path), show_solution=True,
                           title=f"Timestamped Maze - {algo_name.upper()}")
        print(f"  Timestamped:  {timestamp_path.relative_to(manager.base_output_dir)}")
        
        # 4. Auto-numbered filename
        auto_path = manager.get_auto_filename("maze", "png", "images")
        exporter.export_png(maze, str(auto_path), show_solution=True,
                           title=f"Auto-numbered Maze - {algo_name.upper()}")
        print(f"  Auto-numbered: {auto_path.relative_to(manager.base_output_dir)}")
        
        # 5. ASCII output organized by date
        ascii_path = manager.organize_by_date(f"maze_{algo_name}.txt", "ascii")
        ascii_renderer.save_to_file(maze, str(ascii_path), show_solution=True,
                                   title=f"ASCII Maze - {algo_name.upper()}")
        print(f"  ASCII by date: {ascii_path.relative_to(manager.base_output_dir)}")


def demo_temp_file_management(manager):
    """Demonstrate temporary file management."""
    print("\n=== Temporary File Management ===")
    
    temp_dir = manager.base_output_dir / "temp"
    
    # Create some temporary files
    temp_files = []
    for i in range(5):
        temp_file = temp_dir / f"temp_file_{i}.tmp"
        temp_file.write_text(f"Temporary content {i}")
        temp_files.append(temp_file)
        print(f"Created: {temp_file.name}")
    
    print(f"\nCreated {len(temp_files)} temporary files")
    
    # Make some files appear old
    old_time = time.time() - (25 * 3600)  # 25 hours ago
    for temp_file in temp_files[:2]:
        os.utime(temp_file, (old_time, old_time))
        print(f"Made old: {temp_file.name}")
    
    # Clean up old temp files
    cleaned = manager.cleanup_temp_files(max_age_hours=24)
    print(f"\nCleaned up {cleaned} old temporary files")
    
    # List remaining files
    remaining = list(temp_dir.glob("*.tmp"))
    print(f"Remaining temporary files: {len(remaining)}")


def demo_file_listing_and_stats(manager):
    """Demonstrate file listing and statistics."""
    print("\n=== File Listing and Statistics ===")
    
    # List all output files
    file_lists = manager.list_output_files()
    
    total_files = 0
    for file_type, files in file_lists.items():
        if files:
            print(f"\n{file_type.upper()} files ({len(files)}):")
            for file_path in files[:3]:  # Show first 3 files
                print(f"  - {file_path}")
            if len(files) > 3:
                print(f"  ... and {len(files) - 3} more")
            total_files += len(files)
    
    print(f"\nTotal files: {total_files}")
    
    # Directory size
    dir_size = manager.get_directory_size()
    print(f"Directory size: {dir_size / 1024:.1f} KB")
    
    # Check available space
    has_space = manager.check_available_space(10)  # 10 MB
    print(f"Has 10MB available space: {has_space}")


def demo_error_handling():
    """Demonstrate error handling for output directory issues."""
    print("\n=== Error Handling Demo ===")
    
    # Try to create output in a restricted location
    try:
        if os.name == 'posix':  # Unix-like systems
            restricted_path = Path("/root/restricted_output")
        else:  # Windows
            restricted_path = Path("C:\\Windows\\System32\\restricted_output")
        
        print(f"Attempting to create output directory at: {restricted_path}")
        manager = OutputManager(restricted_path)
        
        if manager.initialize_output_structure():
            print("✓ Unexpectedly succeeded")
        else:
            print("✗ Failed as expected (permission denied)")
            
    except OutputDirectoryError as e:
        print(f"✓ Caught expected error: {e}")
    except Exception as e:
        print(f"? Caught unexpected error: {e}")
    
    # Try with invalid path characters
    try:
        if os.name == 'nt':  # Windows
            invalid_path = Path("output<>:|?*")
        else:
            invalid_path = Path("output\x00invalid")
        
        print(f"\nAttempting invalid path: {invalid_path}")
        manager = OutputManager(invalid_path)
        
        if manager.initialize_output_structure():
            print("✓ Unexpectedly succeeded")
        else:
            print("✗ Failed as expected (invalid path)")
            
    except (OutputDirectoryError, OSError) as e:
        print(f"✓ Caught expected error: {e}")


def demo_configuration_integration():
    """Demonstrate integration with configuration system."""
    print("\n=== Configuration Integration ===")
    
    # Load configuration
    config = get_config()
    
    print(f"Default output directory: {config.export.output_directory}")
    print(f"Auto-create directories: {config.export.auto_create_directories}")
    print(f"Organize by algorithm: {config.export.organize_by_algorithm}")
    print(f"Organize by date: {config.export.organize_by_date}")
    print(f"Use timestamped filenames: {config.export.use_timestamped_filenames}")
    print(f"Cleanup temp files: {config.export.cleanup_temp_files}")
    print(f"Temp file max age: {config.export.temp_file_max_age_hours} hours")
    
    # Create manager using configuration
    config_manager = OutputManager(config.export.output_directory)
    
    if config.export.auto_create_directories:
        if config_manager.initialize_output_structure():
            print("✓ Directory structure created using configuration")
        else:
            print("✗ Failed to create directory structure")
    
    if config.export.cleanup_temp_files:
        cleaned = config_manager.cleanup_temp_files(config.export.temp_file_max_age_hours)
        print(f"Cleaned up {cleaned} temp files using configuration")


def main():
    """Run all output directory management demos."""
    print("Procedural Maze Generator - Output Directory Management Demo")
    print("=" * 65)
    
    try:
        # Basic output management
        manager = demo_basic_output_management()
        if not manager:
            return
        
        # File organization
        demo_file_organization(manager)
        
        # Temporary file management
        demo_temp_file_management(manager)
        
        # File listing and statistics
        demo_file_listing_and_stats(manager)
        
        # Error handling
        demo_error_handling()
        
        # Configuration integration
        demo_configuration_integration()
        
        print("\n" + "=" * 65)
        print("Demo completed successfully!")
        print(f"\nCheck the output directory: {manager.base_output_dir}")
        print("You can clean up by deleting the 'demo_output' directory.")
        
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
