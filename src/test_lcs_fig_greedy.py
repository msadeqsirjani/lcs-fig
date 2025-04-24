#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import random
import string
import os
import time
from datetime import datetime
from lcs_fig_greedy import GreedyLCSFIG

def setup_test_dir():
    """Set up test directory."""
    test_dir = "results/lcs_fig_greedy"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    return test_dir

def format_sequence(seq: str, line_length: int = 80) -> str:
    """Format a DNA sequence with line breaks and position markers."""
    lines = []
    for i in range(0, len(seq), line_length):
        chunk = seq[i:i+line_length]
        pos = str(i+1).rjust(8)
        lines.append(f"{pos} {chunk}")
    return '\n'.join(lines)

def test_basic_functionality():
    """Test basic functionality with simple sequences."""
    print("\nTesting basic functionality...")
    test_cases = [
        ("ABCDE", "ACE", 1, 3),  # Basic case
        ("ABCDE", "ABCDE", 1, 3),  # Identical sequences
        ("ABCDE", "XYZ", 1, 0),  # No common subsequence
        ("AAAAAA", "AAA", 2, 2),  # Repeated characters
    ]
    
    all_passed = True
    for X, Y, K, expected_length in test_cases:
        solver = GreedyLCSFIG(X, Y, K)
        length, _ = solver.solve()
        if length == expected_length:
            print(f"✓ Test passed: X='{X}', Y='{Y}', K={K}, Length={length}")
        else:
            print(f"✗ Test failed: X='{X}', Y='{Y}', K={K}, Expected={expected_length}, Got={length}")
            all_passed = False
    
    return all_passed

def test_gap_constraints():
    """Test different gap constraints."""
    print("\nTesting gap constraints...")
    X = "ABCDEFG"
    Y = "ACEG"
    
    test_cases = [
        (1, 2),  # Strict gap constraint
        (2, 2),  # Medium gap constraint
        (3, 2),  # Relaxed gap constraint
    ]
    
    all_passed = True
    for K, expected_length in test_cases:
        solver = GreedyLCSFIG(X, Y, K)
        length, _ = solver.solve()
        if length == expected_length:
            print(f"✓ Test passed: K={K}, Length={length}")
        else:
            print(f"✗ Test failed: K={K}, Expected={expected_length}, Got={length}")
            all_passed = False
    
    return all_passed

def test_invalid_input():
    """Test handling of invalid inputs."""
    print("\nTesting invalid inputs...")
    X = "ABCDE"
    Y = "ACE"
    
    try:
        GreedyLCSFIG(X, Y, -1)
        print("✗ Test failed: Expected ValueError for negative K")
        return False
    except ValueError:
        print("✓ Test passed: Correctly raised ValueError for negative K")
        return True

def test_empty_sequences():
    """Test behavior with empty sequences."""
    print("\nTesting empty sequences...")
    test_cases = [
        ("", "", 1, 0),  # Both empty
        ("ABC", "", 1, 0),  # Second empty
        ("", "ABC", 1, 0),  # First empty
    ]
    
    all_passed = True
    for X, Y, K, expected_length in test_cases:
        solver = GreedyLCSFIG(X, Y, K)
        length, _ = solver.solve()
        if length == expected_length:
            print(f"✓ Test passed: X='{X}', Y='{Y}', K={K}, Length={length}")
        else:
            print(f"✗ Test failed: X='{X}', Y='{Y}', K={K}, Expected={expected_length}, Got={length}")
            all_passed = False
    
    return all_passed

def run_experiments(test_dir):
    """Run intensive experiments with varying input sizes and gap constraints."""
    print("\nRunning intensive performance experiments...")
    
    # More extensive sequence lengths
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    
    # More varied gap constraints
    gap_constraints = [2, 5, 10, 20, 50, 100, 200]
    
    results = {k: [] for k in gap_constraints}
    
    # Track total progress
    total_experiments = len(sizes) * len(gap_constraints)
    current_experiment = 0
    
    for size in sizes:
        print(f"\nTesting with sequence length {size}...")
        
        # Generate longer sequences for each size
        print("Generating random sequences...")
        seq1 = GreedyLCSFIG.generate_random_dna_sequence(size)
        seq2 = GreedyLCSFIG.generate_random_dna_sequence(size)
        
        for k in gap_constraints:
            current_experiment += 1
            print(f"\nProgress: {current_experiment}/{total_experiments}")
            print(f"Testing with K={k}")
            
            # Increase number of runs for better averaging
            num_runs = 10
            solver = GreedyLCSFIG(seq1, seq2, k)
            
            run_times = []
            run_lengths = []
            
            print(f"Performing {num_runs} runs...")
            for run in range(num_runs):
                print(f"Run {run + 1}/{num_runs}", end='\r')
                length, execution_time = solver.solve()
                run_times.append(execution_time)
                run_lengths.append(length)
                
                if run == 0:  # Save detailed results for first run
                    with open(f'{test_dir}/size_{size}_k_{k}_detailed.txt', 'w') as f:
                        # Write header with timestamp
                        f.write("="*80 + "\n")
                        f.write("Greedy LCS-FIG Algorithm Detailed Results\n")
                        f.write("="*80 + "\n")
                        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Input Size: {size}\n")
                        f.write(f"Gap Constraint (K): {k}\n")
                        f.write("\n")

                        # Write input sequence statistics
                        f.write("-"*80 + "\n")
                        f.write("Input Sequence Statistics\n")
                        f.write("-"*80 + "\n")
                        
                        for seq_name, seq in [("Sequence 1", seq1), ("Sequence 2", seq2)]:
                            f.write(f"\n{seq_name}:\n")
                            f.write(f"Length: {len(seq)}\n")
                            f.write("Nucleotide Distribution:\n")
                            for nucleotide in ['A', 'C', 'G', 'T']:
                                count = seq.count(nucleotide)
                                percentage = (count / len(seq)) * 100
                                f.write(f"{nucleotide}: {count} ({percentage:.2f}%)\n")
                            
                            # Calculate sequence complexity metrics
                            dinucleotides = [seq[i:i+2] for i in range(len(seq)-1)]
                            unique_dinucleotides = len(set(dinucleotides))
                            f.write(f"Unique Dinucleotides: {unique_dinucleotides}\n")
                            
                        # Write detailed performance metrics
                        f.write("\n" + "-"*80 + "\n")
                        f.write("Performance Metrics\n")
                        f.write("-"*80 + "\n")
                        f.write(f"LCS Length: {length}\n")
                        f.write(f"Execution Time: {execution_time:.4f} seconds\n")
                        f.write(f"Characters Processed per Second: {(len(seq1) + len(seq2))/execution_time:.2f}\n")
                        f.write(f"LCS to Input Ratio: {length/size:.4f}\n")
            
            # Calculate statistics
            avg_time = sum(run_times) / num_runs
            avg_length = sum(run_lengths) / num_runs
            std_time = (sum((t - avg_time) ** 2 for t in run_times) / num_runs) ** 0.5
            std_length = (sum((l - avg_length) ** 2 for l in run_lengths) / num_runs) ** 0.5
            
            results[k].append({
                'size': size,
                'avg_time': avg_time,
                'std_time': std_time,
                'avg_length': avg_length,
                'std_length': std_length,
                'chars_per_second': (size * 2) / avg_time
            })
            
            print(f"\nResults for K={k}:")
            print(f"Average Time: {avg_time:.4f} ± {std_time:.4f} seconds")
            print(f"Average Length: {avg_length:.2f} ± {std_length:.2f}")
            print(f"Processing Speed: {(size * 2) / avg_time:.2f} chars/second")
    
    return results

def plot_results(results, test_dir):
    """Create and save detailed performance plots."""
    print("\nGenerating detailed performance plots...")
    
    # Extract data for plotting
    sizes = sorted(list({r['size'] for k in results.keys() for r in results[k]}))
    
    # Plot 1: Time vs Size with error bars
    plt.figure(figsize=(15, 10))
    for k in results.keys():
        times = [r['avg_time'] for r in results[k]]
        errors = [r['std_time'] for r in results[k]]
        plt.errorbar(sizes, times, yerr=errors, label=f'K={k}', marker='o')
    
    plt.xlabel('Sequence Length')
    plt.ylabel('Time (seconds)')
    plt.title('LCS-FIG Algorithm Time Performance')
    plt.grid(True)
    plt.legend()
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig(f'{test_dir}/time_performance.png')
    plt.close()
    
    # Plot 2: Length vs Size with error bars
    plt.figure(figsize=(15, 10))
    for k in results.keys():
        lengths = [r['avg_length'] for r in results[k]]
        errors = [r['std_length'] for r in results[k]]
        plt.errorbar(sizes, lengths, yerr=errors, label=f'K={k}', marker='o')
    
    plt.xlabel('Sequence Length')
    plt.ylabel('LCS Length')
    plt.title('LCS-FIG Solution Length')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'{test_dir}/length_performance.png')
    plt.close()
    
    # Plot 3: Processing Speed
    plt.figure(figsize=(15, 10))
    for k in results.keys():
        speeds = [r['chars_per_second'] for r in results[k]]
        plt.plot(sizes, speeds, label=f'K={k}', marker='o')
    
    plt.xlabel('Sequence Length')
    plt.ylabel('Characters Processed per Second')
    plt.title('Processing Speed')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'{test_dir}/processing_speed.png')
    plt.close()
    
    # Save detailed results
    with open(f'{test_dir}/detailed_results.txt', 'w') as f:
        f.write("Detailed Performance Results\n")
        f.write("="*80 + "\n\n")
        
        for k in sorted(results.keys()):
            f.write(f"\nResults for K={k}\n")
            f.write("-"*40 + "\n")
            f.write("Size\tTime(s)\tStd_Time\tLength\tStd_Length\tChars/s\n")
            
            for r in sorted(results[k], key=lambda x: x['size']):
                f.write(f"{r['size']}\t{r['avg_time']:.4f}\t{r['std_time']:.4f}\t")
                f.write(f"{r['avg_length']:.2f}\t{r['std_length']:.2f}\t")
                f.write(f"{r['chars_per_second']:.2f}\n")

def main():
    """Run all tests and experiments."""
    test_dir = setup_test_dir()
    
    # Run basic tests
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Gap Constraints", test_gap_constraints),
        ("Invalid Input", test_invalid_input),
        ("Empty Sequences", test_empty_sequences)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n{'-'*20} Testing {test_name} {'-'*20}")
        if not test_func():
            all_passed = False
            print(f"✗ {test_name} tests failed")
        else:
            print(f"✓ {test_name} tests passed")
    
    # Run performance experiments
    print(f"\n{'-'*20} Running Performance Tests {'-'*20}")
    results = run_experiments(test_dir)
    plot_results(results, test_dir)
    
    print("\nTest Summary:")
    print("✓" if all_passed else "✗", "Basic tests:", "All Passed" if all_passed else "Some Failed")
    print("✓ Performance tests completed")
    print("✓ Results saved in:", test_dir)

if __name__ == '__main__':
    main() 