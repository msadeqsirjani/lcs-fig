#!/usr/bin/env python3

import os
import time
import json
import random
import string
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from rmq_fig import RMQFIG
from fig_dp import FIGDP

def generate_random_sequence(length: int) -> str:
    """Generate random sequence of given length."""
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def run_comparison(sizes: List[int], k_values: List[int], num_trials: int = 3) -> Dict:
    """Run comparison between all algorithms."""
    figdp = FIGDP()
    rmqfig = RMQFIG()
    
    results = {
        'sizes': sizes,
        'k_values': k_values,
        'figdp': {k: {'time': [], 'memory': [], 'lcs_length': []} for k in k_values},
        'rmqfig': {k: {'time': [], 'memory': [], 'lcs_length': []} for k in k_values},
        'speedup': {k: [] for k in k_values},
        'memory_ratio': {k: [] for k in k_values}
    }
    
    for size in sizes:
        print(f"Processing size {size}...")
        for k in k_values:
            print(f"  K = {k}")
            figdp_times = []
            rmqfig_times = []
            figdp_memories = []
            rmqfig_memories = []
            figdp_lengths = []
            rmqfig_lengths = []
            
            for trial in range(num_trials):
                print(f"    Trial {trial + 1}/{num_trials}")
                X = generate_random_sequence(size)
                Y = generate_random_sequence(size)
                
                # Run FIG-DP
                length_dp, _ = figdp.solve(X, Y, k)
                figdp_times.append(figdp.performance_data['time'][-1])
                figdp_memories.append(figdp.performance_data['memory'][-1])
                figdp_lengths.append(length_dp)
                
                # Run RMQ-FIG
                length_rmq, _ = rmqfig.solve(X, Y, k)
                rmqfig_times.append(rmqfig.performance_data['time'][-1])
                rmqfig_memories.append(rmqfig.performance_data['memory'][-1])
                rmqfig_lengths.append(length_rmq)
            
            # Calculate averages
            avg_figdp_time = np.mean(figdp_times)
            avg_rmqfig_time = np.mean(rmqfig_times)
            avg_figdp_memory = np.mean(figdp_memories)
            avg_rmqfig_memory = np.mean(rmqfig_memories)
            
            results['figdp'][k]['time'].append(avg_figdp_time)
            results['figdp'][k]['memory'].append(avg_figdp_memory)
            results['figdp'][k]['lcs_length'].append(np.mean(figdp_lengths))
            
            results['rmqfig'][k]['time'].append(avg_rmqfig_time)
            results['rmqfig'][k]['memory'].append(avg_rmqfig_memory)
            results['rmqfig'][k]['lcs_length'].append(np.mean(rmqfig_lengths))
            
            # Calculate speedup and memory ratio
            speedup = avg_figdp_time / avg_rmqfig_time if avg_rmqfig_time > 0 else 0
            memory_ratio = avg_rmqfig_memory / avg_figdp_memory if avg_figdp_memory > 0 else 0
            
            results['speedup'][k].append(speedup)
            results['memory_ratio'][k].append(memory_ratio)
    
    return results

def plot_results(results: Dict, output_dir: str) -> None:
    """Generate plots from comparison results."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Time comparison plot for each K
    for k in results['k_values']:
        plt.figure(figsize=(12, 6))
        plt.plot(results['sizes'], results['figdp'][k]['time'], 'b-', label='FIG-DP')
        plt.plot(results['sizes'], results['rmqfig'][k]['time'], 'r-', label='RMQ-FIG')
        plt.xlabel('Input Size')
        plt.ylabel('Time (seconds)')
        plt.title(f'Performance Comparison (K={k})')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f'performance_k{k}.png'))
        plt.close()
    
    # Combined time comparison plot
    plt.figure(figsize=(12, 6))
    for k in results['k_values']:
        plt.plot(results['sizes'], results['figdp'][k]['time'], '--', label=f'FIG-DP (K={k})')
        plt.plot(results['sizes'], results['rmqfig'][k]['time'], '-', label=f'RMQ-FIG (K={k})')
    plt.xlabel('Input Size')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison (All K values)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'performance_comparison.png'))
    plt.close()
    
    # Memory comparison plot
    plt.figure(figsize=(12, 6))
    for k in results['k_values']:
        plt.plot(results['sizes'], results['figdp'][k]['memory'], '--', label=f'FIG-DP (K={k})')
        plt.plot(results['sizes'], results['rmqfig'][k]['memory'], '-', label=f'RMQ-FIG (K={k})')
    plt.xlabel('Input Size')
    plt.ylabel('Memory Usage (MB)')
    plt.title('Memory Usage Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'memory_comparison.png'))
    plt.close()
    
    # Speedup plot
    plt.figure(figsize=(12, 6))
    for k in results['k_values']:
        plt.plot(results['sizes'], results['speedup'][k], '-', label=f'K={k}')
    plt.xlabel('Input Size')
    plt.ylabel('Speedup (FIG-DP/RMQ-FIG)')
    plt.title('Algorithm Speedup')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'speedup.png'))
    plt.close()

def save_results(results: Dict, output_dir: str) -> None:
    """Save comparison results to JSON file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Calculate summary statistics
    summary = {
        'avg_speedup': {},
        'max_speedup': {},
        'avg_memory_ratio': {},
        'k_specific_stats': {}
    }
    
    for k in results['k_values']:
        summary['avg_speedup'][k] = np.mean(results['speedup'][k])
        summary['max_speedup'][k] = np.max(results['speedup'][k])
        summary['avg_memory_ratio'][k] = np.mean(results['memory_ratio'][k])
        
        summary['k_specific_stats'][k] = {
            'avg_speedup': np.mean(results['speedup'][k]),
            'max_speedup': np.max(results['speedup'][k]),
            'avg_memory_ratio': np.mean(results['memory_ratio'][k])
        }
    
    # Save detailed results
    with open(os.path.join(output_dir, 'comparison_results.json'), 'w') as f:
        json.dump(results, f, indent=4)
    
    # Save summary
    with open(os.path.join(output_dir, 'summary_stats.json'), 'w') as f:
        json.dump(summary, f, indent=4)

def main():
    """Main function to run algorithm comparison."""
    # Test parameters
    sizes = [100, 200, 300, 400, 500, 1000]
    k_values = [2, 3, 4, 5]
    output_dir = "comparison_results"
    
    print("Starting algorithm comparison...")
    print(f"Input sizes: {sizes}")
    print(f"K values: {k_values}")
    
    # Run comparison
    results = run_comparison(sizes, k_values)
    
    print("Generating plots...")
    plot_results(results, output_dir)
    
    print("Saving results...")
    save_results(results, output_dir)
    
    print(f"\nComparison completed. Results saved in: {output_dir}")
    
    # Print summary statistics
    print("\nSummary:")
    for k in k_values:
        print(f"\nK = {k}:")
        print(f"  Average speedup: {np.mean(results['speedup'][k]):.2f}x")
        print(f"  Maximum speedup: {np.max(results['speedup'][k]):.2f}x")
        print(f"  Average memory ratio: {np.mean(results['memory_ratio'][k]):.2f}x")

if __name__ == "__main__":
    main() 