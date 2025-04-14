#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Create timestamp for unique results directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULTS_DIR="results/run_rmq_$TIMESTAMP"
mkdir -p "$RESULTS_DIR"

# Create logs directory in case it doesn't exist
mkdir -p logs

# Run the experiments
echo "Running RMQ-FIG experiments..."
python src/RMQ-FIG/test_rmq_fig.py

# Move results to timestamped directory
cp results/rmq_performance_plot.png "$RESULTS_DIR/"
cp results/rmq_length_plot.png "$RESULTS_DIR/"
cp results/rmq_performance_data.txt "$RESULTS_DIR/"

# Create a summary file
echo "Creating summary..."
{
    echo "RMQ-FIG Algorithm Experiment Results"
    echo "=================================="
    echo "Run Time: $(date)"
    echo "----------------------------------"
    echo "Performance Data:"
    echo "----------------------------------"
    cat "results/rmq_performance_data.txt"
} > "$RESULTS_DIR/summary.txt"

echo "Experiments completed successfully!"
echo "Results are saved in: $RESULTS_DIR" 