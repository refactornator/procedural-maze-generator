"""Configuration management for the maze generator."""

from __future__ import annotations
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import os

# Optional YAML support
try:
    import yaml
    HAS_YAML = True
except ImportError:
    yaml = None
    HAS_YAML = False


@dataclass
class VisualizationConfig:
    """Configuration for maze visualization."""
    cell_size: int = 20
    wall_width: int = 2
    colors: Dict[str, str] = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                'wall': '#000000',
                'path': '#FFFFFF',
                'start': '#00FF00',
                'end': '#FF0000',
                'solution': '#0000FF',
                'visited': '#FFFF00',
                'current': '#FFA500',
                'frontier': '#800080',
            }


@dataclass
class GenerationConfig:
    """Configuration for maze generation."""
    default_algorithm: str = 'dfs'
    default_width: int = 20
    default_height: int = 20
    default_seed: Optional[int] = None
    animation_delay_ms: int = 50


@dataclass
class SolvingConfig:
    """Configuration for maze solving."""
    default_algorithm: str = 'astar'
    animation_delay_ms: int = 100
    show_visited: bool = True
    show_path: bool = True


@dataclass
class ExportConfig:
    """Configuration for maze export."""
    default_format: str = 'png'
    default_dpi: int = 300
    jpeg_quality: int = 95
    add_border: bool = True
    add_title: bool = True
    output_directory: str = 'output'
    organize_by_algorithm: bool = False
    organize_by_date: bool = False
    auto_create_directories: bool = True
    use_timestamped_filenames: bool = False
    cleanup_temp_files: bool = True
    temp_file_max_age_hours: int = 24


@dataclass
class MazeGeneratorConfig:
    """Main configuration class for the maze generator."""
    visualization: VisualizationConfig = None
    generation: GenerationConfig = None
    solving: SolvingConfig = None
    export: ExportConfig = None
    
    def __post_init__(self):
        if self.visualization is None:
            self.visualization = VisualizationConfig()
        if self.generation is None:
            self.generation = GenerationConfig()
        if self.solving is None:
            self.solving = SolvingConfig()
        if self.export is None:
            self.export = ExportConfig()


class ConfigManager:
    """Manages configuration loading, saving, and validation."""
    
    DEFAULT_CONFIG_PATHS = [
        Path.home() / '.maze_generator' / 'config.yaml',
        Path.cwd() / 'config.yaml',
        Path.cwd() / '.maze_generator.yaml',
    ]
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """Initialize the configuration manager."""
        self.config_path = Path(config_path) if config_path else None
        self.config = MazeGeneratorConfig()
    
    def load_config(self, config_path: Optional[Union[str, Path]] = None) -> MazeGeneratorConfig:
        """Load configuration from file."""
        if config_path:
            self.config_path = Path(config_path)
        
        # Try to find config file
        config_file = self._find_config_file()
        
        if config_file and config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    if config_file.suffix.lower() in ['.yaml', '.yml']:
                        if not HAS_YAML:
                            raise ImportError("PyYAML is required for YAML config files. Install with: pip install PyYAML")
                        data = yaml.safe_load(f)
                    elif config_file.suffix.lower() == '.json':
                        data = json.load(f)
                    else:
                        raise ValueError(f"Unsupported config file format: {config_file.suffix}")
                
                self.config = self._dict_to_config(data)
                print(f"Loaded configuration from {config_file}")
                
            except Exception as e:
                print(f"Warning: Failed to load config from {config_file}: {e}")
                print("Using default configuration")
                self.config = MazeGeneratorConfig()
        else:
            print("No configuration file found, using defaults")
            self.config = MazeGeneratorConfig()
        
        return self.config
    
    def save_config(self, config_path: Optional[Union[str, Path]] = None) -> None:
        """Save current configuration to file."""
        if config_path:
            self.config_path = Path(config_path)
        elif not self.config_path:
            self.config_path = self.DEFAULT_CONFIG_PATHS[0]
        
        # Create directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert config to dictionary
        config_dict = self._config_to_dict(self.config)
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_path.suffix.lower() in ['.yaml', '.yml']:
                    if not HAS_YAML:
                        raise ImportError("PyYAML is required for YAML config files. Install with: pip install PyYAML")
                    yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                elif self.config_path.suffix.lower() == '.json':
                    json.dump(config_dict, f, indent=2)
                else:
                    # Default to JSON if YAML not available
                    if HAS_YAML:
                        yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                    else:
                        json.dump(config_dict, f, indent=2)
            
            print(f"Configuration saved to {self.config_path}")
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def _find_config_file(self) -> Optional[Path]:
        """Find the configuration file to use."""
        if self.config_path and self.config_path.exists():
            return self.config_path
        
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                return path
        
        return None
    
    def _dict_to_config(self, data: Dict[str, Any]) -> MazeGeneratorConfig:
        """Convert dictionary to configuration object."""
        config = MazeGeneratorConfig()
        
        if 'visualization' in data:
            vis_data = data['visualization']
            config.visualization = VisualizationConfig(
                cell_size=vis_data.get('cell_size', 20),
                wall_width=vis_data.get('wall_width', 2),
                colors=vis_data.get('colors', config.visualization.colors)
            )
        
        if 'generation' in data:
            gen_data = data['generation']
            config.generation = GenerationConfig(
                default_algorithm=gen_data.get('default_algorithm', 'dfs'),
                default_width=gen_data.get('default_width', 20),
                default_height=gen_data.get('default_height', 20),
                default_seed=gen_data.get('default_seed'),
                animation_delay_ms=gen_data.get('animation_delay_ms', 50)
            )
        
        if 'solving' in data:
            solve_data = data['solving']
            config.solving = SolvingConfig(
                default_algorithm=solve_data.get('default_algorithm', 'astar'),
                animation_delay_ms=solve_data.get('animation_delay_ms', 100),
                show_visited=solve_data.get('show_visited', True),
                show_path=solve_data.get('show_path', True)
            )
        
        if 'export' in data:
            export_data = data['export']
            config.export = ExportConfig(
                default_format=export_data.get('default_format', 'png'),
                default_dpi=export_data.get('default_dpi', 300),
                jpeg_quality=export_data.get('jpeg_quality', 95),
                add_border=export_data.get('add_border', True),
                add_title=export_data.get('add_title', True),
                output_directory=export_data.get('output_directory', 'output'),
                organize_by_algorithm=export_data.get('organize_by_algorithm', False),
                organize_by_date=export_data.get('organize_by_date', False),
                auto_create_directories=export_data.get('auto_create_directories', True),
                use_timestamped_filenames=export_data.get('use_timestamped_filenames', False),
                cleanup_temp_files=export_data.get('cleanup_temp_files', True),
                temp_file_max_age_hours=export_data.get('temp_file_max_age_hours', 24)
            )
        
        return config
    
    def _config_to_dict(self, config: MazeGeneratorConfig) -> Dict[str, Any]:
        """Convert configuration object to dictionary."""
        return {
            'visualization': asdict(config.visualization),
            'generation': asdict(config.generation),
            'solving': asdict(config.solving),
            'export': asdict(config.export),
        }
    
    def get_config(self) -> MazeGeneratorConfig:
        """Get the current configuration."""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration with new values."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                if isinstance(value, dict):
                    # Update nested configuration
                    current_value = getattr(self.config, key)
                    for nested_key, nested_value in value.items():
                        if hasattr(current_value, nested_key):
                            setattr(current_value, nested_key, nested_value)
                else:
                    setattr(self.config, key, value)
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = MazeGeneratorConfig()
    
    def validate_config(self) -> bool:
        """Validate the current configuration."""
        try:
            # Validate visualization config
            if self.config.visualization.cell_size <= 0:
                raise ValueError("Cell size must be positive")
            if self.config.visualization.wall_width < 0:
                raise ValueError("Wall width must be non-negative")
            
            # Validate generation config
            if self.config.generation.default_width <= 0:
                raise ValueError("Default width must be positive")
            if self.config.generation.default_height <= 0:
                raise ValueError("Default height must be positive")
            if self.config.generation.animation_delay_ms < 0:
                raise ValueError("Animation delay must be non-negative")
            
            # Validate solving config
            if self.config.solving.animation_delay_ms < 0:
                raise ValueError("Animation delay must be non-negative")
            
            # Validate export config
            if self.config.export.default_dpi <= 0:
                raise ValueError("DPI must be positive")
            if not (0 <= self.config.export.jpeg_quality <= 100):
                raise ValueError("JPEG quality must be between 0 and 100")
            
            return True
            
        except ValueError as e:
            print(f"Configuration validation error: {e}")
            return False


# Global configuration manager instance
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
        _config_manager.load_config()
    return _config_manager


def get_config() -> MazeGeneratorConfig:
    """Get the current configuration."""
    return get_config_manager().get_config()
