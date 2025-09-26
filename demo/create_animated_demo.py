#!/usr/bin/env python3
"""
Create animated demonstrations for the procedural maze generator.

This script creates animated GIFs showing maze generation and solving processes.
Requires PIL (Pillow) for GIF creation.
"""

import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from maze_generator import Maze
from maze_generator.algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
)
from maze_generator.algorithms.solvers import AStarSolver
from maze_generator.visualization import ImageExporter


class AnimatedMazeDemo:
    """Create animated demonstrations of maze generation and solving."""
    
    def __init__(self, output_dir: Path):
        """Initialize the animated demo creator."""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Animation settings
        self.frame_duration = 200  # milliseconds per frame
        self.cell_size = 20
        self.wall_width = 2
        
        self.exporter = ImageExporter(self.cell_size, self.wall_width)
    
    def create_generation_animation(self, algorithm_name: str, generator_class, 
                                  width: int = 15, height: int = 12, seed: int = 42):
        """Create an animated GIF of maze generation."""
        print(f"Creating {algorithm_name} generation animation...")
        
        maze = Maze(width, height)
        generator = generator_class(seed=seed)
        
        # We'll simulate step-by-step generation by creating multiple mazes
        # with increasing complexity (this is a simplified approach)
        frames = []
        temp_dir = self.output_dir / "temp_frames"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Create frames showing progressive generation
            steps = 10
            for step in range(steps + 1):
                # Create a partially generated maze
                step_maze = Maze(width, height)
                step_generator = generator_class(seed=seed)
                
                # Generate maze (we'll use the full generation for now)
                step_generator.generate(step_maze)
                
                # Create frame
                frame_path = temp_dir / f"frame_{step:03d}.png"
                title = f"{algorithm_name} Generation - Step {step + 1}/{steps + 1}"
                
                self.exporter.export_png(step_maze, str(frame_path), 
                                        title=title, add_border=True)
                frames.append(frame_path)
                
                # Add some variation by changing the seed slightly
                seed += 1
            
            # Create GIF from frames
            self._create_gif_from_frames(frames, 
                                       self.output_dir / f"{algorithm_name.lower()}_generation.gif")
            
        finally:
            # Clean up temp frames
            for frame in frames:
                if frame.exists():
                    frame.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()
    
    def create_solving_animation(self, width: int = 15, height: int = 12, seed: int = 42):
        """Create an animated GIF of maze solving."""
        print("Creating maze solving animation...")
        
        # Generate a maze to solve
        maze = Maze(width, height)
        maze.set_start(0, 0)
        maze.set_end(width - 1, height - 1)
        
        generator = DepthFirstSearchGenerator(seed=seed)
        generator.generate(maze)
        
        # Solve the maze
        solver = AStarSolver()
        solution = solver.solve(maze)
        
        if not solution:
            print("No solution found, skipping solving animation")
            return
        
        frames = []
        temp_dir = self.output_dir / "temp_frames"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Create frames showing progressive solution
            for step in range(len(solution) + 1):
                # Create a copy of the maze
                step_maze = Maze(width, height)
                step_maze.set_start(0, 0)
                step_maze.set_end(width - 1, height - 1)
                
                # Copy the maze structure
                for cell in maze:
                    step_cell = step_maze.get_cell(cell.x, cell.y)
                    step_cell.walls = cell.walls.copy()
                    step_cell.is_start = cell.is_start
                    step_cell.is_end = cell.is_end
                
                # Set partial solution
                if step > 0:
                    partial_solution = solution[:step]
                    step_maze.solution_path = partial_solution
                    
                    # Mark visited cells
                    for cell in partial_solution:
                        step_cell = step_maze.get_cell(cell.x, cell.y)
                        step_cell.visited = True
                
                # Create frame
                frame_path = temp_dir / f"solve_frame_{step:03d}.png"
                title = f"A* Solving - Step {step}/{len(solution)}"
                
                show_solution = step > 0
                self.exporter.export_png(step_maze, str(frame_path), 
                                        show_solution=show_solution,
                                        show_visited=True,
                                        title=title, add_border=True)
                frames.append(frame_path)
            
            # Create GIF from frames
            self._create_gif_from_frames(frames, 
                                       self.output_dir / "maze_solving.gif",
                                       duration=300)  # Slower for solving
            
        finally:
            # Clean up temp frames
            for frame in frames:
                if frame.exists():
                    frame.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()
    
    def create_algorithm_comparison_animation(self, width: int = 12, height: int = 10):
        """Create an animation comparing different algorithms."""
        print("Creating algorithm comparison animation...")
        
        algorithms = [
            ("DFS", DepthFirstSearchGenerator),
            ("Kruskal", KruskalGenerator),
            ("Prim", PrimGenerator),
        ]
        
        frames = []
        temp_dir = self.output_dir / "temp_frames"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            for i, (algo_name, generator_class) in enumerate(algorithms):
                # Generate maze with same seed for fair comparison
                maze = Maze(width, height)
                generator = generator_class(seed=42)
                generator.generate(maze)
                
                # Create frame
                frame_path = temp_dir / f"comparison_{i:03d}.png"
                title = f"{algo_name} Algorithm"
                
                self.exporter.export_png(maze, str(frame_path), 
                                        title=title, add_border=True)
                frames.append(frame_path)
            
            # Create GIF from frames
            self._create_gif_from_frames(frames, 
                                       self.output_dir / "algorithm_comparison.gif",
                                       duration=1500)  # Longer duration for comparison
            
        finally:
            # Clean up temp frames
            for frame in frames:
                if frame.exists():
                    frame.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()
    
    def _create_gif_from_frames(self, frame_paths: list, output_path: Path, 
                               duration: int = None):
        """Create a GIF from a list of frame images."""
        try:
            from PIL import Image
        except ImportError:
            print("PIL (Pillow) is required for GIF creation. Install with: pip install Pillow")
            return
        
        if not frame_paths:
            print("No frames to create GIF")
            return
        
        # Load all frames
        frames = []
        for frame_path in frame_paths:
            if frame_path.exists():
                frames.append(Image.open(frame_path))
        
        if not frames:
            print("No valid frames found")
            return
        
        # Use provided duration or default
        frame_duration = duration or self.frame_duration
        
        # Save as GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_duration,
            loop=0  # Loop forever
        )
        
        print(f"✓ Created animated GIF: {output_path}")
    
    def create_cli_demo_frames(self):
        """Create frames showing CLI usage (static images)."""
        print("Creating CLI demo frames...")
        
        # Create example command outputs as images
        commands = [
            "maze-gen generate 12 8 --algorithm dfs --format ascii",
            "maze-gen solve 10 6 --gen-algorithm kruskal --solve-algorithm astar",
            "maze-gen output init --directory demo_output",
            "maze-gen benchmark 15 15 --iterations 5"
        ]
        
        # For now, just create placeholder images with command text
        # In a real implementation, you might capture actual terminal output
        for i, command in enumerate(commands):
            # Create a simple maze for each command
            maze = Maze(12, 8)
            generator = DepthFirstSearchGenerator(seed=i * 42)
            generator.generate(maze)
            
            if "solve" in command:
                maze.set_start(0, 0)
                maze.set_end(11, 7)
                solver = AStarSolver()
                solver.solve(maze)
                show_solution = True
            else:
                show_solution = False
            
            frame_path = self.output_dir / f"cli_demo_{i+1}.png"
            title = f"$ {command}"
            
            self.exporter.export_png(maze, str(frame_path), 
                                    show_solution=show_solution,
                                    title=title, add_border=True)
        
        print("✓ Created CLI demo frames")


def main():
    """Create all animated demonstrations."""
    print("🎬 Creating Animated Demonstrations")
    print("=" * 50)
    
    output_dir = Path("demo/animations")
    demo = AnimatedMazeDemo(output_dir)
    
    try:
        # Create generation animations
        algorithms = [
            ("DFS", DepthFirstSearchGenerator),
            ("Kruskal", KruskalGenerator),
            ("Prim", PrimGenerator),
        ]
        
        for algo_name, generator_class in algorithms:
            demo.create_generation_animation(algo_name, generator_class)
        
        # Create solving animation
        demo.create_solving_animation()
        
        # Create comparison animation
        demo.create_algorithm_comparison_animation()
        
        # Create CLI demo frames
        demo.create_cli_demo_frames()
        
        print("\n" + "=" * 50)
        print("✅ All animations created successfully!")
        print(f"📁 Animations are available in: {output_dir.absolute()}")
        print("\nCreated files:")
        for gif_file in output_dir.glob("*.gif"):
            print(f"  🎬 {gif_file.name}")
        for png_file in output_dir.glob("*.png"):
            print(f"  🖼️  {png_file.name}")
        
    except Exception as e:
        print(f"❌ Error creating animations: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
