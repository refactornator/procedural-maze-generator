"""Command line interface for the maze generator."""

import argparse
import sys
import os
from typing import Optional, Dict, Any
import random

from .maze import Maze
from .algorithms.generators import (
    DepthFirstSearchGenerator,
    KruskalGenerator,
    PrimGenerator,
    WilsonGenerator,
)
from .algorithms.solvers import (
    AStarSolver,
    DijkstraSolver,
    BreadthFirstSearchSolver,
    DepthFirstSearchSolver,
    WallFollowerSolver,
)
from .visualization.matplotlib_renderer import MatplotlibRenderer
from .visualization.ascii_renderer import AsciiRenderer
from .visualization.pygame_renderer import PygameRenderer
from .visualization.image_exporter import ImageExporter
from .utils.output_manager import OutputManager, OutputDirectoryError
from .config import get_config


class MazeGeneratorCLI:
    """Command line interface for maze generation and solving."""

    def __init__(self):
        """Initialize the CLI."""
        self.generators = {
            'dfs': DepthFirstSearchGenerator,
            'depth-first': DepthFirstSearchGenerator,
            'kruskal': KruskalGenerator,
            'prim': PrimGenerator,
            'wilson': WilsonGenerator,
        }

        self.solvers = {
            'astar': AStarSolver,
            'a-star': AStarSolver,
            'dijkstra': DijkstraSolver,
            'bfs': BreadthFirstSearchSolver,
            'breadth-first': BreadthFirstSearchSolver,
            'dfs': DepthFirstSearchSolver,
            'depth-first': DepthFirstSearchSolver,
            'wall-follower': WallFollowerSolver,
        }

        # Load configuration
        self.config = get_config()

        # Initialize output manager
        self.output_manager = None

    def create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description='Generate and solve mazes using various algorithms',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s generate 20 20 --algorithm dfs --output maze.png
  %(prog)s generate 30 30 --algorithm kruskal --format ascii
  %(prog)s solve maze.png --algorithm astar --output solution.png
  %(prog)s interactive 25 25 --algorithm prim
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Generate command
        gen_parser = subparsers.add_parser('generate', help='Generate a new maze')
        gen_parser.add_argument('width', type=int, help='Maze width')
        gen_parser.add_argument('height', type=int, help='Maze height')
        gen_parser.add_argument('--algorithm', '-a', choices=list(self.generators.keys()),
                               default='dfs', help='Generation algorithm (default: dfs)')
        gen_parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible mazes')
        gen_parser.add_argument('--output', '-o', help='Output file path')
        gen_parser.add_argument('--format', '-f', choices=['png', 'jpg', 'svg', 'ascii', 'matplotlib'],
                               default='ascii', help='Output format (default: ascii)')
        gen_parser.add_argument('--cell-size', type=int, default=20, help='Cell size in pixels (default: 20)')
        gen_parser.add_argument('--wall-width', type=int, default=2, help='Wall width in pixels (default: 2)')
        gen_parser.add_argument('--title', help='Title for the maze')
        gen_parser.add_argument('--start', nargs=2, type=int, metavar=('X', 'Y'),
                               help='Start position (default: top-left)')
        gen_parser.add_argument('--end', nargs=2, type=int, metavar=('X', 'Y'),
                               help='End position (default: bottom-right)')
        gen_parser.add_argument('--output-dir', help='Output directory path (default: output)')
        gen_parser.add_argument('--organize-by-algorithm', action='store_true',
                               help='Organize output files by algorithm')
        gen_parser.add_argument('--organize-by-date', action='store_true',
                               help='Organize output files by date')
        gen_parser.add_argument('--timestamped', action='store_true',
                               help='Use timestamped filenames')
        
        # Solve command
        solve_parser = subparsers.add_parser('solve', help='Solve an existing maze')
        solve_parser.add_argument('width', type=int, help='Maze width')
        solve_parser.add_argument('height', type=int, help='Maze height')
        solve_parser.add_argument('--gen-algorithm', choices=list(self.generators.keys()),
                                 default='dfs', help='Generation algorithm (default: dfs)')
        solve_parser.add_argument('--solve-algorithm', choices=list(self.solvers.keys()),
                                 default='astar', help='Solving algorithm (default: astar)')
        solve_parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible mazes')
        solve_parser.add_argument('--output', '-o', help='Output file path')
        solve_parser.add_argument('--format', '-f', choices=['png', 'jpg', 'svg', 'ascii', 'matplotlib'],
                                 default='ascii', help='Output format (default: ascii)')
        solve_parser.add_argument('--cell-size', type=int, default=20, help='Cell size in pixels (default: 20)')
        solve_parser.add_argument('--wall-width', type=int, default=2, help='Wall width in pixels (default: 2)')
        solve_parser.add_argument('--title', help='Title for the maze')
        solve_parser.add_argument('--start', nargs=2, type=int, metavar=('X', 'Y'),
                                 help='Start position (default: top-left)')
        solve_parser.add_argument('--end', nargs=2, type=int, metavar=('X', 'Y'),
                                 help='End position (default: bottom-right)')
        solve_parser.add_argument('--show-visited', action='store_true',
                                 help='Show visited cells during solving')
        solve_parser.add_argument('--output-dir', help='Output directory path (default: output)')
        solve_parser.add_argument('--organize-by-algorithm', action='store_true',
                                 help='Organize output files by algorithm')
        solve_parser.add_argument('--organize-by-date', action='store_true',
                                 help='Organize output files by date')
        solve_parser.add_argument('--timestamped', action='store_true',
                                 help='Use timestamped filenames')
        
        # Interactive command
        interactive_parser = subparsers.add_parser('interactive', help='Interactive maze visualization')
        interactive_parser.add_argument('width', type=int, help='Maze width')
        interactive_parser.add_argument('height', type=int, help='Maze height')
        interactive_parser.add_argument('--algorithm', '-a', choices=list(self.generators.keys()),
                                       default='dfs', help='Generation algorithm (default: dfs)')
        interactive_parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible mazes')
        interactive_parser.add_argument('--cell-size', type=int, default=20, help='Cell size in pixels (default: 20)')
        interactive_parser.add_argument('--wall-width', type=int, default=2, help='Wall width in pixels (default: 2)')
        
        # Benchmark command
        benchmark_parser = subparsers.add_parser('benchmark', help='Benchmark algorithms')
        benchmark_parser.add_argument('width', type=int, help='Maze width')
        benchmark_parser.add_argument('height', type=int, help='Maze height')
        benchmark_parser.add_argument('--iterations', '-i', type=int, default=10,
                                     help='Number of iterations (default: 10)')
        benchmark_parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible results')

        # Output management command
        output_parser = subparsers.add_parser('output', help='Manage output directories')
        output_subparsers = output_parser.add_subparsers(dest='output_command', help='Output management commands')

        # Initialize output directory
        init_parser = output_subparsers.add_parser('init', help='Initialize output directory structure')
        init_parser.add_argument('--directory', '-d', help='Output directory path (default: output)')

        # List output files
        list_parser = output_subparsers.add_parser('list', help='List output files')
        list_parser.add_argument('--directory', '-d', help='Output directory path (default: output)')
        list_parser.add_argument('--type', '-t', choices=['images', 'ascii', 'svg', 'animations', 'benchmarks'],
                                help='File type to list (default: all)')

        # Clean output directory
        clean_parser = output_subparsers.add_parser('clean', help='Clean output directory')
        clean_parser.add_argument('--directory', '-d', help='Output directory path (default: output)')
        clean_parser.add_argument('--temp-only', action='store_true', help='Clean only temporary files')
        clean_parser.add_argument('--max-age', type=int, default=24, help='Maximum age in hours for temp files')

        # Show output directory info
        info_parser = output_subparsers.add_parser('info', help='Show output directory information')
        info_parser.add_argument('--directory', '-d', help='Output directory path (default: output)')
        
        return parser

    def _initialize_output_manager(self, args: argparse.Namespace) -> bool:
        """
        Initialize the output manager based on arguments and configuration.

        Args:
            args: Parsed command line arguments.

        Returns:
            bool: True if successful, False otherwise.
        """
        # Determine output directory
        output_dir = None
        if hasattr(args, 'output_dir') and args.output_dir:
            output_dir = args.output_dir
        else:
            output_dir = self.config.export.output_directory

        try:
            self.output_manager = OutputManager(output_dir)

            # Initialize directory structure if auto-create is enabled
            if self.config.export.auto_create_directories:
                if not self.output_manager.initialize_output_structure():
                    print(f"Warning: Could not initialize output directory structure")
                    return False

            # Check available disk space
            if not self.output_manager.check_available_space(100):  # 100MB minimum
                print("Warning: Low disk space available")

            # Clean up temp files if enabled
            if self.config.export.cleanup_temp_files:
                cleaned = self.output_manager.cleanup_temp_files(
                    self.config.export.temp_file_max_age_hours
                )
                if cleaned > 0:
                    print(f"Cleaned up {cleaned} temporary files")

            return True

        except OutputDirectoryError as e:
            print(f"Error: Failed to initialize output directory: {e}")
            print("Try specifying a different output directory with --output-dir")
            return False

    def generate_maze(self, args: argparse.Namespace) -> None:
        """Generate a maze based on command line arguments."""
        # Create maze
        maze = Maze(args.width, args.height)
        
        # Set random seed if provided
        if args.seed is not None:
            random.seed(args.seed)
        
        # Set start and end positions
        start_x, start_y = args.start if args.start else (0, 0)
        end_x, end_y = args.end if args.end else (args.width - 1, args.height - 1)
        
        if not maze.set_start(start_x, start_y):
            print(f"Error: Invalid start position ({start_x}, {start_y})")
            return
        
        if not maze.set_end(end_x, end_y):
            print(f"Error: Invalid end position ({end_x}, {end_y})")
            return
        
        # Generate maze
        generator_class = self.generators[args.algorithm]
        generator = generator_class(seed=args.seed)
        generator.generate(maze)
        
        # Output maze
        self._output_maze(maze, args, show_solution=False)

    def solve_maze(self, args: argparse.Namespace) -> None:
        """Generate and solve a maze based on command line arguments."""
        # Create and generate maze
        maze = Maze(args.width, args.height)
        
        # Set random seed if provided
        if args.seed is not None:
            random.seed(args.seed)
        
        # Set start and end positions
        start_x, start_y = args.start if args.start else (0, 0)
        end_x, end_y = args.end if args.end else (args.width - 1, args.height - 1)
        
        maze.set_start(start_x, start_y)
        maze.set_end(end_x, end_y)
        
        # Generate maze
        generator_class = self.generators[args.gen_algorithm]
        generator = generator_class(seed=args.seed)
        generator.generate(maze)
        
        # Solve maze
        solver_class = self.solvers[args.solve_algorithm]
        solver = solver_class()
        solution = solver.solve(maze)
        
        if solution:
            print(f"Solution found with {len(solution)} steps using {args.solve_algorithm}")
        else:
            print(f"No solution found using {args.solve_algorithm}")
        
        # Output maze with solution
        self._output_maze(maze, args, show_solution=bool(solution), 
                         show_visited=args.show_visited)

    def interactive_mode(self, args: argparse.Namespace) -> None:
        """Run interactive maze visualization."""
        try:
            # Create maze
            maze = Maze(args.width, args.height)
            
            # Set random seed if provided
            if args.seed is not None:
                random.seed(args.seed)
            
            # Set default start and end positions
            maze.set_start(0, 0)
            maze.set_end(args.width - 1, args.height - 1)
            
            # Generate maze
            generator_class = self.generators[args.algorithm]
            generator = generator_class(seed=args.seed)
            generator.generate(maze)
            
            # Show interactive visualization
            renderer = PygameRenderer(args.cell_size, args.wall_width)
            renderer.show_static(maze, title=f"Interactive Maze ({args.algorithm})")
            
        except ImportError:
            print("Error: pygame is required for interactive mode")
            print("Install it with: pip install pygame")
        except Exception as e:
            print(f"Error in interactive mode: {e}")

    def benchmark_algorithms(self, args: argparse.Namespace) -> None:
        """Benchmark different algorithms."""
        import time
        
        print(f"Benchmarking algorithms on {args.width}x{args.height} maze")
        print(f"Iterations: {args.iterations}")
        print("-" * 50)
        
        # Set random seed if provided
        if args.seed is not None:
            random.seed(args.seed)
        
        results = {}
        
        for name, generator_class in self.generators.items():
            times = []
            
            for i in range(args.iterations):
                maze = Maze(args.width, args.height)
                generator = generator_class()
                
                start_time = time.time()
                generator.generate(maze)
                end_time = time.time()
                
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            results[name] = {
                'avg': avg_time,
                'min': min_time,
                'max': max_time
            }
            
            print(f"{name:15} | Avg: {avg_time:.4f}s | Min: {min_time:.4f}s | Max: {max_time:.4f}s")
        
        # Find fastest algorithm
        fastest = min(results.items(), key=lambda x: x[1]['avg'])
        print("-" * 50)
        print(f"Fastest algorithm: {fastest[0]} ({fastest[1]['avg']:.4f}s average)")

    def manage_output_directory(self, args: argparse.Namespace) -> None:
        """Handle output directory management commands."""
        if not args.output_command:
            print("Error: No output management command specified")
            return

        # Get output directory
        output_dir = args.directory if hasattr(args, 'directory') and args.directory else self.config.export.output_directory

        try:
            manager = OutputManager(output_dir)

            if args.output_command == 'init':
                self._init_output_directory(manager)
            elif args.output_command == 'list':
                self._list_output_files(manager, getattr(args, 'type', None))
            elif args.output_command == 'clean':
                self._clean_output_directory(manager, args)
            elif args.output_command == 'info':
                self._show_output_info(manager)

        except OutputDirectoryError as e:
            print(f"Error: {e}")

    def _init_output_directory(self, manager: OutputManager) -> None:
        """Initialize output directory structure."""
        print(f"Initializing output directory: {manager.base_output_dir}")

        if manager.initialize_output_structure():
            print("✓ Output directory structure created successfully")

            # Show created structure
            print("\nCreated directories:")
            for subdir_name in manager.subdirs.values():
                subdir_path = manager.base_output_dir / subdir_name
                if subdir_path.exists():
                    print(f"  - {subdir_name}/")
        else:
            print("✗ Failed to create output directory structure")

    def _list_output_files(self, manager: OutputManager, file_type: Optional[str] = None) -> None:
        """List files in output directory."""
        print(f"Output directory: {manager.base_output_dir}")

        if not manager.base_output_dir.exists():
            print("Output directory does not exist. Run 'maze-gen output init' to create it.")
            return

        file_lists = manager.list_output_files(file_type)
        total_files = 0

        for category, files in file_lists.items():
            if files:
                print(f"\n{category.upper()} ({len(files)} files):")
                for file_path in files:
                    print(f"  {file_path}")
                total_files += len(files)

        if total_files == 0:
            print("\nNo files found in output directory.")
        else:
            print(f"\nTotal files: {total_files}")

            # Show directory size
            size_bytes = manager.get_directory_size()
            if size_bytes > 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            elif size_bytes > 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes} bytes"
            print(f"Directory size: {size_str}")

    def _clean_output_directory(self, manager: OutputManager, args: argparse.Namespace) -> None:
        """Clean output directory."""
        print(f"Cleaning output directory: {manager.base_output_dir}")

        if not manager.base_output_dir.exists():
            print("Output directory does not exist.")
            return

        if args.temp_only:
            # Clean only temporary files
            cleaned = manager.cleanup_temp_files(args.max_age)
            print(f"Cleaned up {cleaned} temporary files older than {args.max_age} hours")
        else:
            # Ask for confirmation before cleaning all files
            response = input("This will delete ALL files in the output directory. Continue? (y/N): ")
            if response.lower() in ['y', 'yes']:
                import shutil
                try:
                    shutil.rmtree(manager.base_output_dir)
                    print("✓ Output directory cleaned successfully")

                    # Recreate structure
                    if manager.initialize_output_structure():
                        print("✓ Output directory structure recreated")
                except Exception as e:
                    print(f"✗ Error cleaning directory: {e}")
            else:
                print("Cleaning cancelled")

    def _show_output_info(self, manager: OutputManager) -> None:
        """Show output directory information."""
        print(f"Output Directory Information")
        print("=" * 40)
        print(f"Path: {manager.base_output_dir}")
        print(f"Exists: {manager.base_output_dir.exists()}")

        if manager.base_output_dir.exists():
            # Directory size
            size_bytes = manager.get_directory_size()
            if size_bytes > 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            elif size_bytes > 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes} bytes"
            print(f"Size: {size_str}")

            # File counts
            file_lists = manager.list_output_files()
            total_files = sum(len(files) for files in file_lists.values())
            print(f"Total files: {total_files}")

            for category, files in file_lists.items():
                if files:
                    print(f"  {category}: {len(files)} files")

            # Disk usage
            usage = manager.get_disk_usage()
            if usage:
                print(f"\nDisk Usage:")
                print(f"  Total: {usage['total_gb']:.1f} GB")
                print(f"  Used:  {usage['used_gb']:.1f} GB ({usage['usage_percent']:.1f}%)")
                print(f"  Free:  {usage['free_gb']:.1f} GB")

                # Check available space
                has_space_100mb = manager.check_available_space(100)
                has_space_1gb = manager.check_available_space(1000)
                print(f"\nAvailable space check:")
                print(f"  100 MB: {'✓' if has_space_100mb else '✗'}")
                print(f"  1 GB:   {'✓' if has_space_1gb else '✗'}")

        # Configuration info
        print(f"\nConfiguration:")
        print(f"  Auto-create directories: {self.config.export.auto_create_directories}")
        print(f"  Organize by algorithm: {self.config.export.organize_by_algorithm}")
        print(f"  Organize by date: {self.config.export.organize_by_date}")
        print(f"  Use timestamped filenames: {self.config.export.use_timestamped_filenames}")
        print(f"  Cleanup temp files: {self.config.export.cleanup_temp_files}")
        print(f"  Temp file max age: {self.config.export.temp_file_max_age_hours} hours")

    def _get_output_filename(self, args: argparse.Namespace, base_name: str = None) -> str:
        """Generate output filename based on arguments and configuration."""
        if args.output:
            return args.output

        # Generate automatic filename
        if not base_name:
            base_name = f"maze_{args.width}x{args.height}"

        # Add algorithm suffix if organizing by algorithm
        if hasattr(args, 'organize_by_algorithm') and args.organize_by_algorithm:
            algorithm = getattr(args, 'algorithm', getattr(args, 'gen_algorithm', 'unknown'))
            base_name += f"_{algorithm}"

        # Add solution suffix if this is a solved maze
        if hasattr(args, 'solve_algorithm'):
            base_name += f"_solved_{args.solve_algorithm}"

        return f"{base_name}.{args.format}"

    def _output_maze(self, maze: Maze, args: argparse.Namespace,
                    show_solution: bool = False, show_visited: bool = False) -> None:
        """Output maze in the specified format."""
        title = args.title or f"Maze ({args.width}x{args.height})"

        # Initialize output manager if not already done
        if not self.output_manager:
            if not self._initialize_output_manager(args):
                return

        if args.format == 'ascii':
            renderer = AsciiRenderer()
            if args.output or not sys.stdout.isatty():
                # Determine output path
                filename = self._get_output_filename(args, "maze_ascii")

                if hasattr(args, 'organize_by_algorithm') and args.organize_by_algorithm:
                    algorithm = getattr(args, 'algorithm', getattr(args, 'gen_algorithm', 'dfs'))
                    output_path = self.output_manager.organize_by_algorithm(algorithm, filename, 'ascii')
                elif hasattr(args, 'organize_by_date') and args.organize_by_date:
                    output_path = self.output_manager.organize_by_date(filename, 'ascii')
                elif hasattr(args, 'timestamped') and args.timestamped:
                    base_name = filename.rsplit('.', 1)[0]
                    extension = filename.rsplit('.', 1)[1] if '.' in filename else 'txt'
                    output_path = self.output_manager.get_timestamped_filename(base_name, extension, 'ascii')
                else:
                    output_path = self.output_manager.get_output_path(filename, 'ascii')

                renderer.save_to_file(maze, str(output_path), show_solution, title=title)
                print(f"ASCII maze saved to {output_path}")
            else:
                renderer.print_maze(maze, show_solution, title=title)
        
        elif args.format == 'matplotlib':
            renderer = MatplotlibRenderer(args.cell_size, args.wall_width)
            if args.output or not sys.stdout.isatty():
                filename = self._get_output_filename(args, "maze_matplotlib")
                if not filename.endswith('.png'):
                    filename = filename.rsplit('.', 1)[0] + '.png'

                output_path = self._get_organized_output_path(args, filename, 'images')
                renderer.save_image(maze, str(output_path), show_solution, show_visited)
                print(f"Matplotlib maze saved to {output_path}")
            else:
                renderer.show(maze, show_solution, show_visited)

        elif args.format in ['png', 'jpg', 'svg']:
            filename = self._get_output_filename(args)
            file_type = 'svg' if args.format == 'svg' else 'images'
            output_path = self._get_organized_output_path(args, filename, file_type)

            exporter = ImageExporter(args.cell_size, args.wall_width)

            if args.format == 'png':
                exporter.export_png(maze, str(output_path), show_solution, show_visited, title=title)
            elif args.format == 'jpg':
                exporter.export_jpg(maze, str(output_path), show_solution, show_visited, title=title)
            elif args.format == 'svg':
                exporter.export_svg(maze, str(output_path), show_solution, show_visited, title=title)

            print(f"Maze saved to {output_path}")

    def _get_organized_output_path(self, args: argparse.Namespace, filename: str, file_type: str):
        """Get organized output path based on arguments."""
        if hasattr(args, 'organize_by_algorithm') and args.organize_by_algorithm:
            algorithm = getattr(args, 'algorithm', getattr(args, 'gen_algorithm', 'dfs'))
            return self.output_manager.organize_by_algorithm(algorithm, filename, file_type)
        elif hasattr(args, 'organize_by_date') and args.organize_by_date:
            return self.output_manager.organize_by_date(filename, file_type)
        elif hasattr(args, 'timestamped') and args.timestamped:
            base_name = filename.rsplit('.', 1)[0]
            extension = filename.rsplit('.', 1)[1] if '.' in filename else 'png'
            return self.output_manager.get_timestamped_filename(base_name, extension, file_type)
        else:
            return self.output_manager.get_output_path(filename, file_type)

    def run(self, args: Optional[list] = None) -> None:
        """Run the CLI with the given arguments."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return
        
        try:
            # Initialize output manager for commands that need it
            if parsed_args.command in ['generate', 'solve']:
                if not self._initialize_output_manager(parsed_args):
                    sys.exit(1)

            if parsed_args.command == 'generate':
                self.generate_maze(parsed_args)
            elif parsed_args.command == 'solve':
                self.solve_maze(parsed_args)
            elif parsed_args.command == 'interactive':
                self.interactive_mode(parsed_args)
            elif parsed_args.command == 'benchmark':
                self.benchmark_algorithms(parsed_args)
            elif parsed_args.command == 'output':
                self.manage_output_directory(parsed_args)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    cli = MazeGeneratorCLI()
    cli.run()


if __name__ == '__main__':
    main()
