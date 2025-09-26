"""Output directory management for the maze generator."""

import os
import shutil
from pathlib import Path
from typing import Optional, Union, Dict, Any
from datetime import datetime
import logging

from .file_utils import ensure_directory_exists, get_unique_filename, clean_filename


class OutputDirectoryError(Exception):
    """Exception raised when output directory operations fail."""
    pass


class OutputManager:
    """Manages output directories and file organization for maze generation."""
    
    def __init__(self, base_output_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the output manager.
        
        Args:
            base_output_dir: Base output directory path. If None, uses 'output' in current directory.
        """
        self.base_output_dir = Path(base_output_dir) if base_output_dir else Path.cwd() / "output"
        self.logger = logging.getLogger(__name__)
        
        # Subdirectory structure
        self.subdirs = {
            'images': 'images',
            'ascii': 'ascii',
            'svg': 'svg',
            'animations': 'animations',
            'benchmarks': 'benchmarks',
            'temp': 'temp'
        }
        
        # File counters for automatic naming
        self._file_counters = {}
    
    def initialize_output_structure(self) -> bool:
        """
        Initialize the complete output directory structure.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Create base directory
            self._create_directory(self.base_output_dir)
            
            # Create subdirectories
            for subdir_key, subdir_name in self.subdirs.items():
                subdir_path = self.base_output_dir / subdir_name
                self._create_directory(subdir_path)
            
            # Create info file
            self._create_info_file()
            
            self.logger.info(f"Output directory structure initialized at: {self.base_output_dir}")
            return True
            
        except OutputDirectoryError as e:
            self.logger.error(f"Failed to initialize output structure: {e}")
            return False
    
    def _create_directory(self, path: Path) -> None:
        """
        Create a directory with proper error handling.
        
        Args:
            path: Directory path to create.
            
        Raises:
            OutputDirectoryError: If directory creation fails.
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            
            # Test write permissions
            test_file = path / ".write_test"
            try:
                test_file.touch()
                test_file.unlink()
            except (PermissionError, OSError) as e:
                raise OutputDirectoryError(
                    f"No write permission for directory: {path}. Error: {e}"
                )
                
        except PermissionError as e:
            raise OutputDirectoryError(
                f"Permission denied creating directory: {path}. Error: {e}"
            )
        except OSError as e:
            if e.errno == 28:  # No space left on device
                raise OutputDirectoryError(
                    f"Insufficient disk space to create directory: {path}"
                )
            else:
                raise OutputDirectoryError(
                    f"Failed to create directory: {path}. Error: {e}"
                )
    
    def _create_info_file(self) -> None:
        """Create an info file in the output directory."""
        info_file = self.base_output_dir / "README.txt"
        
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write("Procedural Maze Generator - Output Directory\n")
                f.write("=" * 45 + "\n\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("Directory Structure:\n")
                f.write("- images/      : PNG and JPEG maze images\n")
                f.write("- ascii/       : ASCII text maze files\n")
                f.write("- svg/         : SVG vector maze files\n")
                f.write("- animations/  : Animated maze generation/solving\n")
                f.write("- benchmarks/  : Performance benchmark results\n")
                f.write("- temp/        : Temporary files\n\n")
                f.write("This directory was created automatically by the\n")
                f.write("Procedural Maze Generator application.\n")
                
        except (PermissionError, OSError) as e:
            self.logger.warning(f"Could not create info file: {e}")
    
    def get_output_path(self, filename: str, file_type: str = 'images', 
                       create_unique: bool = True) -> Path:
        """
        Get the full output path for a file.
        
        Args:
            filename: Base filename.
            file_type: Type of file (images, ascii, svg, animations, benchmarks).
            create_unique: If True, create unique filename if file exists.
            
        Returns:
            Path: Full path for the output file.
        """
        # Clean the filename
        clean_name = clean_filename(filename)
        
        # Get the appropriate subdirectory
        if file_type in self.subdirs:
            subdir = self.base_output_dir / self.subdirs[file_type]
        else:
            subdir = self.base_output_dir
        
        # Ensure subdirectory exists
        try:
            self._create_directory(subdir)
        except OutputDirectoryError:
            # Fall back to base directory if subdirectory creation fails
            subdir = self.base_output_dir
            self._create_directory(subdir)
        
        full_path = subdir / clean_name
        
        # Create unique filename if requested and file exists
        if create_unique and full_path.exists():
            full_path = Path(get_unique_filename(str(full_path)))
        
        return full_path
    
    def get_auto_filename(self, prefix: str, extension: str, 
                         file_type: str = 'images') -> Path:
        """
        Generate an automatic filename with counter.
        
        Args:
            prefix: Filename prefix (e.g., 'maze', 'solution').
            extension: File extension (e.g., 'png', 'txt').
            file_type: Type of file for directory organization.
            
        Returns:
            Path: Full path with auto-generated filename.
        """
        # Initialize counter for this prefix if not exists
        counter_key = f"{file_type}_{prefix}"
        if counter_key not in self._file_counters:
            self._file_counters[counter_key] = 1
        
        # Generate filename with counter
        while True:
            counter = self._file_counters[counter_key]
            filename = f"{prefix}_{counter:04d}.{extension}"
            full_path = self.get_output_path(filename, file_type, create_unique=False)
            
            if not full_path.exists():
                self._file_counters[counter_key] = counter + 1
                return full_path
            
            self._file_counters[counter_key] += 1
    
    def get_timestamped_filename(self, prefix: str, extension: str,
                                file_type: str = 'images') -> Path:
        """
        Generate a filename with timestamp.
        
        Args:
            prefix: Filename prefix.
            extension: File extension.
            file_type: Type of file for directory organization.
            
        Returns:
            Path: Full path with timestamped filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"
        return self.get_output_path(filename, file_type, create_unique=False)
    
    def organize_by_algorithm(self, algorithm_name: str, filename: str,
                             file_type: str = 'images') -> Path:
        """
        Organize files by algorithm in subdirectories.
        
        Args:
            algorithm_name: Name of the algorithm used.
            filename: Base filename.
            file_type: Type of file for directory organization.
            
        Returns:
            Path: Full path organized by algorithm.
        """
        # Create algorithm subdirectory
        algo_subdir = self.base_output_dir / self.subdirs[file_type] / clean_filename(algorithm_name)
        
        try:
            self._create_directory(algo_subdir)
        except OutputDirectoryError:
            # Fall back to main subdirectory
            algo_subdir = self.base_output_dir / self.subdirs[file_type]
        
        clean_name = clean_filename(filename)
        return algo_subdir / clean_name
    
    def organize_by_date(self, filename: str, file_type: str = 'images') -> Path:
        """
        Organize files by date in subdirectories.
        
        Args:
            filename: Base filename.
            file_type: Type of file for directory organization.
            
        Returns:
            Path: Full path organized by date.
        """
        # Create date subdirectory (YYYY-MM-DD format)
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_subdir = self.base_output_dir / self.subdirs[file_type] / date_str
        
        try:
            self._create_directory(date_subdir)
        except OutputDirectoryError:
            # Fall back to main subdirectory
            date_subdir = self.base_output_dir / self.subdirs[file_type]
        
        clean_name = clean_filename(filename)
        return date_subdir / clean_name
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up temporary files older than specified age.
        
        Args:
            max_age_hours: Maximum age of temp files in hours.
            
        Returns:
            int: Number of files cleaned up.
        """
        temp_dir = self.base_output_dir / self.subdirs['temp']
        
        if not temp_dir.exists():
            return 0
        
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        cleaned_count = 0
        
        try:
            for file_path in temp_dir.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age_seconds:
                        try:
                            file_path.unlink()
                            cleaned_count += 1
                        except (PermissionError, OSError) as e:
                            self.logger.warning(f"Could not delete temp file {file_path}: {e}")
        
        except (PermissionError, OSError) as e:
            self.logger.warning(f"Could not access temp directory: {e}")
        
        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} temporary files")
        
        return cleaned_count
    
    def get_disk_usage(self) -> Dict[str, Any]:
        """
        Get disk usage information for the output directory.
        
        Returns:
            Dict: Disk usage information.
        """
        try:
            usage = shutil.disk_usage(self.base_output_dir)
            
            return {
                'total_bytes': usage.total,
                'used_bytes': usage.used,
                'free_bytes': usage.free,
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'free_gb': usage.free / (1024**3),
                'usage_percent': (usage.used / usage.total) * 100
            }
        except OSError as e:
            self.logger.error(f"Could not get disk usage: {e}")
            return {}
    
    def check_available_space(self, required_mb: float = 100) -> bool:
        """
        Check if there's enough available disk space.
        
        Args:
            required_mb: Required space in megabytes.
            
        Returns:
            bool: True if enough space is available.
        """
        usage = self.get_disk_usage()
        if not usage:
            return True  # Assume OK if we can't check
        
        required_bytes = required_mb * 1024 * 1024
        return usage['free_bytes'] >= required_bytes
    
    def get_directory_size(self) -> int:
        """
        Get the total size of the output directory in bytes.
        
        Returns:
            int: Total size in bytes.
        """
        total_size = 0
        
        try:
            for dirpath, dirnames, filenames in os.walk(self.base_output_dir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        pass  # Skip files that can't be accessed
        except (PermissionError, OSError):
            pass  # Return partial size if directory can't be fully accessed
        
        return total_size
    
    def list_output_files(self, file_type: Optional[str] = None) -> Dict[str, list]:
        """
        List all files in the output directory.
        
        Args:
            file_type: Specific file type to list, or None for all.
            
        Returns:
            Dict: Dictionary of file lists organized by type.
        """
        file_lists = {}
        
        if file_type and file_type in self.subdirs:
            subdirs_to_check = {file_type: self.subdirs[file_type]}
        else:
            subdirs_to_check = self.subdirs
        
        for subdir_key, subdir_name in subdirs_to_check.items():
            subdir_path = self.base_output_dir / subdir_name
            file_lists[subdir_key] = []
            
            if subdir_path.exists():
                try:
                    for file_path in subdir_path.rglob('*'):
                        if file_path.is_file():
                            file_lists[subdir_key].append(str(file_path.relative_to(self.base_output_dir)))
                except (PermissionError, OSError) as e:
                    self.logger.warning(f"Could not list files in {subdir_path}: {e}")
        
        return file_lists
    
    def __str__(self) -> str:
        """String representation of the output manager."""
        return f"OutputManager(base_dir='{self.base_output_dir}')"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"OutputManager(base_output_dir='{self.base_output_dir}', subdirs={list(self.subdirs.keys())})"
