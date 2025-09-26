"""Visualization components for maze generation and solving."""

# Always available
from .ascii_renderer import AsciiRenderer

# Optional imports with graceful fallback
__all__ = ["AsciiRenderer"]

try:
    from .matplotlib_renderer import MatplotlibRenderer
    __all__.append("MatplotlibRenderer")
except ImportError:
    MatplotlibRenderer = None

try:
    from .pygame_renderer import PygameRenderer
    __all__.append("PygameRenderer")
except ImportError:
    PygameRenderer = None

try:
    from .image_exporter import ImageExporter
    __all__.append("ImageExporter")
except ImportError:
    ImageExporter = None
