"""File and directory utilities."""

import os
from pathlib import Path
from typing import Optional, List


def ensure_directory_exists(path: str) -> None:
    """Ensure that a directory exists, creating it if necessary."""
    directory = Path(path).parent if Path(path).is_file() else Path(path)
    directory.mkdir(parents=True, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """Get the file extension from a filename."""
    return Path(filename).suffix.lower().lstrip('.')


def is_valid_filename(filename: str) -> bool:
    """Check if a filename is valid for the current operating system."""
    if not filename or filename.strip() != filename:
        return False
    
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?*'
    if any(char in filename for char in invalid_chars):
        return False
    
    # Check for reserved names on Windows
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    name_without_ext = Path(filename).stem.upper()
    if name_without_ext in reserved_names:
        return False
    
    return True


def get_unique_filename(base_path: str) -> str:
    """Generate a unique filename by appending a number if necessary."""
    path = Path(base_path)
    
    if not path.exists():
        return str(path)
    
    counter = 1
    while True:
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        
        if not new_path.exists():
            return str(new_path)
        
        counter += 1


def list_files_with_extension(directory: str, extension: str) -> List[str]:
    """List all files with a specific extension in a directory."""
    directory_path = Path(directory)
    
    if not directory_path.exists() or not directory_path.is_dir():
        return []
    
    extension = extension.lower().lstrip('.')
    files = []
    
    for file_path in directory_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower().lstrip('.') == extension:
            files.append(str(file_path))
    
    return sorted(files)


def get_file_size(file_path: str) -> int:
    """Get the size of a file in bytes."""
    path = Path(file_path)
    
    if not path.exists() or not path.is_file():
        return 0
    
    return path.stat().st_size


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def backup_file(file_path: str, backup_suffix: str = ".bak") -> Optional[str]:
    """Create a backup of a file."""
    path = Path(file_path)
    
    if not path.exists() or not path.is_file():
        return None
    
    backup_path = path.with_suffix(path.suffix + backup_suffix)
    backup_path = Path(get_unique_filename(str(backup_path)))
    
    try:
        import shutil
        shutil.copy2(path, backup_path)
        return str(backup_path)
    except Exception:
        return None


def clean_filename(filename: str) -> str:
    """Clean a filename by removing or replacing invalid characters."""
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    cleaned = filename
    
    for char in invalid_chars:
        cleaned = cleaned.replace(char, '_')
    
    # Remove leading/trailing whitespace and dots
    cleaned = cleaned.strip(' .')
    
    # Ensure it's not empty
    if not cleaned:
        cleaned = "unnamed"
    
    return cleaned


def get_relative_path(file_path: str, base_path: str) -> str:
    """Get the relative path from base_path to file_path."""
    try:
        return str(Path(file_path).relative_to(Path(base_path)))
    except ValueError:
        return file_path


def find_files_by_pattern(directory: str, pattern: str) -> List[str]:
    """Find files matching a glob pattern in a directory."""
    directory_path = Path(directory)
    
    if not directory_path.exists() or not directory_path.is_dir():
        return []
    
    return [str(path) for path in directory_path.glob(pattern) if path.is_file()]
