# LCS-FIG: Longest Common Subsequence with Gap Constraints

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