"""Pytest configuration and shared fixtures."""

import pytest
import sys
from pathlib import Path

# Add src directory to Python path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_maze_sizes():
    """Provide various maze sizes for testing."""
    return [(3, 3), (5, 5), (10, 10), (15, 8)]


@pytest.fixture
def test_seed():
    """Provide a consistent seed for reproducible tests."""
    return 42


@pytest.fixture
def algorithms():
    """Provide list of available algorithms."""
    return {
        'generators': ['dfs', 'kruskal', 'prim', 'wilson'],
        'solvers': ['astar', 'dijkstra', 'bfs', 'dfs', 'wall-follower']
    }
