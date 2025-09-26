#!/bin/bash

# Procedural Maze Generator - Demo Script
# This script demonstrates all major features of the maze generator

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Demo configuration
DEMO_DIR="demo_output"
PAUSE_BETWEEN_STEPS=true

# Function to print colored headers
print_header() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

# Function to print step descriptions
print_step() {
    echo -e "\n${CYAN}🔹 $1${NC}"
}

# Function to run commands with description
run_command() {
    local cmd="$1"
    local description="$2"
    
    if [ -n "$description" ]; then
        echo -e "\n${YELLOW}📝 $description${NC}"
    fi
    
    echo -e "${GREEN}💻 Running: $cmd${NC}"
    
    if [ "$PAUSE_BETWEEN_STEPS" = true ]; then
        echo -e "${PURPLE}   Press Enter to continue...${NC}"
        read -r
    fi
    
    if eval "$cmd"; then
        echo -e "${GREEN}✅ Command completed successfully${NC}"
    else
        echo -e "${RED}❌ Command failed${NC}"
        return 1
    fi
}

# Function to check if maze-gen is available
check_installation() {
    if ! command -v maze-gen &> /dev/null; then
        echo -e "${RED}❌ maze-gen command not found${NC}"
        echo "Please install the procedural maze generator first:"
        echo "  pip install -e ."
        exit 1
    fi
    echo -e "${GREEN}✅ maze-gen is available${NC}"
}

# Demo: Basic maze generation
demo_basic_generation() {
    print_header "Basic Maze Generation"
    
    print_step "Generate a simple 10x8 maze using DFS algorithm"
    run_command "maze-gen generate 10 8 --algorithm dfs --format ascii" \
        "This creates a maze using Depth-First Search and displays it as ASCII art"
    
    print_step "Generate a maze and save to PNG file"
    run_command "maze-gen generate 15 10 --algorithm kruskal --format png --output $DEMO_DIR/basic_maze.png" \
        "Save a Kruskal-generated maze as a PNG image"
    
    print_step "Generate with custom start/end points"
    run_command "maze-gen generate 12 8 --algorithm prim --start 0 0 --end 11 7 --format ascii" \
        "Create a maze with specified start and end positions"
}

# Demo: Output directory management
demo_output_management() {
    print_header "Output Directory Management"
    
    print_step "Initialize output directory structure"
    run_command "maze-gen output init --directory $DEMO_DIR" \
        "Create organized directory structure for maze outputs"
    
    print_step "Show output directory information"
    run_command "maze-gen output info --directory $DEMO_DIR" \
        "Display directory statistics and configuration"
    
    print_step "Generate mazes organized by algorithm"
    for algo in dfs kruskal prim; do
        run_command "maze-gen generate 12 8 --algorithm $algo --format png --output-dir $DEMO_DIR --organize-by-algorithm" \
            "Generate ${algo^^} maze organized by algorithm"
    done
    
    print_step "List generated files"
    run_command "maze-gen output list --directory $DEMO_DIR --type images" \
        "Show all generated image files"
}

# Demo: File organization options
demo_file_organization() {
    print_header "File Organization Options"
    
    print_step "Generate with timestamped filenames"
    run_command "maze-gen generate 10 6 --algorithm dfs --format png --output-dir $DEMO_DIR --timestamped" \
        "Create maze with timestamp in filename"
    
    print_step "Generate organized by date"
    run_command "maze-gen generate 8 8 --algorithm kruskal --format ascii --output-dir $DEMO_DIR --organize-by-date" \
        "Organize output files by creation date"
    
    print_step "Generate in multiple formats"
    for format in png svg ascii; do
        run_command "maze-gen generate 10 8 --algorithm prim --format $format --output-dir $DEMO_DIR" \
            "Generate maze in ${format^^} format"
    done
}

# Demo: Maze solving
demo_maze_solving() {
    print_header "Maze Solving"
    
    print_step "Generate and solve with A* algorithm"
    run_command "maze-gen solve 15 12 --gen-algorithm dfs --solve-algorithm astar --format png --output-dir $DEMO_DIR --show-visited" \
        "Create maze and solve it showing the solution path"
    
    print_step "Compare different solving algorithms"
    for solver in astar dijkstra bfs; do
        run_command "maze-gen solve 10 8 --gen-algorithm kruskal --solve-algorithm $solver --format ascii" \
            "Solve maze using ${solver^^} algorithm"
    done
}

# Demo: Advanced features
demo_advanced_features() {
    print_header "Advanced Features"
    
    print_step "Benchmark different algorithms"
    run_command "maze-gen benchmark 15 15 --iterations 5" \
        "Compare performance of different generation algorithms"
    
    print_step "Generate large maze with custom settings"
    run_command "maze-gen generate 25 20 --algorithm wilson --format svg --output-dir $DEMO_DIR --cell-size 15 --wall-width 1 --title 'Large Wilson Maze'" \
        "Create a large maze with custom visualization parameters"
}

# Demo: Directory exploration
demo_directory_exploration() {
    print_header "Exploring Generated Files"
    
    print_step "Show directory structure"
    if [ -d "$DEMO_DIR" ]; then
        echo -e "${CYAN}📁 Directory structure:${NC}"
        tree "$DEMO_DIR" 2>/dev/null || find "$DEMO_DIR" -type f | head -20
    fi
    
    print_step "List all generated files"
    run_command "maze-gen output list --directory $DEMO_DIR" \
        "Show all files organized by type"
    
    print_step "Show final directory statistics"
    run_command "maze-gen output info --directory $DEMO_DIR" \
        "Display final directory information"
}

# Main demo function
run_full_demo() {
    echo -e "${BLUE}🎯 Procedural Maze Generator - Shell Demo${NC}"
    echo "============================================================"
    echo "This demo will showcase all major features of the maze generator,"
    echo "including the new output directory management system."
    echo ""
    echo "The demo will:"
    echo "• Generate mazes with different algorithms"
    echo "• Demonstrate output directory management"
    echo "• Show file organization options"
    echo "• Solve mazes with various algorithms"
    echo "• Display advanced features"
    echo ""
    echo -e "${YELLOW}📂 Demo files will be saved to: $(pwd)/$DEMO_DIR${NC}"
    
    if [ "$1" != "--no-pause" ]; then
        echo -e "\n${PURPLE}Press Enter to start the demo...${NC}"
        read -r
    else
        PAUSE_BETWEEN_STEPS=false
        echo -e "\n${GREEN}🚀 Running demo without pauses...${NC}"
    fi
    
    # Check installation
    check_installation
    
    # Run all demo sections
    demo_basic_generation
    demo_output_management
    demo_file_organization
    demo_maze_solving
    demo_advanced_features
    demo_directory_exploration
    
    # Summary
    print_header "Demo Complete!"
    echo -e "${GREEN}✅ Demo completed successfully!${NC}"
    echo -e "${CYAN}📁 Generated files are available in: $(pwd)/$DEMO_DIR${NC}"
    echo -e "\n${BLUE}🎉 Thank you for trying the Procedural Maze Generator!${NC}"
    echo "Visit https://github.com/yourusername/procedural-maze-generator for more information."
}

# Quick demo function
run_quick_demo() {
    echo -e "${GREEN}🚀 Running Quick Demo${NC}"
    PAUSE_BETWEEN_STEPS=false
    
    check_installation
    
    run_command "maze-gen output init --directory $DEMO_DIR"
    run_command "maze-gen generate 12 8 --algorithm dfs --format ascii"
    run_command "maze-gen generate 10 8 --algorithm kruskal --format png --output-dir $DEMO_DIR"
    run_command "maze-gen solve 8 6 --gen-algorithm prim --solve-algorithm astar --format ascii"
    run_command "maze-gen output info --directory $DEMO_DIR"
    
    echo -e "\n${GREEN}✅ Quick demo complete!${NC}"
}

# Handle command line arguments
case "${1:-}" in
    --quick)
        run_quick_demo
        ;;
    --no-pause)
        run_full_demo --no-pause
        ;;
    --help|-h)
        echo "Usage: $0 [--quick|--no-pause|--help]"
        echo "  --quick     Run a quick demo without all features"
        echo "  --no-pause  Run full demo without pausing between steps"
        echo "  --help      Show this help message"
        ;;
    *)
        run_full_demo
        ;;
esac
