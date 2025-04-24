#!/usr/bin/env python3

import time
import psutil
import numpy as np
from typing import List, Tuple
import json
import os

class FIGDP:
    """Implementation of the basic FIG-DP algorithm."""
    def __init__(self):
        self.performance_data = {
            'time': [],
            'memory': [],
            'size': [],
            'k': [],
            'lcs_length': []
        }
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def solve(self, X: str, Y: str, K: int) -> Tuple[int, List[str]]:
        """
        Solve LCS-FIG using basic dynamic programming approach.
        
        Args:
            X: First sequence
            Y: Second sequence
            K: Gap constraint
            
        Returns:
            Tuple of (length of LCS-FIG, the actual subsequence)
        """
        start_time = time.time()
        initial_memory = self.get_memory_usage()
        
        n, m = len(X), len(Y)
        dp = np.zeros((n+1, m+1), dtype=int)
        prev = {}  # Store previous positions for backtracking
        
        # Main algorithm
        for i in range(1, n+1):
            for j in range(1, m+1):
                if X[i-1] == Y[j-1]:
                    # Check previous positions within gap constraint
                    max_prev = 0
                    max_pos = None
                    for pi in range(max(0, i-K-1), i):
                        for pj in range(max(0, j-K-1), j):
                            if dp[pi][pj] > max_prev:
                                max_prev = dp[pi][pj]
                                max_pos = (pi, pj)
                    
                    if max_prev > 0:
                        dp[i][j] = max_prev + 1
                        prev[(i,j)] = max_pos
                    else:
                        dp[i][j] = 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Record performance data
        end_time = time.time()
        final_memory = self.get_memory_usage()
        
        self.performance_data['time'].append(end_time - start_time)
        self.performance_data['memory'].append(final_memory - initial_memory)
        self.performance_data['size'].append(max(n, m))
        self.performance_data['k'].append(K)
        self.performance_data['lcs_length'].append(int(dp[n][m]))
        
        # Backtrack to get the subsequence
        lcs = []
        i, j = n, m
        max_length = dp[n][m]
        while i > 0 and j > 0:
            if (i,j) in prev:
                lcs.append(X[i-1])
                i, j = prev[(i,j)]
            elif dp[i][j] == dp[i-1][j]:
                i -= 1
            else:
                j -= 1
        
        return max_length, lcs[::-1]
    
    def save_performance_data(self, filename: str) -> None:
        """Save performance data to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.performance_data, f, indent=4)
    
    def get_average_performance(self) -> dict:
        """Get average performance metrics."""
        return {
            'avg_time': np.mean(self.performance_data['time']),
            'avg_memory': np.mean(self.performance_data['memory']),
            'avg_length': np.mean(self.performance_data['lcs_length'])
        }

if __name__ == "__main__":
    # Example usage
    X = "ABCDEFG"
    Y = "ACDEFGH"
    K = 2
    
    fig_dp = FIGDP()
    length, subsequence = fig_dp.solve(X, Y, K)
    
    print(f"Length of LCS-FIG: {length}")
    print(f"Subsequence: {''.join(subsequence)}")
    print(f"Performance: {fig_dp.get_average_performance()}") 