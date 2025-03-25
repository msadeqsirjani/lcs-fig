#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Create timestamp for unique results directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULTS_DIR="results/run_$TIMESTAMP"
mkdir -p "$RESULTS_DIR"

# Run the experiments
echo "Running FIG-DP experiments..."
python src/test_fig_dp.py

# Move results to timestamped directory
mv performance_plot.png "$RESULTS_DIR/"
mv performance_data.txt "$RESULTS_DIR/"

# Create a summary file
echo "Creating summary..."
{
    echo "FIG-DP Algorithm Experiment Results"
    echo "=================================="
    echo "Run Time: $(date)"
    echo "----------------------------------"
    echo "Performance Data:"
    echo "----------------------------------"
    cat "$RESULTS_DIR/performance_data.txt"
} > "$RESULTS_DIR/summary.txt"

echo "Experiments completed successfully!"
echo "Results are saved in: $RESULTS_DIR" 