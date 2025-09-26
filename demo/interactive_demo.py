#!/usr/bin/env python3
"""
Interactive CLI Demo for Procedural Maze Generator

This script provides an interactive demonstration of all the major features
of the procedural maze generator, including the new output directory management system.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Any


class MazeGeneratorDemo:
    """Interactive demo for the maze generator CLI."""
    
    def __init__(self):
        """Initialize the demo."""
        self.demo_dir = Path("demo_output")
        self.commands_run = []
        self.pause_between_commands = True
        
    def print_header(self, title: str) -> None:
        """Print a formatted header."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_step(self, step: str) -> None:
        """Print a demo step."""
        print(f"\n🔹 {step}")
    
    def run_command(self, command: str, description: str = "") -> bool:
        """Run a command and display the output."""
        if description:
            print(f"\n📝 {description}")
        
        print(f"💻 Running: {command}")
        
        if self.pause_between_commands:
            input("   Press Enter to continue...")
        
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                print("📤 Output:")
                print(result.stdout)
            
            if result.stderr and result.returncode != 0:
                print("⚠️  Error:")
                print(result.stderr)
                return False
            
            self.commands_run.append((command, result.returncode == 0))
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("⏰ Command timed out")
            return False
        except FileNotFoundError:
            print("❌ Command not found. Make sure 'maze-gen' is installed and in PATH")
            return False
    
    def demo_basic_generation(self) -> None:
        """Demo basic maze generation."""
        self.print_header("Basic Maze Generation")
        
        self.print_step("Generate a simple 10x8 maze using DFS algorithm")
        self.run_command(
            "maze-gen generate 10 8 --algorithm dfs --format ascii",
            "This creates a maze using Depth-First Search and displays it as ASCII art"
        )
        
        self.print_step("Generate a maze and save to file")
        self.run_command(
            f"maze-gen generate 15 10 --algorithm kruskal --format png --output {self.demo_dir}/basic_maze.png",
            "Save a Kruskal-generated maze as a PNG image"
        )
        
        self.print_step("Generate with custom start/end points")
        self.run_command(
            "maze-gen generate 12 8 --algorithm prim --start 0 0 --end 11 7 --format ascii",
            "Create a maze with specified start and end positions"
        )
    
    def demo_output_directory_management(self) -> None:
        """Demo output directory management features."""
        self.print_header("Output Directory Management")
        
        self.print_step("Initialize output directory structure")
        self.run_command(
            f"maze-gen output init --directory {self.demo_dir}",
            "Create organized directory structure for maze outputs"
        )
        
        self.print_step("Show output directory information")
        self.run_command(
            f"maze-gen output info --directory {self.demo_dir}",
            "Display directory statistics and configuration"
        )
        
        self.print_step("Generate mazes with organized output")
        algorithms = ["dfs", "kruskal", "prim"]
        
        for algo in algorithms:
            self.run_command(
                f"maze-gen generate 12 8 --algorithm {algo} --format png "
                f"--output-dir {self.demo_dir} --organize-by-algorithm",
                f"Generate {algo.upper()} maze organized by algorithm"
            )
        
        self.print_step("List generated files")
        self.run_command(
            f"maze-gen output list --directory {self.demo_dir} --type images",
            "Show all generated image files"
        )
    
    def demo_file_organization(self) -> None:
        """Demo different file organization options."""
        self.print_header("File Organization Options")
        
        self.print_step("Generate with timestamped filenames")
        self.run_command(
            f"maze-gen generate 10 6 --algorithm dfs --format png "
            f"--output-dir {self.demo_dir} --timestamped",
            "Create maze with timestamp in filename"
        )
        
        self.print_step("Generate organized by date")
        self.run_command(
            f"maze-gen generate 8 8 --algorithm kruskal --format ascii "
            f"--output-dir {self.demo_dir} --organize-by-date",
            "Organize output files by creation date"
        )
        
        self.print_step("Generate multiple formats")
        formats = ["png", "svg", "ascii"]
        for fmt in formats:
            self.run_command(
                f"maze-gen generate 10 8 --algorithm prim --format {fmt} "
                f"--output-dir {self.demo_dir}",
                f"Generate maze in {fmt.upper()} format"
            )
    
    def demo_maze_solving(self) -> None:
        """Demo maze solving capabilities."""
        self.print_header("Maze Solving")
        
        self.print_step("Generate and solve with A* algorithm")
        self.run_command(
            f"maze-gen solve 15 12 --gen-algorithm dfs --solve-algorithm astar "
            f"--format png --output-dir {self.demo_dir} --show-visited",
            "Create maze and solve it showing the solution path"
        )
        
        self.print_step("Compare different solving algorithms")
        solvers = ["astar", "dijkstra", "bfs"]
        
        for solver in solvers:
            self.run_command(
                f"maze-gen solve 10 8 --gen-algorithm kruskal --solve-algorithm {solver} "
                f"--format ascii --output-dir {self.demo_dir}",
                f"Solve maze using {solver.upper()} algorithm"
            )
    
    def demo_advanced_features(self) -> None:
        """Demo advanced features."""
        self.print_header("Advanced Features")
        
        self.print_step("Benchmark different algorithms")
        self.run_command(
            "maze-gen benchmark 15 15 --iterations 5",
            "Compare performance of different generation algorithms"
        )
        
        self.print_step("Generate large maze with custom settings")
        self.run_command(
            f"maze-gen generate 25 20 --algorithm wilson --format svg "
            f"--output-dir {self.demo_dir} --cell-size 15 --wall-width 1 "
            f"--title 'Large Wilson Maze'",
            "Create a large maze with custom visualization parameters"
        )
        
        self.print_step("Clean up temporary files")
        self.run_command(
            f"maze-gen output clean --directory {self.demo_dir} --temp-only",
            "Clean up temporary files while keeping generated mazes"
        )
    
    def demo_directory_exploration(self) -> None:
        """Show the generated directory structure."""
        self.print_header("Exploring Generated Files")
        
        self.print_step("Show final directory structure")
        if self.demo_dir.exists():
            print("📁 Directory structure:")
            self._show_directory_tree(self.demo_dir)
        
        self.print_step("List all generated files")
        self.run_command(
            f"maze-gen output list --directory {self.demo_dir}",
            "Show all files organized by type"
        )
        
        self.print_step("Show directory statistics")
        self.run_command(
            f"maze-gen output info --directory {self.demo_dir}",
            "Display final directory information"
        )
    
    def _show_directory_tree(self, path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> None:
        """Display directory tree structure."""
        if current_depth > max_depth:
            return
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and current_depth < max_depth:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    self._show_directory_tree(item, next_prefix, max_depth, current_depth + 1)
        except PermissionError:
            print(f"{prefix}└── [Permission Denied]")
    
    def run_full_demo(self) -> None:
        """Run the complete demo."""
        print("🎯 Procedural Maze Generator - Interactive Demo")
        print("=" * 60)
        print("This demo will showcase all major features of the maze generator,")
        print("including the new output directory management system.")
        print("\nThe demo will:")
        print("• Generate mazes with different algorithms")
        print("• Demonstrate output directory management")
        print("• Show file organization options")
        print("• Solve mazes with various algorithms")
        print("• Display advanced features")
        
        response = input("\nWould you like to run with pauses between commands? (y/N): ")
        self.pause_between_commands = response.lower() in ['y', 'yes']
        
        print(f"\n📂 Demo files will be saved to: {self.demo_dir.absolute()}")
        
        try:
            # Run all demo sections
            self.demo_basic_generation()
            self.demo_output_directory_management()
            self.demo_file_organization()
            self.demo_maze_solving()
            self.demo_advanced_features()
            self.demo_directory_exploration()
            
            # Summary
            self.print_header("Demo Complete!")
            
            successful_commands = sum(1 for _, success in self.commands_run if success)
            total_commands = len(self.commands_run)
            
            print(f"✅ Successfully executed {successful_commands}/{total_commands} commands")
            print(f"📁 Generated files are available in: {self.demo_dir.absolute()}")
            print("\n🎉 Thank you for trying the Procedural Maze Generator!")
            print("Visit https://github.com/yourusername/procedural-maze-generator for more information.")
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Demo interrupted by user")
            print("Generated files are still available in the demo directory.")
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
            print("Please check that the maze generator is properly installed.")
    
    def run_quick_demo(self) -> None:
        """Run a quick demo without pauses."""
        self.pause_between_commands = False
        print("🚀 Running Quick Demo (no pauses)")
        
        # Just run a few key commands
        self.run_command(f"maze-gen output init --directory {self.demo_dir}")
        self.run_command("maze-gen generate 12 8 --algorithm dfs --format ascii")
        self.run_command(f"maze-gen generate 10 8 --algorithm kruskal --format png --output-dir {self.demo_dir}")
        self.run_command(f"maze-gen solve 8 6 --gen-algorithm prim --solve-algorithm astar --format ascii")
        self.run_command(f"maze-gen output info --directory {self.demo_dir}")
        
        print("\n✅ Quick demo complete!")


def main():
    """Main demo function."""
    demo = MazeGeneratorDemo()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        demo.run_quick_demo()
    else:
        demo.run_full_demo()


if __name__ == "__main__":
    main()
