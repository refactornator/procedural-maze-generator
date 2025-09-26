"""Integration tests for the CLI."""

import pytest
import tempfile
import os
from pathlib import Path
from maze_generator.cli import MazeGeneratorCLI


class TestCLIIntegration:
    """Test CLI integration."""
    
    @pytest.fixture
    def cli(self):
        """Create CLI instance."""
        return MazeGeneratorCLI()
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_generate_ascii_maze(self, cli, temp_dir):
        """Test generating ASCII maze."""
        output_file = os.path.join(temp_dir, "test_maze.txt")
        args = ['generate', '10', '10', '--format', 'ascii', '--output', output_file]
        
        cli.run(args)
        
        assert os.path.exists(output_file)
        with open(output_file, 'r') as f:
            content = f.read()
            assert len(content) > 0
            assert '█' in content or '+' in content  # Wall characters
    
    def test_generate_png_maze(self, cli, temp_dir):
        """Test generating PNG maze."""
        output_file = os.path.join(temp_dir, "test_maze.png")
        args = ['generate', '5', '5', '--format', 'png', '--output', output_file]
        
        cli.run(args)
        
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_solve_maze(self, cli, temp_dir):
        """Test solving a maze."""
        output_file = os.path.join(temp_dir, "solution.txt")
        args = ['solve', '8', '8', '--format', 'ascii', '--output', output_file]
        
        cli.run(args)
        
        assert os.path.exists(output_file)
        with open(output_file, 'r') as f:
            content = f.read()
            assert len(content) > 0
    
    def test_benchmark_command(self, cli, capsys):
        """Test benchmark command."""
        args = ['benchmark', '5', '5', '--iterations', '3']
        
        cli.run(args)
        
        captured = capsys.readouterr()
        assert "Benchmarking algorithms" in captured.out
        assert "Fastest algorithm" in captured.out
    
    def test_invalid_dimensions(self, cli, capsys):
        """Test handling of invalid dimensions."""
        args = ['generate', '0', '5']
        
        with pytest.raises(SystemExit):
            cli.run(args)
    
    def test_different_algorithms(self, cli, temp_dir):
        """Test different generation algorithms."""
        algorithms = ['dfs', 'kruskal', 'prim']
        
        for algorithm in algorithms:
            output_file = os.path.join(temp_dir, f"maze_{algorithm}.txt")
            args = ['generate', '5', '5', '--algorithm', algorithm, 
                   '--format', 'ascii', '--output', output_file]
            
            cli.run(args)
            
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0
    
    def test_seed_reproducibility(self, cli, temp_dir):
        """Test that same seed produces same maze."""
        output1 = os.path.join(temp_dir, "maze1.txt")
        output2 = os.path.join(temp_dir, "maze2.txt")
        
        args1 = ['generate', '5', '5', '--seed', '123', '--format', 'ascii', '--output', output1]
        args2 = ['generate', '5', '5', '--seed', '123', '--format', 'ascii', '--output', output2]
        
        cli.run(args1)
        cli.run(args2)
        
        with open(output1, 'r') as f1, open(output2, 'r') as f2:
            content1 = f1.read()
            content2 = f2.read()
            assert content1 == content2
