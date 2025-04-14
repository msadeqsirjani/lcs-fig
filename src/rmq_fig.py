#!/usr/bin/env python3

import time
import psutil
import numpy as np
from typing import List, Tuple
import json
import os

class RMQStructure:
    def __init__(self, n: int, m: int):
        """Initialize RMQ structure for a 2D table."""
        self.n = n
        self.m = m
        self.table = np.zeros((n+1, m+1), dtype=int)
        
    def update(self, i: int, j: int, value: int) -> None:
        """Update value at position (i,j)."""
        self.table[i][j] = value
        
    def query(self, i1: int, i2: int, j1: int, j2: int) -> int:
        """Query maximum value in rectangle [(i1,j1), (i2,j2)]."""
        if i1 < 0 or j1 < 0:
            return 0
        return np.max(self.table[i1:i2+1, j1:j2+1])

class RMQFIG:
    def __init__(self):
        """Initialize RMQ-FIG algorithm."""
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
        return process.memory_info().rss / 1024 / 1024  # Convert to MB
        
    def solve(self, X: str, Y: str, K: int) -> Tuple[int, List[str]]:
        """
        Solve LCS-FIG using RMQ approach.
        
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
        rmq = RMQStructure(n, m)
        dp = np.zeros((n+1, m+1), dtype=int)
        prev = {}  # Store previous positions for backtracking
        
        # Main algorithm
        for i in range(1, n+1):
            for j in range(1, m+1):
                if X[i-1] == Y[j-1]:
                    # Query best previous value within gap constraint
                    prev_best = rmq.query(
                        max(0, i-K-1), i-1,
                        max(0, j-K-1), j-1
                    )
                    if prev_best > 0:
                        dp[i][j] = prev_best + 1
                        # Store previous position for backtracking
                        for pi in range(max(0, i-K-1), i):
                            for pj in range(max(0, j-K-1), j):
                                if dp[pi][pj] == prev_best:
                                    prev[(i,j)] = (pi, pj)
                                    break
                            if (i,j) in prev:
                                break
                    else:
                        dp[i][j] = 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                rmq.update(i, j, dp[i][j])
        
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
    
    rmq_fig = RMQFIG()
    length, subsequence = rmq_fig.solve(X, Y, K)
    
    print(f"Length of LCS-FIG: {length}")
    print(f"Subsequence: {''.join(subsequence)}")
    print(f"Performance: {rmq_fig.get_average_performance()}") 