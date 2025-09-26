#!/usr/bin/env python3
"""
Comprehensive demo launcher for the Procedural Maze Generator.

This script provides a menu-driven interface to run all available demos
and generate sample outputs.
"""

import sys
import subprocess
from pathlib import Path
import argparse


class DemoLauncher:
    """Main demo launcher with menu interface."""
    
    def __init__(self):
        """Initialize the demo launcher."""
        self.demo_dir = Path(__file__).parent
        self.project_root = self.demo_dir.parent
    
    def print_banner(self):
        """Print the demo banner."""
        print("🎯" + "=" * 58 + "🎯")
        print("🎯  PROCEDURAL MAZE GENERATOR - COMPREHENSIVE DEMO  🎯")
        print("🎯" + "=" * 58 + "🎯")
        print()
        print("Welcome to the interactive demo system!")
        print("This launcher provides access to all demo features.")
        print()
    
    def show_menu(self):
        """Show the main demo menu."""
        print("📋 Available Demos:")
        print("=" * 30)
        print("1. 🚀 Interactive Python Demo")
        print("2. 🐚 Shell Script Demo")
        print("3. 🎨 Generate Sample Outputs")
        print("4. 🎬 Create Animated Demos")
        print("5. 📊 Run Performance Benchmarks")
        print("6. 🧪 Test All Examples")
        print("7. 📁 Initialize Demo Environment")
        print("8. 🧹 Clean Demo Outputs")
        print("9. ❓ Show Help")
        print("0. 🚪 Exit")
        print()
    
    def run_interactive_demo(self, quick: bool = False):
        """Run the interactive Python demo."""
        print("🚀 Running Interactive Python Demo...")
        print("-" * 40)
        
        script_path = self.demo_dir / "interactive_demo.py"
        cmd = [sys.executable, str(script_path)]
        
        if quick:
            cmd.append("--quick")
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Demo failed with exit code {e.returncode}")
        except KeyboardInterrupt:
            print("\n⏹️  Demo interrupted by user")
    
    def run_shell_demo(self, quick: bool = False):
        """Run the shell script demo."""
        print("🐚 Running Shell Script Demo...")
        print("-" * 40)
        
        script_path = self.demo_dir / "demo.sh"
        cmd = [str(script_path)]
        
        if quick:
            cmd.append("--quick")
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Demo failed with exit code {e.returncode}")
        except FileNotFoundError:
            print("❌ Shell script not found or not executable")
            print("Try: chmod +x demo/demo.sh")
        except KeyboardInterrupt:
            print("\n⏹️  Demo interrupted by user")
    
    def generate_samples(self):
        """Generate sample outputs."""
        print("🎨 Generating Sample Outputs...")
        print("-" * 40)
        
        script_path = self.demo_dir / "generate_samples.py"
        cmd = [sys.executable, str(script_path)]
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Sample generation failed with exit code {e.returncode}")
        except KeyboardInterrupt:
            print("\n⏹️  Sample generation interrupted by user")
    
    def create_animations(self):
        """Create animated demos."""
        print("🎬 Creating Animated Demos...")
        print("-" * 40)
        print("Note: This requires PIL (Pillow) for GIF creation")
        
        script_path = self.demo_dir / "create_animated_demo.py"
        cmd = [sys.executable, str(script_path)]
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Animation creation failed with exit code {e.returncode}")
            if e.returncode == 1:
                print("💡 Try installing Pillow: pip install Pillow")
        except KeyboardInterrupt:
            print("\n⏹️  Animation creation interrupted by user")
    
    def run_benchmarks(self):
        """Run performance benchmarks."""
        print("📊 Running Performance Benchmarks...")
        print("-" * 40)
        
        example_path = self.project_root / "examples" / "performance_comparison.py"
        cmd = [sys.executable, str(example_path)]
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Benchmarks failed with exit code {e.returncode}")
        except KeyboardInterrupt:
            print("\n⏹️  Benchmarks interrupted by user")
    
    def test_examples(self):
        """Test all example scripts."""
        print("🧪 Testing All Examples...")
        print("-" * 40)
        
        examples_dir = self.project_root / "examples"
        example_scripts = [
            "basic_usage.py",
            "output_directory_demo.py",
            "performance_comparison.py"
        ]
        
        for script_name in example_scripts:
            script_path = examples_dir / script_name
            if script_path.exists():
                print(f"\n🔍 Testing {script_name}...")
                cmd = [sys.executable, str(script_path)]
                
                try:
                    result = subprocess.run(cmd, cwd=self.project_root, 
                                          capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        print(f"✅ {script_name} completed successfully")
                    else:
                        print(f"❌ {script_name} failed with exit code {result.returncode}")
                        if result.stderr:
                            print(f"Error: {result.stderr[:200]}...")
                except subprocess.TimeoutExpired:
                    print(f"⏰ {script_name} timed out")
                except KeyboardInterrupt:
                    print(f"\n⏹️  Testing interrupted by user")
                    break
            else:
                print(f"⚠️  {script_name} not found")
    
    def initialize_environment(self):
        """Initialize the demo environment."""
        print("📁 Initializing Demo Environment...")
        print("-" * 40)
        
        # Create output directories
        directories = [
            "demo_output",
            "demo/samples",
            "demo/animations",
            "demo/readme_examples"
        ]
        
        for dir_name in directories:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {dir_path}")
        
        # Initialize output directory structure using CLI
        print("\n🏗️  Initializing output directory structure...")
        cmd = ["maze-gen", "output", "init", "--directory", "demo_output"]
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Output directory structure initialized")
        except subprocess.CalledProcessError:
            print("⚠️  Could not initialize output directory (maze-gen not found)")
        except FileNotFoundError:
            print("⚠️  maze-gen command not found. Install the package first.")
    
    def clean_outputs(self):
        """Clean demo outputs."""
        print("🧹 Cleaning Demo Outputs...")
        print("-" * 40)
        
        import shutil
        
        # Directories to clean
        clean_dirs = [
            "demo_output",
            "demo/samples",
            "demo/animations",
            "demo/readme_examples"
        ]
        
        for dir_name in clean_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"🗑️  Removed: {dir_path}")
                except Exception as e:
                    print(f"⚠️  Could not remove {dir_path}: {e}")
            else:
                print(f"ℹ️  Directory not found: {dir_path}")
        
        print("✅ Cleanup completed")
    
    def show_help(self):
        """Show help information."""
        print("❓ Demo Help")
        print("=" * 20)
        print()
        print("🎯 Demo Components:")
        print("• Interactive Demo: Step-by-step Python demo with explanations")
        print("• Shell Demo: Automated shell script with colored output")
        print("• Sample Generation: Create example outputs for documentation")
        print("• Animated Demos: Create GIF animations (requires Pillow)")
        print("• Benchmarks: Performance comparison of algorithms")
        print("• Example Tests: Verify all example scripts work")
        print()
        print("🔧 Requirements:")
        print("• Python 3.8+ with maze generator installed")
        print("• Optional: Pillow for GIF creation")
        print("• Optional: matplotlib for advanced visualizations")
        print()
        print("📁 Output Locations:")
        print("• demo_output/ - Main demo outputs")
        print("• demo/samples/ - Generated sample files")
        print("• demo/animations/ - Animated GIFs")
        print("• demo/readme_examples/ - README examples")
        print()
        print("💡 Tips:")
        print("• Run 'Initialize Demo Environment' first")
        print("• Use quick mode for faster demos")
        print("• Check the demo/README.md for more details")
        print()
    
    def run_menu(self):
        """Run the interactive menu."""
        while True:
            self.show_menu()
            
            try:
                choice = input("Select an option (0-9): ").strip()
                print()
                
                if choice == "0":
                    print("👋 Thanks for trying the Procedural Maze Generator!")
                    break
                elif choice == "1":
                    quick = input("Run in quick mode? (y/N): ").lower().startswith('y')
                    self.run_interactive_demo(quick)
                elif choice == "2":
                    quick = input("Run in quick mode? (y/N): ").lower().startswith('y')
                    self.run_shell_demo(quick)
                elif choice == "3":
                    self.generate_samples()
                elif choice == "4":
                    self.create_animations()
                elif choice == "5":
                    self.run_benchmarks()
                elif choice == "6":
                    self.test_examples()
                elif choice == "7":
                    self.initialize_environment()
                elif choice == "8":
                    confirm = input("Are you sure you want to clean all outputs? (y/N): ")
                    if confirm.lower().startswith('y'):
                        self.clean_outputs()
                elif choice == "9":
                    self.show_help()
                else:
                    print("❌ Invalid choice. Please select 0-9.")
                
                if choice != "0":
                    input("\nPress Enter to continue...")
                    print("\n" * 2)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo launcher interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Demo launcher closed. Goodbye!")
                break


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Procedural Maze Generator Demo Launcher")
    parser.add_argument("--auto", choices=["interactive", "shell", "samples", "animations", "benchmarks", "test", "init", "clean"],
                       help="Run a specific demo automatically without menu")
    parser.add_argument("--quick", action="store_true", help="Run demos in quick mode")
    
    args = parser.parse_args()
    
    launcher = DemoLauncher()
    
    if args.auto:
        # Run specific demo automatically
        launcher.print_banner()
        
        if args.auto == "interactive":
            launcher.run_interactive_demo(args.quick)
        elif args.auto == "shell":
            launcher.run_shell_demo(args.quick)
        elif args.auto == "samples":
            launcher.generate_samples()
        elif args.auto == "animations":
            launcher.create_animations()
        elif args.auto == "benchmarks":
            launcher.run_benchmarks()
        elif args.auto == "test":
            launcher.test_examples()
        elif args.auto == "init":
            launcher.initialize_environment()
        elif args.auto == "clean":
            launcher.clean_outputs()
    else:
        # Run interactive menu
        launcher.print_banner()
        launcher.run_menu()


if __name__ == "__main__":
    main()
