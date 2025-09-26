#!/usr/bin/env python3
"""
Test script to verify that example scripts work correctly.

This script runs all example scripts and verifies they complete successfully,
even in environments with missing optional dependencies.
"""

import sys
import subprocess
import tempfile
import shutil
from pathlib import Path


def test_example_script(script_path: Path, timeout: int = 60) -> bool:
    """Test a single example script."""
    print(f"Testing {script_path.name}...")
    
    try:
        # Run the script with a timeout
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=Path.cwd(),  # Run from project root, not examples directory
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {script_path.name} completed successfully")
            if result.stdout:
                print(f"   Output: {result.stdout[:100]}...")
            return True
        else:
            print(f"❌ {script_path.name} failed with exit code {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_path.name} timed out after {timeout} seconds")
        return False
    except Exception as e:
        print(f"❌ {script_path.name} failed with exception: {e}")
        return False


def test_all_examples():
    """Test all example scripts."""
    print("🧪 Testing Example Scripts")
    print("=" * 40)
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found")
        return False
    
    # List of example scripts to test
    example_scripts = [
        "basic_usage.py",
        "output_directory_demo.py",
        "performance_comparison.py",
    ]
    
    results = []
    
    for script_name in example_scripts:
        script_path = examples_dir / script_name
        
        if script_path.exists():
            # Set timeout based on script type
            timeout = 120 if "performance" in script_name else 60
            result = test_example_script(script_path, timeout)
            results.append((script_name, result))
        else:
            print(f"⚠️  {script_name} not found")
            results.append((script_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    for script_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{script_name:25} | {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    return passed == len(results)


def test_with_minimal_deps():
    """Test examples in a minimal dependency environment."""
    print("\n🔬 Testing with Minimal Dependencies")
    print("=" * 45)
    
    # Create a temporary environment simulation
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy source files to temp directory
        src_dir = Path("src")
        if src_dir.exists():
            shutil.copytree(src_dir, temp_path / "src")
        
        # Copy examples to temp directory
        examples_dir = Path("examples")
        if examples_dir.exists():
            shutil.copytree(examples_dir, temp_path / "examples")
        
        # Test basic_usage.py in the temp environment
        basic_usage = temp_path / "examples" / "basic_usage.py"
        if basic_usage.exists():
            print("Testing basic_usage.py in isolated environment...")
            
            # Modify PYTHONPATH to include our src
            env = {"PYTHONPATH": str(temp_path / "src")}
            
            try:
                result = subprocess.run(
                    [sys.executable, str(basic_usage)],
                    cwd=temp_path / "examples",
                    capture_output=True,
                    text=True,
                    timeout=60,
                    env={**dict(os.environ), **env} if 'os' in globals() else env
                )
                
                if result.returncode == 0:
                    print("✅ basic_usage.py works in minimal environment")
                    return True
                else:
                    print("❌ basic_usage.py failed in minimal environment")
                    if result.stderr:
                        print(f"   Error: {result.stderr[:200]}...")
                    return False
                    
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                return False
        else:
            print("⚠️  basic_usage.py not found for minimal test")
            return False


def check_generated_files():
    """Check if example scripts generate expected files."""
    print("\n📁 Checking Generated Files")
    print("=" * 30)
    
    # Look for common output files
    output_patterns = [
        "*.png",
        "*.jpg", 
        "*.svg",
        "*.txt",
        "demo_output/",
        "maze_*.png",
        "sample_*.png",
    ]
    
    found_files = []
    
    for pattern in output_patterns:
        if "*" in pattern:
            # Use glob for patterns
            from pathlib import Path
            for file_path in Path(".").glob(pattern):
                found_files.append(str(file_path))
        else:
            # Check if directory/file exists
            path = Path(pattern)
            if path.exists():
                if path.is_dir():
                    # List files in directory
                    try:
                        for file_path in path.rglob("*"):
                            if file_path.is_file():
                                found_files.append(str(file_path))
                    except PermissionError:
                        found_files.append(f"{pattern} (directory, permission denied)")
                else:
                    found_files.append(str(path))
    
    if found_files:
        print(f"Found {len(found_files)} generated files:")
        for file_path in found_files[:10]:  # Show first 10
            print(f"  📄 {file_path}")
        if len(found_files) > 10:
            print(f"  ... and {len(found_files) - 10} more files")
        return True
    else:
        print("No generated files found")
        return False


def main():
    """Run all example tests."""
    import os
    
    print("🎯 Example Scripts Test Suite")
    print("=" * 50)
    print("Testing that all example scripts work correctly")
    print()
    
    # Test all examples
    examples_passed = test_all_examples()
    
    # Check for generated files
    files_found = check_generated_files()
    
    # Overall result
    print("\n" + "=" * 50)
    if examples_passed:
        print("🎉 All example scripts passed!")
        if files_found:
            print("📁 Generated files were found")
        else:
            print("⚠️  No generated files found (may be due to missing optional dependencies)")
        return 0
    else:
        print("❌ Some example scripts failed!")
        print("This may be due to missing optional dependencies or other issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
