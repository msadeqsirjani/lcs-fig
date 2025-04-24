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
from lcs_fig_greedy import GreedyLCSFIG

def generate_random_sequence(length: int) -> str:
    """Generate random sequence of given length."""
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def run_comparison(sizes: List[int], k_values: List[int], num_trials: int = 3) -> Dict:
    """Run comparison between all algorithms."""
    results = {
        'sizes': sizes,
        'k_values': k_values,
        'figdp': {k: {'time': [], 'memory': [], 'lcs_length': []} for k in k_values},
        'rmqfig': {k: {'time': [], 'memory': [], 'lcs_length': []} for k in k_values},
        'greedy': {k: {'time': [], 'memory': [], 'lcs_length': []} for k in k_values},
        'relative_performance': {k: {
            'figdp_vs_rmq': [],
            'figdp_vs_greedy': [],
            'rmq_vs_greedy': []
        } for k in k_values},
        'solution_quality': {k: {
            'greedy_vs_optimal': []
        } for k in k_values}
    }
    
    for size in sizes:
        print(f"Processing size {size}...")
        for k in k_values:
            print(f"  K = {k}")
            figdp_metrics = {'time': [], 'memory': [], 'length': []}
            rmqfig_metrics = {'time': [], 'memory': [], 'length': []}
            greedy_metrics = {'time': [], 'memory': [], 'length': []}
            
            for trial in range(num_trials):
                print(f"    Trial {trial + 1}/{num_trials}")
                X = generate_random_sequence(size)
                Y = generate_random_sequence(size)
                
                # Run FIG-DP (optimal solution)
                figdp = FIGDP()
                start_time = time.time()
                length_dp, _ = figdp.solve(X, Y, k)
                dp_time = time.time() - start_time
                figdp_metrics['time'].append(dp_time)
                figdp_metrics['memory'].append(figdp.get_memory_usage())
                figdp_metrics['length'].append(length_dp)
                
                # Run RMQ-FIG
                rmqfig = RMQFIG()
                start_time = time.time()
                length_rmq, _ = rmqfig.solve(X, Y, k)
                rmq_time = time.time() - start_time
                rmqfig_metrics['time'].append(rmq_time)
                rmqfig_metrics['memory'].append(rmqfig.get_memory_usage())
                rmqfig_metrics['length'].append(length_rmq)
                
                # Run Greedy LCS-FIG
                greedy = GreedyLCSFIG(X, Y, k)
                start_time = time.time()
                length_greedy, greedy_time = greedy.solve()
                greedy_metrics['time'].append(greedy_time)
                greedy_metrics['memory'].append(0)  # Constant memory usage
                greedy_metrics['length'].append(length_greedy)
            
            # Calculate averages
            for algo, metrics in [('figdp', figdp_metrics), 
                                ('rmqfig', rmqfig_metrics), 
                                ('greedy', greedy_metrics)]:
                results[algo][k]['time'].append(np.mean(metrics['time']))
                results[algo][k]['memory'].append(np.mean(metrics['memory']))
                results[algo][k]['lcs_length'].append(np.mean(metrics['length']))
            
            # Calculate relative performance
            avg_dp_time = np.mean(figdp_metrics['time'])
            avg_rmq_time = np.mean(rmqfig_metrics['time'])
            avg_greedy_time = np.mean(greedy_metrics['time'])
            
            results['relative_performance'][k]['figdp_vs_rmq'].append(avg_dp_time / avg_rmq_time)
            results['relative_performance'][k]['figdp_vs_greedy'].append(avg_dp_time / avg_greedy_time)
            results['relative_performance'][k]['rmq_vs_greedy'].append(avg_rmq_time / avg_greedy_time)
            
            # Calculate solution quality (compared to optimal FIG-DP solution)
            avg_dp_length = np.mean(figdp_metrics['length'])
            avg_greedy_length = np.mean(greedy_metrics['length'])
            results['solution_quality'][k]['greedy_vs_optimal'].append(avg_greedy_length / avg_dp_length)
    
    return results

def plot_results(results: Dict, output_dir: str) -> None:
    """Generate plots from comparison results."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Combined performance plot (log scale)
    plt.figure(figsize=(15, 10))
    for k in results['k_values']:
        plt.plot(results['sizes'], results['figdp'][k]['time'], '--', label=f'FIG-DP (K={k})')
        plt.plot(results['sizes'], results['rmqfig'][k]['time'], ':', label=f'RMQ-FIG (K={k})')
        plt.plot(results['sizes'], results['greedy'][k]['time'], '-', label=f'Greedy (K={k})')
    plt.xlabel('Input Size')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison of All Algorithms')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'performance_comparison.png'))
    plt.close()
    
    # Solution quality comparison
    plt.figure(figsize=(15, 10))
    for k in results['k_values']:
        plt.plot(results['sizes'], results['solution_quality'][k]['greedy_vs_optimal'], 
                '-o', label=f'K={k}')
    plt.xlabel('Input Size')
    plt.ylabel('Solution Quality Ratio (Greedy/Optimal)')
    plt.title('Greedy Algorithm Solution Quality vs Optimal Solution')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'solution_quality.png'))
    plt.close()
    
    # Relative performance plots
    metrics = ['figdp_vs_rmq', 'figdp_vs_greedy', 'rmq_vs_greedy']
    titles = ['FIG-DP vs RMQ-FIG', 'FIG-DP vs Greedy', 'RMQ-FIG vs Greedy']
    
    for metric, title in zip(metrics, titles):
        plt.figure(figsize=(15, 10))
        for k in results['k_values']:
            plt.plot(results['sizes'], 
                    results['relative_performance'][k][metric], 
                    '-o', label=f'K={k}')
        plt.xlabel('Input Size')
        plt.ylabel('Time Ratio')
        plt.title(f'Relative Performance: {title}')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f'relative_performance_{metric}.png'))
        plt.close()

def save_results(results: Dict, output_dir: str) -> None:
    """Save comparison results and generate summary statistics."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    summary = {
        'average_performance': {},
        'solution_quality': {},
        'memory_usage': {},
        'recommendations': {}
    }
    
    for k in results['k_values']:
        summary['average_performance'][k] = {
            'figdp_avg_time': np.mean(results['figdp'][k]['time']),
            'rmqfig_avg_time': np.mean(results['rmqfig'][k]['time']),
            'greedy_avg_time': np.mean(results['greedy'][k]['time'])
        }
        
        summary['solution_quality'][k] = {
            'avg_quality_ratio': np.mean(results['solution_quality'][k]['greedy_vs_optimal']),
            'min_quality_ratio': np.min(results['solution_quality'][k]['greedy_vs_optimal']),
            'max_quality_ratio': np.max(results['solution_quality'][k]['greedy_vs_optimal'])
        }
        
        # Determine recommendations based on metrics
        fastest_algo = min(['figdp', 'rmqfig', 'greedy'], 
                         key=lambda x: np.mean(results[x][k]['time']))
        
        summary['recommendations'][k] = {
            'fastest_algorithm': fastest_algo,
            'quality_vs_speed_tradeoff': summary['solution_quality'][k]['avg_quality_ratio'],
            'recommended_for': {
                'speed_critical': 'greedy' if fastest_algo == 'greedy' else 'rmqfig',
                'quality_critical': 'figdp',
                'balanced': 'rmqfig'
            }
        }
    
    # Save detailed results
    with open(os.path.join(output_dir, 'comparison_results.json'), 'w') as f:
        json.dump(results, f, indent=4)
    
    # Save summary
    with open(os.path.join(output_dir, 'summary_stats.json'), 'w') as f:
        json.dump(summary, f, indent=4)
    
    return summary

def main():
    """Main function to run algorithm comparison."""
    # Test parameters
    sizes = [100, 500, 1000, 2000, 5000]
    k_values = [2, 5, 10, 20, 40]
    output_dir = "results/algorithm_comparison"
    
    print("Starting comprehensive algorithm comparison...")
    print(f"Input sizes: {sizes}")
    print(f"K values: {k_values}")
    
    # Run comparison
    results = run_comparison(sizes, k_values)
    
    print("Generating plots...")
    plot_results(results, output_dir)
    
    print("Saving results and generating summary...")
    summary = save_results(results, output_dir)
    
    print(f"\nComparison completed. Results saved in: {output_dir}")
    
    # Print key findings
    print("\nKey Findings:")
    for k in k_values:
        print(f"\nK = {k}:")
        print("  Performance Ratios:")
        print(f"    FIG-DP vs RMQ-FIG: {np.mean(results['relative_performance'][k]['figdp_vs_rmq']):.2f}x")
        print(f"    FIG-DP vs Greedy: {np.mean(results['relative_performance'][k]['figdp_vs_greedy']):.2f}x")
        print(f"    RMQ-FIG vs Greedy: {np.mean(results['relative_performance'][k]['rmq_vs_greedy']):.2f}x")
        print(f"  Solution Quality:")
        print(f"    Greedy vs Optimal: {np.mean(results['solution_quality'][k]['greedy_vs_optimal'])*100:.1f}%")
        print(f"  Recommended for:")
        print(f"    Speed-critical: {summary['recommendations'][k]['recommended_for']['speed_critical']}")
        print(f"    Quality-critical: {summary['recommendations'][k]['recommended_for']['quality_critical']}")
        print(f"    Balanced: {summary['recommendations'][k]['recommended_for']['balanced']}")

if __name__ == "__main__":
    main() 