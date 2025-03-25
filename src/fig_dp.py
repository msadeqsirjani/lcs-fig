import numpy as np
from typing import List, Tuple
import time

class FIGDP:
    def __init__(self, seq1: str, seq2: str, k: int):
        """
        Initialize the LCS-FIG algorithm with two sequences and gap parameter.
        
        Args:
            seq1: First sequence
            seq2: Second sequence
            k: Gap constraint parameter
        """
        self.seq1 = seq1
        self.seq2 = seq2
        self.n = len(seq1)
        self.m = len(seq2)
        self.k = k
        self.dp_table = None
        self.parent = None
        
    def solve(self) -> Tuple[int, str, float]:
        """
        Solve the LCS-FIG problem using dynamic programming.
        
        Returns:
            Tuple containing:
            - Length of the longest common subsequence with gap constraints
            - The actual matching sequence
            - Time taken to solve the problem
        """
        start_time = time.time()
        
        # Initialize DP table and parent pointers
        self.dp_table = np.zeros((self.n + 1, self.m + 1), dtype=np.int32)
        self.parent = np.zeros((self.n + 1, self.m + 1), dtype=np.int32)
        
        # Fill the DP table
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                if self.seq1[i-1] == self.seq2[j-1]:
                    if i > self.k + 1 and j > self.k + 1:
                        self.dp_table[i][j] = self.dp_table[i - self.k - 1][j - self.k - 1] + 1
                        self.parent[i][j] = 1  # diagonal with gap
                    else:
                        self.dp_table[i][j] = 1
                        self.parent[i][j] = 2  # start of new sequence
                else:
                    if self.dp_table[i-1][j] >= self.dp_table[i][j-1]:
                        self.dp_table[i][j] = self.dp_table[i-1][j]
                        self.parent[i][j] = 3  # up
                    else:
                        self.dp_table[i][j] = self.dp_table[i][j-1]
                        self.parent[i][j] = 4  # left
        
        # Find the maximum value and its position
        max_length = np.max(self.dp_table)
        max_pos = np.unravel_index(np.argmax(self.dp_table), self.dp_table.shape)
        
        # Reconstruct the matching sequence
        matching_seq = self._reconstruct_sequence(max_pos[0], max_pos[1])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return max_length, matching_seq, execution_time
    
    def _reconstruct_sequence(self, i: int, j: int) -> str:
        """
        Reconstruct the matching sequence using parent pointers.
        
        Args:
            i: Current position in first sequence
            j: Current position in second sequence
            
        Returns:
            The matching sequence
        """
        sequence = []
        while i > 0 and j > 0:
            if self.parent[i][j] == 1:  # diagonal with gap
                sequence.append(self.seq1[i-1])
                i -= self.k + 1
                j -= self.k + 1
            elif self.parent[i][j] == 2:  # start of new sequence
                sequence.append(self.seq1[i-1])
                break
            elif self.parent[i][j] == 3:  # up
                i -= 1
            else:  # left
                j -= 1
        return ''.join(reversed(sequence))
    
    def get_dp_table(self) -> np.ndarray:
        """
        Get the DP table for visualization or analysis.
        
        Returns:
            The filled DP table
        """
        return self.dp_table 