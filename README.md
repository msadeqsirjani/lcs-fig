# LCS-FIG: Longest Common Subsequence with Fixed Interval Gap Constraints

This project implements and compares two algorithms for solving the Longest Common Subsequence with Fixed Interval Gap Constraints (LCS-FIG) problem:

1. **FIG-DP** - A dynamic programming approach
2. **RMQ-FIG** - An optimized version using Range Maximum Query (RMQ) data structures

## Problem Definition

Given two sequences X and Y, the goal is to find the longest common subsequence Z subject to the constraint that for any two consecutive elements of Z, if Z[i−1] appears at position p in X (or q in Y), then Z[i] must appear no later than position p + K + 1 in X (and similarly in Y), where K is a fixed gap parameter.

This variant is especially useful in bioinformatics and text analysis where controlled spacing between matches is required.

## Algorithms

### FIG-DP Algorithm

A straightforward dynamic programming approach to solve the LCS-FIG problem. The algorithm builds a 2D table where each cell represents the length of the longest common subsequence ending at the corresponding positions in the input sequences, subject to the gap constraint.

**Time Complexity:** O(nm)  
**Space Complexity:** O(nm)

### RMQ-FIG Algorithm

The RMQ-FIG algorithm enhances the dynamic programming approach by using a Range Maximum Query (RMQ) structure to quickly find the best LCS length within the valid gap range. This optimization speeds up the algorithm compared to standard DP.

**Time Complexity:** O(nm log n)  
**Space Complexity:** O(nm)

## Project Structure

- `src/fig_dp.py` - Implementation of the FIG-DP algorithm
- `src/rmq_fig.py` - Implementation of the RMQ-FIG algorithm
- `src/test_fig_dp.py` - Testing script for the FIG-DP algorithm
- `src/test_rmq_fig.py` - Testing script for the RMQ-FIG algorithm
- `src/compare_algorithms.py` - Script to compare both algorithms
- `src/run.py` - Unified command-line interface to run algorithms

## Requirements

- Python 3.7+
- NumPy
- Matplotlib

## Installation

```bash
pip install numpy matplotlib
```

## Usage

### Running a Single Algorithm

To run a specific algorithm with default parameters (random DNA sequences of length 100, K=5):

```bash
# Run FIG-DP algorithm
python src/run.py --algorithm figdp

# Run RMQ-FIG algorithm
python src/run.py --algorithm rmqfig
```

### Comparing Both Algorithms

```bash
python src/run.py --algorithm both
```

### Customizing Parameters

You can customize the input parameters:

```bash
python src/run.py --algorithm both --size 1000 --gap 10
```

### Using Custom Sequences

```bash
python src/run.py --seq1 "ACGTACGT" --seq2 "ACGTACGT" --gap 3
```

### Specifying Output File

```bash
python src/run.py --output "results/my_results.txt"
```

### Full Usage Help

```bash
python src/run.py --help
```

## Running Comprehensive Tests

To run comprehensive tests on various sequence lengths and gap parameters:

```bash
# Test FIG-DP algorithm
python src/test_fig_dp.py

# Test RMQ-FIG algorithm
python src/test_rmq_fig.py

# Compare both algorithms
python src/compare_algorithms.py
```

## Output

The results are saved to the `results/` directory. Each result file contains:

- Input parameters and sequences
- Solution length and sequence
- Execution time
- Position mapping of the matched elements
- Nucleotide composition analysis

When comparing both algorithms, the output also includes:
- Performance comparison
- Speedup calculation
- Differences in the solution

## Performance Analysis

The algorithms are compared based on:

1. **Execution time** - How fast each algorithm finds the solution
2. **Solution length** - Whether both algorithms find solutions of the same length
3. **Memory usage** - Space requirements for each approach

## Credits

This implementation was developed as part of the Analysis of Algorithms course project.

## Overview
This project implements the Longest Common Subsequence with Gap Constraints (LCS-FIG) algorithm, specifically designed for DNA sequence analysis. The algorithm extends the classic LCS problem by introducing gap constraints between consecutive matches, making it particularly suitable for biological sequence analysis applications.

### Key Features
- Efficient dynamic programming implementation
- Gap-constrained sequence matching
- DNA sequence analysis support
- Performance visualization tools
- Comprehensive testing framework

## Installation

### Prerequisites
- Python 3.8 or higher
- NumPy 1.21.0 or higher
- Matplotlib (for visualization)
- pytest (for testing)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/msadeqsirjani/lcs-fig.git
cd lcs-fig
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example
```python
from src.fig_dp import FIGDP

# Initialize sequences and gap constraint
seq1 = "ACGTACGT"
seq2 = "ACGACGT"
k = 2

# Create LCS-FIG instance
fig = FIGDP(seq1, seq2, k)

# Find longest common subsequence
result = fig.solve()
print(f"LCS Length: {result.length}")
print(f"LCS Sequence: {result.sequence}")
```

### Running Tests
```bash
pytest src/test_fig_dp.py
```

### Performance Analysis
```python
from src.performance_analysis import run_performance_tests

# Run performance tests with different sequence lengths and gap constraints
results = run_performance_tests(
    lengths=[100, 200, 400, 800],
    k_values=[5, 10, 20],
    runs_per_test=5
)

# Generate performance plots
results.plot_performance()
results.plot_length_analysis()
```

## Algorithm Details

### Problem Definition
Given:
- Two sequences X[1..n] and Y[1..m]
- A gap constraint parameter K

Find: The longest common subsequence Z such that:
- For any consecutive elements in Z, their positions in X and Y are at most K+1 positions apart

### Time Complexity
- Overall: O(nm)
- Space Complexity: O(nm)

## Project Structure
```
lcs-fig/
├── src/
│   ├── fig_dp.py           # Core algorithm implementation
│   ├── test_fig_dp.py      # Unit tests
│   └── performance_analysis.py  # Performance testing utilities
├── results/                # Performance analysis results
├── report/                # Documentation and analysis
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Performance Results

### Test Environment
- Hardware: MacBook Pro M1
- OS: macOS 24.3.0
- Python: 3.8
- NumPy: 1.21.0

### Sample Results
For sequences of length 800 with K=10:
```
DNA Sequence 1 Length: 800
DNA Sequence 2 Length: 800
Maximum LCS Length: 187
Execution Time: 0.0234 seconds
```

## Documentation

For detailed information about the implementation and analysis, please refer to:
- [Technical Report](report/LCS-FIG_Report.md)
- [Performance Analysis](report/LCS-FIG_Report.md#experimental-analysis)
- [API Documentation](docs/api.md)

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Original LCS-FIG Algorithm Paper
- NumPy Documentation
- Python Performance Optimization Guide
- Bioinformatics Algorithms: An Active Learning Approach

## Contact
Mohammad Sadegh Sirjani - [GitHub Profile](https://github.com/msadeqsirjani)

Project Link: [https://github.com/msadeqsirjani/lcs-fig](https://github.com/msadeqsirjani/lcs-fig) 