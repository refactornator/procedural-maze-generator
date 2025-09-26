"""Validation utilities for maze parameters."""

from typing import Tuple, Optional


def validate_maze_dimensions(width: int, height: int, 
                           min_size: int = 1, max_size: int = 1000) -> bool:
    """Validate maze dimensions."""
    if not isinstance(width, int) or not isinstance(height, int):
        raise TypeError("Width and height must be integers")
    
    if width < min_size or height < min_size:
        raise ValueError(f"Maze dimensions must be at least {min_size}x{min_size}")
    
    if width > max_size or height > max_size:
        raise ValueError(f"Maze dimensions must not exceed {max_size}x{max_size}")
    
    return True


def validate_coordinates(x: int, y: int, width: int, height: int) -> bool:
    """Validate coordinates within maze bounds."""
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Coordinates must be integers")
    
    if x < 0 or x >= width:
        raise ValueError(f"X coordinate {x} is out of bounds (0-{width-1})")
    
    if y < 0 or y >= height:
        raise ValueError(f"Y coordinate {y} is out of bounds (0-{height-1})")
    
    return True


def validate_seed(seed: Optional[int]) -> bool:
    """Validate random seed value."""
    if seed is not None and not isinstance(seed, int):
        raise TypeError("Seed must be an integer or None")
    
    return True


def validate_cell_size(cell_size: int, min_size: int = 1, max_size: int = 200) -> bool:
    """Validate cell size for visualization."""
    if not isinstance(cell_size, int):
        raise TypeError("Cell size must be an integer")
    
    if cell_size < min_size:
        raise ValueError(f"Cell size must be at least {min_size}")
    
    if cell_size > max_size:
        raise ValueError(f"Cell size must not exceed {max_size}")
    
    return True


def validate_wall_width(wall_width: int, min_width: int = 0, max_width: int = 20) -> bool:
    """Validate wall width for visualization."""
    if not isinstance(wall_width, int):
        raise TypeError("Wall width must be an integer")
    
    if wall_width < min_width:
        raise ValueError(f"Wall width must be at least {min_width}")
    
    if wall_width > max_width:
        raise ValueError(f"Wall width must not exceed {max_width}")
    
    return True


def validate_algorithm_name(algorithm: str, available_algorithms: list) -> bool:
    """Validate algorithm name against available algorithms."""
    if not isinstance(algorithm, str):
        raise TypeError("Algorithm name must be a string")
    
    if algorithm not in available_algorithms:
        raise ValueError(f"Unknown algorithm '{algorithm}'. "
                        f"Available algorithms: {', '.join(available_algorithms)}")
    
    return True


def validate_file_path(file_path: str, allowed_extensions: Optional[list] = None) -> bool:
    """Validate file path and extension."""
    if not isinstance(file_path, str):
        raise TypeError("File path must be a string")
    
    if not file_path.strip():
        raise ValueError("File path cannot be empty")
    
    if allowed_extensions:
        extension = file_path.lower().split('.')[-1] if '.' in file_path else ''
        if extension not in allowed_extensions:
            raise ValueError(f"File extension '{extension}' not allowed. "
                           f"Allowed extensions: {', '.join(allowed_extensions)}")
    
    return True


def validate_color_hex(color: str) -> bool:
    """Validate hexadecimal color string."""
    if not isinstance(color, str):
        raise TypeError("Color must be a string")
    
    if not color.startswith('#'):
        raise ValueError("Color must start with '#'")
    
    if len(color) not in [4, 7]:  # #RGB or #RRGGBB
        raise ValueError("Color must be in format #RGB or #RRGGBB")
    
    try:
        int(color[1:], 16)
    except ValueError:
        raise ValueError("Color must contain valid hexadecimal digits")
    
    return True


def validate_rgb_color(color: Tuple[int, int, int]) -> bool:
    """Validate RGB color tuple."""
    if not isinstance(color, (tuple, list)) or len(color) != 3:
        raise TypeError("RGB color must be a tuple or list of 3 integers")
    
    for i, component in enumerate(color):
        if not isinstance(component, int):
            raise TypeError(f"RGB component {i} must be an integer")
        
        if not (0 <= component <= 255):
            raise ValueError(f"RGB component {i} must be between 0 and 255")
    
    return True


def validate_percentage(value: float, name: str = "value") -> bool:
    """Validate a percentage value (0.0 to 1.0)."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} must be between 0.0 and 1.0")
    
    return True


def validate_positive_integer(value: int, name: str = "value", 
                            min_value: int = 1) -> bool:
    """Validate a positive integer."""
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    
    if value < min_value:
        raise ValueError(f"{name} must be at least {min_value}")
    
    return True


def validate_non_negative_integer(value: int, name: str = "value") -> bool:
    """Validate a non-negative integer."""
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    
    return True
