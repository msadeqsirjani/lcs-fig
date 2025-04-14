#!/usr/bin/env python3

import unittest
import random
import string
import os
from rmq_fig import RMQFIG

class TestRMQFIG(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.rmq_fig = RMQFIG()
        self.test_dir = "test_results"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
    def generate_random_sequence(self, length: int) -> str:
        """Generate random sequence of given length."""
        return ''.join(random.choices(string.ascii_uppercase, k=length))
    
    def test_basic_functionality(self):
        """Test basic functionality with simple sequences."""
        test_cases = [
            ("ABCDE", "ACE", 1, 3),  # Basic case
            ("ABCDE", "ABCDE", 1, 5),  # Identical sequences
            ("ABCDE", "XYZ", 1, 0),  # No common subsequence
            ("AAAAAA", "AAA", 2, 3),  # Repeated characters
        ]
        
        for X, Y, K, expected_length in test_cases:
            length, subsequence = self.rmq_fig.solve(X, Y, K)
            self.assertEqual(length, expected_length)
            
    def test_gap_constraints(self):
        """Test different gap constraints."""
        X = "ABCDEFG"
        Y = "ACEG"
        
        # Test with different K values
        test_cases = [
            (1, 2),  # Strict gap constraint
            (2, 3),  # Medium gap constraint
            (3, 4),  # Relaxed gap constraint
        ]
        
        for K, expected_length in test_cases:
            length, subsequence = self.rmq_fig.solve(X, Y, K)
            self.assertEqual(length, expected_length)
            
    def test_performance_scaling(self):
        """Test performance scaling with input size."""
        sizes = [10, 50, 100]
        K = 3
        
        for size in sizes:
            X = self.generate_random_sequence(size)
            Y = self.generate_random_sequence(size)
            
            length, subsequence = self.rmq_fig.solve(X, Y, K)
            
            # Verify performance data was recorded
            self.assertTrue(len(self.rmq_fig.performance_data['time']) > 0)
            self.assertTrue(len(self.rmq_fig.performance_data['memory']) > 0)
            
    def test_memory_usage(self):
        """Test memory usage tracking."""
        X = self.generate_random_sequence(100)
        Y = self.generate_random_sequence(100)
        K = 3
        
        initial_memory = self.rmq_fig.get_memory_usage()
        length, subsequence = self.rmq_fig.solve(X, Y, K)
        final_memory = self.rmq_fig.get_memory_usage()
        
        # Verify memory usage is being tracked
        self.assertTrue(final_memory >= initial_memory)
        
    def test_performance_data_saving(self):
        """Test saving performance data to file."""
        # Run some test cases
        sizes = [10, 20, 30]
        K = 2
        
        for size in sizes:
            X = self.generate_random_sequence(size)
            Y = self.generate_random_sequence(size)
            self.rmq_fig.solve(X, Y, K)
        
        # Save performance data
        output_file = os.path.join(self.test_dir, "performance_data.json")
        self.rmq_fig.save_performance_data(output_file)
        
        # Verify file exists and contains data
        self.assertTrue(os.path.exists(output_file))
        
    def test_average_performance(self):
        """Test average performance calculation."""
        # Run multiple test cases
        for _ in range(3):
            X = self.generate_random_sequence(50)
            Y = self.generate_random_sequence(50)
            self.rmq_fig.solve(X, Y, 2)
        
        avg_perf = self.rmq_fig.get_average_performance()
        
        # Verify average metrics
        self.assertIn('avg_time', avg_perf)
        self.assertIn('avg_memory', avg_perf)
        self.assertIn('avg_length', avg_perf)
        
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main() 