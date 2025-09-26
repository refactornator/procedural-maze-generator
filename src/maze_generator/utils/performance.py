"""Performance measurement utilities."""

import time
import functools
from typing import Callable, Any, Dict, List
from contextlib import contextmanager


class Timer:
    """A simple timer for measuring execution time."""
    
    def __init__(self):
        """Initialize the timer."""
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
    
    def start(self) -> None:
        """Start the timer."""
        self.start_time = time.perf_counter()
        self.end_time = None
        self.elapsed_time = None
    
    def stop(self) -> float:
        """Stop the timer and return elapsed time."""
        if self.start_time is None:
            raise RuntimeError("Timer not started")
        
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        return self.elapsed_time
    
    def reset(self) -> None:
        """Reset the timer."""
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
    
    def get_elapsed(self) -> float:
        """Get elapsed time without stopping the timer."""
        if self.start_time is None:
            return 0.0
        
        current_time = time.perf_counter()
        return current_time - self.start_time
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


@contextmanager
def time_it(description: str = "Operation"):
    """Context manager for timing operations."""
    timer = Timer()
    print(f"Starting {description}...")
    timer.start()
    try:
        yield timer
    finally:
        elapsed = timer.stop()
        print(f"{description} completed in {elapsed:.4f} seconds")


def benchmark_function(func: Callable, *args, iterations: int = 10, **kwargs) -> Dict[str, float]:
    """Benchmark a function by running it multiple times."""
    times = []
    
    for _ in range(iterations):
        timer = Timer()
        timer.start()
        func(*args, **kwargs)
        elapsed = timer.stop()
        times.append(elapsed)
    
    return {
        'min': min(times),
        'max': max(times),
        'avg': sum(times) / len(times),
        'total': sum(times),
        'iterations': iterations,
        'times': times
    }


def timed(func: Callable) -> Callable:
    """Decorator to time function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timer = Timer()
        timer.start()
        result = func(*args, **kwargs)
        elapsed = timer.stop()
        print(f"{func.__name__} executed in {elapsed:.4f} seconds")
        return result
    return wrapper


class PerformanceProfiler:
    """A simple performance profiler for tracking multiple operations."""
    
    def __init__(self):
        """Initialize the profiler."""
        self.timers: Dict[str, List[float]] = {}
        self.active_timers: Dict[str, Timer] = {}
    
    def start_timer(self, name: str) -> None:
        """Start a named timer."""
        if name in self.active_timers:
            raise RuntimeError(f"Timer '{name}' is already running")
        
        timer = Timer()
        timer.start()
        self.active_timers[name] = timer
    
    def stop_timer(self, name: str) -> float:
        """Stop a named timer and record the time."""
        if name not in self.active_timers:
            raise RuntimeError(f"Timer '{name}' is not running")
        
        timer = self.active_timers.pop(name)
        elapsed = timer.stop()
        
        if name not in self.timers:
            self.timers[name] = []
        self.timers[name].append(elapsed)
        
        return elapsed
    
    @contextmanager
    def timer(self, name: str):
        """Context manager for named timing."""
        self.start_timer(name)
        try:
            yield
        finally:
            self.stop_timer(name)
    
    def get_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a named timer."""
        if name not in self.timers or not self.timers[name]:
            return {}
        
        times = self.timers[name]
        return {
            'count': len(times),
            'total': sum(times),
            'avg': sum(times) / len(times),
            'min': min(times),
            'max': max(times)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all timers."""
        return {name: self.get_stats(name) for name in self.timers}
    
    def print_stats(self) -> None:
        """Print statistics for all timers."""
        print("Performance Statistics:")
        print("-" * 50)
        
        for name, stats in self.get_all_stats().items():
            if stats:
                print(f"{name:20} | Count: {stats['count']:3d} | "
                      f"Total: {stats['total']:8.4f}s | "
                      f"Avg: {stats['avg']:8.4f}s | "
                      f"Min: {stats['min']:8.4f}s | "
                      f"Max: {stats['max']:8.4f}s")
    
    def reset(self) -> None:
        """Reset all timers and statistics."""
        self.timers.clear()
        self.active_timers.clear()


# Global profiler instance
_profiler = PerformanceProfiler()


def get_profiler() -> PerformanceProfiler:
    """Get the global profiler instance."""
    return _profiler
