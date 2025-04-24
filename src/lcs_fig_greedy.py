"""
Greedy Algorithm for Longest Common Subsequence with Fixed-length Indel Gaps (LCS-FIG)

This module implements a greedy approximation algorithm for the LCS-FIG problem.
The algorithm provides a fast but non-optimal solution by selecting matching characters
and jumping K+1 positions ahead in both sequences when a match is found.

Time Complexity: O(n + m) where n and m are the lengths of input sequences
Space Complexity: O(1) as it uses only constant extra space
"""

import random
import string
import time

class GreedyLCSFIG:
    """
    A class implementing the Greedy algorithm for LCS-FIG problem.
    """
    
    def __init__(self, seq1: str, seq2: str, k: int):
        """
        Initialize the GreedyLCSFIG solver.
        
        Args:
            seq1 (str): First input sequence
            seq2 (str): Second input sequence
            k (int): Fixed gap length (K >= 0)
            
        Raises:
            ValueError: If K is negative
        """
        if k < 0:
            raise ValueError("Gap length K must be non-negative")
            
        self.seq1 = seq1
        self.seq2 = seq2
        self.k = k
        self.performance_data = {
            'time': [],
            'length': []
        }
        
    def solve(self) -> tuple[int, float]:
        """
        Compute an approximation of the Longest Common Subsequence with Fixed-length Indel Gaps.
        
        Returns:
            tuple: (length of LCS-FIG, execution time in seconds)
        """
        start_time = time.time()
        
        n, m = len(self.seq1), len(self.seq2)
        i = j = 0
        lcs_length = 0
        
        while i < n and j < m:
            if self.seq1[i] == self.seq2[j]:
                lcs_length += 1
                i += self.k + 1
                j += self.k + 1
            elif self.seq1[i] < self.seq2[j]:
                i += 1
            else:
                j += 1
                
        execution_time = time.time() - start_time
        self.performance_data['time'].append(execution_time)
        self.performance_data['length'].append(lcs_length)
        
        return lcs_length, execution_time
    
    def get_performance_data(self) -> dict:
        """
        Get the performance data collected during solving.
        
        Returns:
            dict: Dictionary containing performance metrics
        """
        return {
            'avg_time': sum(self.performance_data['time']) / len(self.performance_data['time']) if self.performance_data['time'] else 0,
            'avg_length': sum(self.performance_data['length']) / len(self.performance_data['length']) if self.performance_data['length'] else 0,
            'num_runs': len(self.performance_data['time'])
        }
    
    @staticmethod
    def generate_random_sequence(length: int) -> str:
        """
        Generate a random sequence of specified length containing lowercase letters.
        
        Args:
            length (int): Length of sequence to generate
            
        Returns:
            str: Random sequence of lowercase letters
        """
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @staticmethod
    def generate_random_dna_sequence(length: int) -> str:
        """
        Generate a random DNA sequence of specified length.
        
        Args:
            length (int): Length of sequence to generate
            
        Returns:
            str: Random DNA sequence
        """
        return ''.join(random.choices(['A', 'C', 'G', 'T'], k=length))

if __name__ == "__main__":
    # Example usage
    X = "ABCDE"
    Y = "ACE"
    K = 1
    
    solver = GreedyLCSFIG(X, Y, K)
    length, time = solver.solve()
    print(f"LCS-FIG length for X='{X}', Y='{Y}', K={K}: {length}")
    print(f"Execution time: {time:.4f} seconds") 