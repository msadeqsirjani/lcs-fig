#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Parse command line arguments
ALGORITHM="both"
SIZE=100
K=5

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -a|--algorithm) ALGORITHM="$2"; shift ;;
        -s|--size) SIZE="$2"; shift ;;
        -k|--gap) K="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Create results directory if it doesn't exist
mkdir -p results
mkdir -p logs

# Create timestamp for unique results directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULTS_DIR="results/run_$TIMESTAMP"
mkdir -p "$RESULTS_DIR"

# Run the appropriate algorithm
if [ "$ALGORITHM" == "figdp" ]; then
    echo "Running FIG-DP algorithm with size=$SIZE, k=$K..."
    python -c "from src.FIG_DP.fig_dp import FIGDP; import numpy as np; seq1 = ''.join(np.random.choice(['A', 'C', 'G', 'T'], size=$SIZE)); seq2 = ''.join(np.random.choice(['A', 'C', 'G', 'T'], size=$SIZE)); solver = FIGDP(seq1, seq2, $K); length, seq, time = solver.solve(); print(f'Length: {length}, Time: {time:.4f}s')"
elif [ "$ALGORITHM" == "rmqfig" ]; then
    echo "Running RMQ-FIG algorithm with size=$SIZE, k=$K..."
    python -c "from src.RMQ_FIG.rmq_fig import RMQFIG; import numpy as np; seq1 = ''.join(np.random.choice(['A', 'C', 'G', 'T'], size=$SIZE)); seq2 = ''.join(np.random.choice(['A', 'C', 'G', 'T'], size=$SIZE)); solver = RMQFIG(seq1, seq2, $K); length, seq, time = solver.solve(); print(f'Length: {length}, Time: {time:.4f}s')"
else
    echo "Running comparison with size=$SIZE, k=$K..."
    python src/compare_algorithms.py --size $SIZE --gap $K
fi

echo "Done!" 