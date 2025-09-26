"""Unit tests for the output manager."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from maze_generator.utils.output_manager import OutputManager, OutputDirectoryError


class TestOutputManager:
    """Test the OutputManager class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def output_manager(self, temp_dir):
        """Create an OutputManager instance with temporary directory."""
        return OutputManager(temp_dir / "output")
    
    def test_initialization(self, temp_dir):
        """Test OutputManager initialization."""
        manager = OutputManager(temp_dir / "test_output")
        assert manager.base_output_dir == temp_dir / "test_output"
        assert 'images' in manager.subdirs
        assert 'ascii' in manager.subdirs
        assert 'svg' in manager.subdirs
    
    def test_default_initialization(self):
        """Test OutputManager with default directory."""
        manager = OutputManager()
        assert manager.base_output_dir == Path.cwd() / "output"
    
    def test_initialize_output_structure(self, output_manager):
        """Test creating the complete output directory structure."""
        result = output_manager.initialize_output_structure()
        assert result is True
        
        # Check that base directory exists
        assert output_manager.base_output_dir.exists()
        
        # Check that all subdirectories exist
        for subdir_name in output_manager.subdirs.values():
            subdir_path = output_manager.base_output_dir / subdir_name
            assert subdir_path.exists()
            assert subdir_path.is_dir()
        
        # Check that info file was created
        info_file = output_manager.base_output_dir / "README.txt"
        assert info_file.exists()
    
    def test_get_output_path(self, output_manager):
        """Test getting output paths for files."""
        output_manager.initialize_output_structure()
        
        # Test basic path generation
        path = output_manager.get_output_path("test.png", "images")
        expected = output_manager.base_output_dir / "images" / "test.png"
        assert path == expected
        
        # Test with different file type
        path = output_manager.get_output_path("maze.txt", "ascii")
        expected = output_manager.base_output_dir / "ascii" / "maze.txt"
        assert path == expected
    
    def test_get_output_path_unique(self, output_manager):
        """Test unique filename generation."""
        output_manager.initialize_output_structure()
        
        # Create a file
        first_path = output_manager.get_output_path("test.png", "images", create_unique=False)
        first_path.touch()
        
        # Get unique path
        unique_path = output_manager.get_output_path("test.png", "images", create_unique=True)
        assert unique_path != first_path
        assert "test_1.png" in str(unique_path)
    
    def test_get_auto_filename(self, output_manager):
        """Test automatic filename generation with counters."""
        output_manager.initialize_output_structure()
        
        # Get first auto filename
        path1 = output_manager.get_auto_filename("maze", "png", "images")
        assert "maze_0001.png" in str(path1)
        
        # Create the file
        path1.touch()
        
        # Get next auto filename
        path2 = output_manager.get_auto_filename("maze", "png", "images")
        assert "maze_0002.png" in str(path2)
    
    def test_get_timestamped_filename(self, output_manager):
        """Test timestamped filename generation."""
        output_manager.initialize_output_structure()
        
        path = output_manager.get_timestamped_filename("maze", "png", "images")
        
        # Check that timestamp is in filename
        filename = path.name
        assert filename.startswith("maze_")
        assert filename.endswith(".png")
        assert len(filename) == len("maze_YYYYMMDD_HHMMSS.png")
    
    def test_organize_by_algorithm(self, output_manager):
        """Test organizing files by algorithm."""
        output_manager.initialize_output_structure()
        
        path = output_manager.organize_by_algorithm("dfs", "test.png", "images")
        expected = output_manager.base_output_dir / "images" / "dfs" / "test.png"
        assert path == expected
        
        # Check that algorithm subdirectory was created
        assert (output_manager.base_output_dir / "images" / "dfs").exists()
    
    def test_organize_by_date(self, output_manager):
        """Test organizing files by date."""
        output_manager.initialize_output_structure()
        
        path = output_manager.organize_by_date("test.png", "images")
        
        # Check that date subdirectory is in path
        assert "images" in str(path)
        assert "test.png" in str(path)
        
        # Date should be in YYYY-MM-DD format
        import datetime
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        assert today in str(path)
    
    def test_cleanup_temp_files(self, output_manager):
        """Test temporary file cleanup."""
        output_manager.initialize_output_structure()
        
        temp_dir = output_manager.base_output_dir / "temp"
        
        # Create some temp files
        old_file = temp_dir / "old_file.tmp"
        new_file = temp_dir / "new_file.tmp"
        
        old_file.touch()
        new_file.touch()
        
        # Make old file appear old by modifying its timestamp
        import time
        old_time = time.time() - (25 * 3600)  # 25 hours ago
        old_file.touch(times=(old_time, old_time))
        
        # Cleanup files older than 24 hours
        cleaned = output_manager.cleanup_temp_files(24)
        
        assert cleaned == 1
        assert not old_file.exists()
        assert new_file.exists()
    
    def test_get_disk_usage(self, output_manager):
        """Test disk usage information."""
        output_manager.initialize_output_structure()
        
        usage = output_manager.get_disk_usage()
        
        assert 'total_bytes' in usage
        assert 'used_bytes' in usage
        assert 'free_bytes' in usage
        assert 'total_gb' in usage
        assert 'usage_percent' in usage
        
        assert usage['total_bytes'] > 0
        assert usage['free_bytes'] >= 0
        assert 0 <= usage['usage_percent'] <= 100
    
    def test_check_available_space(self, output_manager):
        """Test available space checking."""
        output_manager.initialize_output_structure()
        
        # Should have space for small requirement
        assert output_manager.check_available_space(1) is True
        
        # Might not have space for huge requirement
        result = output_manager.check_available_space(1000000)  # 1TB
        assert isinstance(result, bool)
    
    def test_get_directory_size(self, output_manager):
        """Test directory size calculation."""
        output_manager.initialize_output_structure()
        
        # Create some files
        test_file = output_manager.base_output_dir / "images" / "test.txt"
        test_file.write_text("Hello, World!")
        
        size = output_manager.get_directory_size()
        assert size > 0
    
    def test_list_output_files(self, output_manager):
        """Test listing output files."""
        output_manager.initialize_output_structure()
        
        # Create some test files
        (output_manager.base_output_dir / "images" / "test1.png").touch()
        (output_manager.base_output_dir / "ascii" / "test2.txt").touch()
        
        # List all files
        file_lists = output_manager.list_output_files()
        
        assert 'images' in file_lists
        assert 'ascii' in file_lists
        assert len(file_lists['images']) >= 1
        assert len(file_lists['ascii']) >= 1
        
        # List specific file type
        image_files = output_manager.list_output_files('images')
        assert 'images' in image_files
        assert len(image_files['images']) >= 1
    
    def test_permission_error_handling(self, temp_dir):
        """Test handling of permission errors."""
        # Create a directory with no write permissions
        restricted_dir = temp_dir / "restricted"
        restricted_dir.mkdir()
        restricted_dir.chmod(0o444)  # Read-only
        
        try:
            manager = OutputManager(restricted_dir / "output")
            result = manager.initialize_output_structure()
            assert result is False
        finally:
            # Restore permissions for cleanup
            restricted_dir.chmod(0o755)
    
    @patch('shutil.disk_usage')
    def test_disk_space_error_handling(self, mock_disk_usage, output_manager):
        """Test handling of disk space errors."""
        mock_disk_usage.side_effect = OSError("Disk error")
        
        usage = output_manager.get_disk_usage()
        assert usage == {}
        
        # Should return True (assume OK) when can't check
        result = output_manager.check_available_space(100)
        assert result is True
    
    def test_string_representations(self, output_manager):
        """Test string representations of OutputManager."""
        str_repr = str(output_manager)
        assert "OutputManager" in str_repr
        assert str(output_manager.base_output_dir) in str_repr
        
        repr_str = repr(output_manager)
        assert "OutputManager" in repr_str
        assert "subdirs" in repr_str
