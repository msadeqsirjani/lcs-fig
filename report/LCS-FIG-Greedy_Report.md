# Analysis of Greedy LCS-FIG Algorithm Performance

## Abstract

This report presents a comprehensive analysis of the Greedy Algorithm for Longest Common Subsequence with Fixed-length Indel Gaps (LCS-FIG). We examine its performance characteristics, solution quality, and scalability through extensive experimental evaluation using DNA sequences of varying lengths and different gap constraints.

## 1. Introduction

The LCS-FIG problem extends the classical Longest Common Subsequence problem by introducing fixed-length gap constraints between matched elements. The greedy approach provides a fast but non-optimal solution by making locally optimal choices at each step.

### 1.1 Algorithm Overview

The greedy algorithm works by:
1. Scanning both sequences simultaneously
2. When matching characters are found, including them in the solution
3. Jumping K+1 positions ahead in both sequences after a match
4. Moving forward one position in the appropriate sequence when characters don't match

**Time Complexity**: O(n + m)  
**Space Complexity**: O(1)

### 1.2 Algorithm Pseudocode

```
Algorithm: Greedy LCS-FIG Algorithm
Input: Sequences X[1...n], Y[1...m], fixed gap K
Output: Length of LCS-FIG

Initialize i ← 1, j ← 1, LCS length ← 0
while i ≤ n and j ≤ m do
    if X[i] = Y[j] then
        LCS length ← LCS length + 1
        i ← i + K + 1
        j ← j + K + 1
    else if X[i] < Y[j] then
        i ← i + 1
    else
        j ← j + 1
return LCS length
```

## 2. Experimental Setup

### 2.1 Test Parameters

- **Sequence Lengths**: [1000, 2000, 5000, 10000, 20000, 50000, 100000]
- **Gap Constraints (K)**: [2, 5, 10, 20, 50, 100, 200]
- **Number of Runs**: 10 runs per configuration
- **Sequence Type**: Random DNA sequences (A, C, G, T)

### 2.2 Metrics

1. Execution Time (seconds)
2. Solution Length (LCS length)
3. Processing Speed (characters/second)
4. Standard Deviations
5. LCS to Input Ratio

## 3. Results and Analysis

### 3.1 Time Performance

![Time Performance](../results/lcs_fig_greedy/time_performance.png)

The time performance graph shows:
- Linear growth in execution time with sequence length (note log-log scale)
- Larger gap values (K) generally result in faster execution
- Consistent performance across multiple runs (small error bars)

### 3.2 Solution Quality

![Length Performance](../results/lcs_fig_greedy/length_performance.png)

The solution length analysis reveals:
- LCS length grows sub-linearly with input size
- Larger gap constraints result in shorter solutions
- Trade-off between execution speed and solution quality

### 3.3 Processing Efficiency

![Processing Speed](../results/lcs_fig_greedy/processing_speed.png)

Processing speed analysis shows:
- Relatively stable processing rates across sequence lengths
- Higher gap values achieve better throughput
- Some performance degradation with very large sequences

## 4. Key Findings

1. **Scalability**:
   - The algorithm demonstrates excellent scalability, handling sequences up to 100,000 characters efficiently
   - Linear time complexity is confirmed by empirical results

2. **Gap Constraint Impact**:
   - Larger K values improve processing speed but reduce solution quality
   - Optimal K value depends on specific application requirements

3. **Performance Characteristics**:
   - Consistent performance across multiple runs
   - Memory usage remains constant regardless of input size
   - Processing speed is influenced more by K than sequence length

## 5. Trade-offs and Recommendations

### 5.1 Trade-offs

1. **Speed vs. Quality**:
   - Larger gap values increase speed but decrease solution quality
   - Smaller gap values provide better solutions but slower execution

2. **Memory vs. Optimality**:
   - Constant memory usage achieved by sacrificing solution optimality
   - No backtracking or dynamic programming tables needed

### 5.2 Recommendations

1. **For Speed-Critical Applications**:
   - Use larger gap values (K ≥ 50)
   - Suitable for real-time processing of long sequences

2. **For Quality-Critical Applications**:
   - Use smaller gap values (K ≤ 20)
   - Consider alternative algorithms if optimality is crucial

3. **For Balanced Performance**:
   - Use moderate gap values (20 ≤ K ≤ 50)
   - Provides good trade-off between speed and solution quality

## 6. Conclusion

The Greedy LCS-FIG algorithm proves to be an efficient solution for processing large sequences with fixed-gap constraints. Its linear time complexity and constant space usage make it particularly suitable for applications where speed and memory efficiency are prioritized over solution optimality.

The experimental results demonstrate that the algorithm can effectively process sequences of 100,000+ characters while maintaining consistent performance characteristics. The gap constraint parameter provides a flexible means of tuning the algorithm's behavior to meet specific application requirements.

## 7. Future Work

1. Comparison with other LCS-FIG algorithms
2. Analysis on different sequence types
3. Investigation of parallel processing opportunities
4. Development of adaptive gap constraint strategies 